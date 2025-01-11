from cryptography.fernet import Fernet
from pathlib import Path
import base64

class CryptoUtils:
    def __init__(self, key_path: str = ".key"):
        self.key_path = Path(key_path)
        self.fernet = self._initialize_fernet()

    def _initialize_fernet(self) -> Fernet:
        """Initialize Fernet with existing key or generate new one"""
        if self.key_path.exists():
            key = self.key_path.read_bytes()
        else:
            key = Fernet.generate_key()
            self.key_path.write_bytes(key)
        return Fernet(key)

    def encrypt(self, data: str) -> str:
        """Encrypt string data and return base64 encoded string"""
        encrypted_bytes = self.fernet.encrypt(data.encode())
        return base64.b64encode(encrypted_bytes).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt base64 encoded encrypted string"""
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            decrypted_bytes = self.fernet.decrypt(encrypted_bytes)
            return decrypted_bytes.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {str(e)}")

    def rotate_key(self):
        """Generate new key and re-encrypt existing data"""
        new_key = Fernet.generate_key()
        self.key_path.write_bytes(new_key)
        self.fernet = Fernet(new_key)