import base64
import hashlib
from cryptography.fernet import Fernet
from django.conf import settings

def get_fernet():
    # Derive a 32-byte key from Django's SECRET_KEY
    key_hash = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    fernet_key = base64.urlsafe_b64encode(key_hash)
    return Fernet(fernet_key)

def encrypt_contact_detail(plain_text: str) -> str:
    fernet = get_fernet()
    return fernet.encrypt(plain_text.encode()).decode()

def decrypt_contact_detail(encrypted_text: str) -> str:
    fernet = get_fernet()
    return fernet.decrypt(encrypted_text.encode()).decode()
