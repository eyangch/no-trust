import sqlite3
import hashlib
import secrets
import json
from pathlib import Path

con = sqlite3.connect("data/data.db")
con.row_factory = sqlite3.Row

cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS ports(proxy_port PRIMARY KEY, hidden_port)")
cur.execute("CREATE TABLE IF NOT EXISTS accounts(user PRIMARY KEY, pass_hash, salt, proxy_access)")

PBKDF2_ITERS = 100000

def hash_pass(password: str) -> tuple[str, str]:
    salt: str = secrets.token_urlsafe(16)
    pass_hash: str = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), PBKDF2_ITERS).hex()
    return (salt, pass_hash)

def compare_pass(password: str, pass_hash: str, salt: str) -> bool:
    new_hash: str = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), PBKDF2_ITERS).hex()
    return secrets.compare_digest(new_hash, pass_hash)

def get_user(user: str):
    return cur.execute("SELECT * FROM accounts WHERE user = ?", (user, )).fetchone()

def create_user(user: str, password: str, proxy_access: list = [], check_dup: bool = True) -> bool:
    if check_dup:
        existing_user = get_user(user)
        if existing_user is not None:
            return False
    salt: str
    pass_hash: str
    salt, pass_hash = hash_pass(password)
    cur.execute(
        "INSERT OR REPLACE INTO accounts VALUES(?, ?, ?, ?)", 
        (user, pass_hash, salt, json.dumps(proxy_access, separators=(',', ':')))
    )
    con.commit()
    return True

def update_password(user: str, new_password: str) -> bool:
    existing_user = get_user(user)
    if existing_user is None:
        return False
    salt: str
    pass_hash: str
    salt, pass_hash = hash_pass(new_password)
    cur.execute(
        "UPDATE accounts SET pass_hash = ?, salt = ? WHERE user = ?",
        (pass_hash, salt, user)
    )
    con.commit()
    return True

def add_port_to_user(user: str, port: int) -> bool:
    existing_user = get_user(user)
    if existing_user is None:
        return False
    proxy_access = json.loads(existing_user["proxy_access"])
    if port in proxy_access:
        return False
    proxy_access.append(port)
    cur.execute(
        "UPDATE accounts SET proxy_access = ? WHERE user = ?",
        (json.dumps(proxy_access, separators=(',', ':')), user)
    )
    con.commit()
    return True

def authenticate_user(user: str, password: str):
    existing_user = get_user(user)
    if existing_user is None:
        return False
    salt: str = existing_user["salt"]
    pass_hash: str = existing_user["pass_hash"]
    return compare_pass(
        password=password,
        pass_hash=pass_hash,
        salt=salt
    )

def get_port(proxy_port: int):
    return cur.execute("SELECT * FROM ports WHERE proxy_port = ?", (proxy_port, )).fetchone()

def get_all_ports(user: str):
    existing_user = get_user(user)
    if existing_user is None:
        return []
    proxy_access = json.loads(existing_user["proxy_access"])
    return [x for x in cur.execute("SELECT * FROM ports").fetchall() if x["proxy_port"] in proxy_access]

def add_port(proxy_port: int, hidden_port: int, check_dup: bool = True):
    if check_dup:
        existing_port = get_port(proxy_port)
        if existing_port is not None:
            return False
    cur.execute(
        "INSERT OR REPLACE INTO ports VALUES(?, ?)", 
        (proxy_port, hidden_port)
    )
    con.commit()
    add_port_to_user("root", proxy_port)
    return True

create_user("root", "admin")