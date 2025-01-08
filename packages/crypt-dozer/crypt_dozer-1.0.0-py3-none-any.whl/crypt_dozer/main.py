from cryptography.fernet import Fernet


class CryptDozer:
    def __init__(self, key: bytes = None):
        # Generate a new key if not provided
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key
        self.fernet = Fernet(self.key)

    def encrypt(self, data: str) -> str:
        """
        Encrypts a string using the Fernet encryption system.

        Args:
            data (str): The data to encrypt.

        Returns:
            str: The encrypted data.
        """
        data_bytes = data.encode()  # Convert string to bytes
        encrypted_data = self.fernet.encrypt(data_bytes)
        return encrypted_data.decode()  # Return as string

    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypts a string that was encrypted using the Fernet encryption system.

        Args:
            encrypted_data (str): The encrypted data.

        Returns:
            str: The decrypted data.
        """
        encrypted_data_bytes = encrypted_data.encode()  # Convert string to bytes
        decrypted_data = self.fernet.decrypt(encrypted_data_bytes)
        return decrypted_data.decode()  # Return as string
