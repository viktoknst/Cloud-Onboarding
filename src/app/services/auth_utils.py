import time
import json

import hmac
import base64
from hashlib import sha256

SECRET = "secret".encode() # CHANGE THIS

def gen_salt():
    with open('/dev/urandom', 'br') as fp:
        random = fp.read(32)
        return base64.b64encode(random).decode('utf-8')

def hash_password(password: str, user_name: str, salt: str):
    db = ''
    return sha256((password + salt).encode()).hexdigest()


def str_to_base64(string: str) -> bytes:
    return base64.urlsafe_b64encode(string.encode())


def gen_signature_hs256(header64b: bytes, payload64b: bytes) -> bytes:
    signatureb = hmac.new(SECRET, header64b+b'.'+payload64b, sha256).digest()
    return base64.urlsafe_b64encode(signatureb)


# implements JWT as specified on wikipedia
def gen_auth_token(
    sub: str,
    iat: int | None = None,
    exp: int | None = None,
    iss: str = "Bicagis",
    alg: str = "HS256",
    cty: str = "JWT"
    ):
    DEFAULT_EXPIRY = 15 * 60 # 15 mins
    if iat == None:
        iat = str(int(time.time())) # warning: dumb code, and time is NOT posix conformant on... i'd guess microwaves
    if exp == None:
        exp = str(int(time.time()+DEFAULT_EXPIRY))
    if alg != 'HS256':
        raise Exception("Algorythm not supported or DNE")
    if cty != 'JWT':
        raise Exception("Why is this an argument? Im not sure")
    header = json.dumps({
        'cty':cty,
        'alg':alg,
    })
    payload = json.dumps({
        'iss':iss,
        'sub':sub,
        'exp':exp,
        'iat':iat
    })
    header64b = str_to_base64(header)
    payload64b = str_to_base64(payload)
    signature64b = gen_signature_hs256(header64b, payload64b)
    token64b = header64b+b'.'+payload64b+b'.'+signature64b
    return token64b.decode()


def unpack_auth_token(token: str):
    header, payload, signature = token.split('.')
    result = {}

    header = base64.urlsafe_b64decode(header).decode()
    header = json.loads(header)
    result['header'] = header

    payload = base64.urlsafe_b64decode(payload).decode()
    payload = json.loads(payload)
    result['payload'] = payload

    return result

# returns tuple (Literal["OK"| error string], token dict)
def validate_auth_token(token: str):
    try:
        header64s, payload64s, signature64s = token.split('.')
        unpacked = unpack_auth_token(token)
    except:
        return ('Malformed token', None)

    if unpacked['payload']['iss'] != 'Bicagis':
        return ('Token not issued by server', unpacked)
    if unpacked['header']['alg'] != 'HS256':
        return ('Cant verify token; algorythm not known', None)

    correct_signature64b = gen_signature_hs256(header64s.encode(), payload64s.encode())

    if signature64s.encode() != correct_signature64b:
        return ('Signature unverified', unpacked)
    if int(unpacked['payload']['exp']) < int(time.time()):
        return ('Token expired', unpacked)

    return ('OK', unpacked)


if __name__ == "__main__":
    payload = json.dumps({
        "loggedInAs": "admin",
        "iat": 1422779638
    }).encode()
    #payload = '{"loggedInAs":"admin","iat":1422779638}'.encode()
    header = json.dumps({
        "alg": "HS256",
        "typ": "JWT"
    }).encode()
    #header = '{"alg":"HS256","typ":"JWT"}'.encode()
    secret = b'secretkey'
    payload64 = base64.urlsafe_b64encode(payload)
    header64 = base64.urlsafe_b64encode(header)
    signature = hmac.new(secret, header64+b'.'+payload64, sha256).digest()
    signature64 = base64.urlsafe_b64encode(signature)
    token = header64+b'.'+payload64+b'.'+signature64
    token = token.decode()
    assert token == 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJsb2dnZWRJbkFzIjogImFkbWluIiwgImlhdCI6IDE0MjI3Nzk2Mzh9.5q7_W0yEwPe6-0eMAIbWDfWxh7ZBt5U0Fr4L23eTq3Q='

    token = gen_auth_token('John')
    print(validate_auth_token(token))
