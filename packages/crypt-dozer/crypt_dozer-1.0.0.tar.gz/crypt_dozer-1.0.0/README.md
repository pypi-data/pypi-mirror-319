# CryptDozer

`CryptDozer` is a simple package for encrypting and decrypting data using the `cryptography` library. It supports symmetric encryption with Fernet.

## Installation

To install the package, use the following:

```bash
pip install crypt_dozer
```

## Usage

```python

from crypt_dozer import CryptDozer

# Initialize with a new key (or use an existing key)
crypto = CryptDozer()

# Encrypt data
encrypted = crypto.encrypt("Hello, world!")
print("Encrypted:", encrypted)

# Decrypt data
decrypted = crypto.decrypt(encrypted)
print("Decrypted:", decrypted)
```