import jwt
import secrets
import time
from pathlib import Path

jwt_secret_file = Path("data/jwt_secret")
jwt_secret = secrets.token_urlsafe(128)
if jwt_secret_file.is_file():
    with open(jwt_secret_file) as f:
        jwt_secret = f.read()
else:
    with open(jwt_secret_file, "w") as f:
        f.write(jwt_secret)

def gen_jwt(user: str, password: str, expire_hours: float = 8) -> str:
    expire_time = int(time.time() + expire_hours * 60 * 60)
    token = jwt.encode({"exp": expire_time, "user": user}, jwt_secret, algorithm="HS256")
    return token

def decode_jwt(token: str) -> dict | None:
    res = None
    try:
        res = jwt.decode(token, jwt_secret, algorithms=["HS256"])
    except (
        jwt.exceptions.InvalidTokenError, 
        jwt.exceptions.DecodeError, 
        jwt.exceptions.InvalidSignatureError, 
        jwt.exceptions.ExpiredSignatureError,
    ) as e:
        print(f"Error decoding jwt: {e}")
    return res

# token = gen_jwt("root", "admin")
# print(token)
# print(decode_jwt(token))
# time.sleep(2.5)
# print(decode_jwt(token))