import base64
import hashlib
import json
import platform
import socket
import uuid
from getpass import getpass

from cryptography.fernet import Fernet


def generate_key(user_key: str = None, from_system: bool = True):
    if from_system:
        if user_key is None:
            user_key = ""
        system_name = platform.system()
        hostname = socket.gethostname()
        architecture = platform.machine()
        mac_address = str(uuid.getnode())
        system_info = f"{user_key}{system_name}{hostname}{mac_address}{architecture}"
        hashed_info = hashlib.sha256(system_info.encode()).digest()
        key = base64.urlsafe_b64encode(hashed_info[:32])
    else:
        key = Fernet.generate_key()
    return key


def pass_account() -> dict:
    username = input("Username: ")
    password = getpass()
    return {"username": username, "password": password}


def encrypt(content: str | bytes | dict, key: str = None) -> bytes:
    if content is None:
        content = {}
    if isinstance(content, dict):
        content = json.dumps(content)
    if isinstance(content, str):
        content = content.encode()
    if key is None:
        key = generate_key()
    cipher = Fernet(key)
    return cipher.encrypt(content)


def decrypt(content: str | bytes, key: str = None, to_dict: bool = False) -> bytes | dict:
    if isinstance(content, str):
        content = content.encode()
    if key is None:
        key = generate_key()
    cipher = Fernet(key)
    decrypted_content = cipher.decrypt(content)
    if to_dict:
        decrypted_content = json.loads(decrypted_content)
    return decrypted_content


def save(content: str | bytes | dict, file: str, key: str = None) -> bytes:
    if file is None:
        file = "./account.key"
    encrypted_content = encrypt(content=content, key=key)
    with open(file, "wb") as f:
        f.write(encrypted_content)
    return encrypted_content


def load(file: str = None, key: str = None, to_dict: dict = True) -> bytes | dict:
    if file is None:
        file = "./account.key"
    with open(file, "rb") as f:
        content = f.read()
    decrypted_content = decrypt(content, key=key, to_dict=to_dict)
    return decrypted_content
