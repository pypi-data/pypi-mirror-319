import os
from pathlib import Path
from cryptography.fernet import Fernet
from src.clipthread.core.crypto import CryptoUtils


class TestCryptoUtils:
    def setup_method(self):
        self.test_key_path = ".test_key"
        # Clean up before each test
        if os.path.exists(self.test_key_path):
            os.remove(self.test_key_path)

    def teardown_method(self):
        # Clean up after each test
        if os.path.exists(self.test_key_path):
            os.remove(self.test_key_path)

    def test_initialize_fernet_creates_new_key(self):
        crypto = CryptoUtils(self.test_key_path)
        
        # Verify key file was created
        assert Path(self.test_key_path).exists()
        
        # Verify Fernet instance was created correctly
        assert isinstance(crypto.fernet, Fernet)
        
        # Verify key file contains valid Fernet key
        saved_key = Path(self.test_key_path).read_bytes()
        test_fernet = Fernet(saved_key)
        assert isinstance(test_fernet, Fernet)

    def test_initialize_fernet_uses_existing_key(self):
        # Create first instance to generate key
        crypto1 = CryptoUtils(self.test_key_path)
        original_key = Path(self.test_key_path).read_bytes()
        
        # Create second instance that should use existing key
        crypto2 = CryptoUtils(self.test_key_path)
        loaded_key = Path(self.test_key_path).read_bytes()
        
        # Verify both instances use same key
        assert original_key == loaded_key
        assert crypto1.fernet.encrypt(b'test') != crypto2.fernet.encrypt(b'test')  # Encryptions should differ due to random IV
        
        # But decryption should work between instances
        test_data = b'test message'
        encrypted = crypto1.fernet.encrypt(test_data)
        decrypted = crypto2.fernet.decrypt(encrypted)
        assert decrypted == test_data

    def test_encrypt_decrypt(self):
        crypto = CryptoUtils(self.test_key_path)
        test_data = "test message"
        encrypted = crypto.encrypt(test_data)
        decrypted = crypto.decrypt(encrypted)
        assert decrypted == test_data