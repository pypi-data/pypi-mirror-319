from datetime import timedelta
import time
import uuid
import json
import jwt

from Cryptodome.PublicKey.RSA import importKey
from django.utils import dateformat, timezone
from jwkest.jwk import RSAKey as jwk_RSAKey
from jwkest.jwk import SYMKey
from jwkest.jws import JWS
from jwkest.jwt import JWT
from jwt.utils import (base64url_decode, base64url_encode)
from jwt.exceptions import PyJWKError

from oidc_provider.lib.utils.common import get_issuer, run_processing_hook
from oidc_provider.lib.utils.dpop import compute_thumbprint
from oidc_provider.lib.claims import StandardScopeClaims
from oidc_provider.models import (
    Code,
    RSAKey,
    Token,
    TokenType,
)
from oidc_provider.lib.errors import (
    TokenError,
)
from oidc_provider import settings


def create_id_token(token, user, aud, nonce='', at_hash='', request=None, scope=None):
    """
    Creates the id_token dictionary.
    See: http://openid.net/specs/openid-connect-core-1_0.html#IDToken
    Return a dic.
    """
    if scope is None:
        scope = []
    sub = settings.get('OIDC_IDTOKEN_SUB_GENERATOR', import_str=True)(user=user)

    expires_in = settings.get('OIDC_IDTOKEN_EXPIRE')

    # Convert datetimes into timestamps.
    now = int(time.time())
    iat_time = now
    exp_time = int(now + expires_in)
    user_auth_time = user.last_login or user.date_joined
    auth_time = int(dateformat.format(user_auth_time, 'U'))

    dic = {
        'iss': get_issuer(request=request),
        'sub': sub,
        'aud': str(aud),
        'exp': exp_time,
        'iat': iat_time,
        'auth_time': auth_time,
    }

    if token.token_type == TokenType.DPoP:
        dic['webid'] = dic['sub']

    if nonce:
        dic['nonce'] = str(nonce)

    if at_hash:
        dic['at_hash'] = at_hash

    # Inlude (or not) user standard claims in the id_token.
    if settings.get('OIDC_IDTOKEN_INCLUDE_CLAIMS'):
        if settings.get('OIDC_EXTRA_SCOPE_CLAIMS'):
            custom_claims = settings.get('OIDC_EXTRA_SCOPE_CLAIMS', import_str=True)(token)
            claims = custom_claims.create_response_dic()
        else:
            claims = StandardScopeClaims(token).create_response_dic()
        dic.update(claims)

    dic = run_processing_hook(
        dic, 'OIDC_IDTOKEN_PROCESSING_HOOK',
        user=user, token=token, request=request)

    return dic


def encode_id_token(payload, client):
    """
    Represent the ID Token as a JSON Web Token (JWT).
    Return a hash.
    """
    keys = get_client_alg_keys(client)
    _jws = JWS(payload, alg=client.jwt_alg)
    return _jws.sign_compact(keys)


def decode_id_token(token, client):
    """
    Represent the ID Token as a JSON Web Token (JWT).
    Return a hash.
    """
    keys = get_client_alg_keys(client)
    return JWS().verify_compact(token, keys=keys)


def client_id_from_id_token(id_token):
    """
    Extracts the client id from a JSON Web Token (JWT).
    Returns a string or None.
    """
    payload = JWT().unpack(id_token).payload()
    aud = payload.get('aud', None)
    if aud is None:
        return None
    if isinstance(aud, list):
        return aud[0]
    return aud


def create_token(user, client, scope, id_token_dic=None, token_type=TokenType.Bearer, request=None):
    """
    Create and populate a Token object.
    Return a Token object.
    """
    token = Token()
    token.user = user
    token.client = client
    token.token_type = token_type

    # build access token
    if token_type == TokenType.DPoP:
        expires_in = settings.get('OIDC_IDTOKEN_EXPIRE')
        now = int(time.time())
        iat_time = now
        exp_time = int(now + expires_in)

        # generate JWK thumbprint
        dpop_proof = request.headers.get('dpop')
        headers = jwt.get_unverified_header(dpop_proof)
        jwk_thumbprint = compute_thumbprint(headers.get('jwk'))

        # replace the access token with a DPoP version
        # https://solid.github.io/authentication-panel/solid-oidc-primer/#authorization-code-pkce-flow-step-18
        # TODO: the webid returned below is how it's done for the sub parameter in the id token.. suitable for us?
        #  - copy the function from djangoldp_account if you can
        # TODO: https://git.startinblox.com/djangoldp-packages/django-webidoidc-provider/issues/10
        token.access_token = encode_id_token({
            "webid": settings.get('OIDC_IDTOKEN_SUB_GENERATOR', import_str=True)(user=user),
            "iss": get_issuer(request=request),
            "aud": "solid",
            "cnf": {
                "jkt": jwk_thumbprint
            },
            "client_id": client.client_id,
            "jti": str(uuid.uuid4()),
            "iat": iat_time,
            "exp": exp_time
        }, client)
    else:
        token.access_token = uuid.uuid4().hex

    if id_token_dic is not None:
        token.id_token = id_token_dic

    token.refresh_token = uuid.uuid4().hex
    token.expires_at = timezone.now() + timedelta(
        seconds=settings.get('OIDC_TOKEN_EXPIRE'))
    token.scope = scope

    return token


def create_code(user, client, scope, nonce, is_authentication,
                code_challenge=None, code_challenge_method=None):
    """
    Create and populate a Code object.
    Return a Code object.
    """
    code = Code()
    code.user = user
    code.client = client

    code.code = uuid.uuid4().hex

    if code_challenge and code_challenge_method:
        code.code_challenge = code_challenge
        code.code_challenge_method = code_challenge_method

    code.expires_at = timezone.now() + timedelta(
        seconds=settings.get('OIDC_CODE_EXPIRE'))
    code.scope = scope
    code.nonce = nonce
    code.is_authentication = is_authentication

    return code


def get_client_alg_keys(client):
    """
    Takes a client and returns the set of (server) keys associated with it.
    Returns a list of private keys, although you can get the public key from them with .publickey()
    """
    if client.jwt_alg == 'RS256':
        keys = []
        for rsakey in RSAKey.objects.all():
            keys.append(jwk_RSAKey(key=importKey(rsakey.key), kid=rsakey.kid))
        if not keys:
            raise Exception('You must add at least one RSA Key.')
    elif client.jwt_alg == 'HS256':
        keys = [SYMKey(key=client.client_secret, alg=client.jwt_alg)]
    else:
        raise Exception('Unsupported key algorithm.')

    return keys
