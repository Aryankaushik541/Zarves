#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS Code Encryption System
Encrypts all Python files to protect source code
Only authorized users can decrypt and run
"""

import os
import sys
from pathlib import Path
from cryptography.fernet import Fernet
import base64
import hashlib


class CodeEncryptor:
    """Encrypt/Decrypt Python source code"""
    
    def __init__(self, password: str = None):
        """
        Initialize encryptor with password
        
        Args:
            password: Master password for encryption/decryption
        """
        if password:
            # Generate key from password
            self.key = self._generate_key_from_password(password)
        else:
            # Generate random key
            self.key = Fernet.generate_key()
        
        self.cipher = Fernet(self.key)
    
    def _generate_key_from_password(self, password: str) -> bytes:
        """Generate Fernet key from password"""
        # Use SHA256 to hash password
        password_bytes = password.encode()
        hash_obj = hashlib.sha256(password_bytes)
        key = base64.urlsafe_b64encode(hash_obj.digest())
        return key
    
    def encrypt_file(self, file_path: str) -> bool:
        """
        Encrypt a Python file
        
        Args:
            file_path: Path to file to encrypt
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read original file
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Encrypt data
            encrypted_data = self.cipher.encrypt(file_data)
            
            # Write encrypted file
            encrypted_path = file_path + '.encrypted'
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)
            
            print(f"✅ Encrypted: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to encrypt {file_path}: {e}")
            return False
    
    def decrypt_file(self, encrypted_path: str, output_path: str = None) -> bool:
        """
        Decrypt an encrypted file
        
        Args:
            encrypted_path: Path to encrypted file
            output_path: Where to save decrypted file (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read encrypted file
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt data
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Determine output path
            if not output_path:
                output_path = encrypted_path.replace('.encrypted', '')
            
            # Write decrypted file
            with open(output_path, 'wb') as f:
                f.write(decrypted_data)
            
            print(f"✅ Decrypted: {encrypted_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to decrypt {encrypted_path}: {e}")
            return False
    
    def encrypt_directory(self, directory: str, extensions: list = ['.py']) -> dict:
        """
        Encrypt all files in directory with given extensions
        
        Args:
            directory: Directory to encrypt
            extensions: File extensions to encrypt (default: ['.py'])
            
        Returns:
            Dictionary with success/failure counts
        """
        results = {'success': 0, 'failed': 0, 'skipped': 0}
        
        # Walk through directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Check extension
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    
                    # Skip already encrypted files
                    if file.endswith('.encrypted'):
                        results['skipped'] += 1
                        continue
                    
                    # Skip this encryption script
                    if 'encrypt_code.py' in file_path:
                        results['skipped'] += 1
                        continue
                    
                    # Encrypt file
                    if self.encrypt_file(file_path):
                        results['success'] += 1
                    else:
                        results['failed'] += 1
        
        return results
    
    def decrypt_directory(self, directory: str) -> dict:
        """
        Decrypt all .encrypted files in directory
        
        Args:
            directory: Directory to decrypt
            
        Returns:
            Dictionary with success/failure counts
        """
        results = {'success': 0, 'failed': 0}
        
        # Walk through directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.encrypted'):
                    encrypted_path = os.path.join(root, file)
                    
                    # Decrypt file
                    if self.decrypt_file(encrypted_path):
                        results['success'] += 1
                    else:
                        results['failed'] += 1
        
        return results
    
    def save_key(self, key_file: str = 'encryption.key'):
        """Save encryption key to file"""
        try:
            with open(key_file, 'wb') as f:
                f.write(self.key)
            print(f"✅ Key saved to: {key_file}")
            print(f"⚠️  KEEP THIS FILE SAFE! You need it to decrypt files.")
            return True
        except Exception as e:
            print(f"❌ Failed to save key: {e}")
            return False
    
    @staticmethod
    def load_key(key_file: str = 'encryption.key') -> 'CodeEncryptor':
        """Load encryption key from file"""
        try:
            with open(key_file, 'rb') as f:
                key = f.read()
            encryptor = CodeEncryptor()
            encryptor.key = key
            encryptor.cipher = Fernet(key)
            print(f"✅ Key loaded from: {key_file}")
            return encryptor
        except Exception as e:
            print(f"❌ Failed to load key: {e}")
            return None


def main():
    """Main encryption/decryption interface"""
    print("\n" + "="*70)
    print("🔒 JARVIS Code Encryption System")
    print("="*70)
    print()
    
    # Menu
    print("Choose an option:")
    print("1. Encrypt all code (with password)")
    print("2. Decrypt all code (with password)")
    print("3. Encrypt all code (with random key)")
    print("4. Decrypt all code (with key file)")
    print()
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        # Encrypt with password
        print()
        password = input("Enter master password: ").strip()
        
        if not password:
            print("❌ Password cannot be empty!")
            return
        
        print()
        print("🔒 Encrypting all Python files...")
        print()
        
        encryptor = CodeEncryptor(password)
        
        # Encrypt skill directory
        results = encryptor.encrypt_directory('skill')
        
        print()
        print("="*70)
        print("📊 Encryption Results:")
        print("="*70)
        print(f"✅ Success: {results['success']} files")
        print(f"❌ Failed: {results['failed']} files")
        print(f"⏭️  Skipped: {results['skipped']} files")
        print()
        print("💡 To decrypt, use the same password")
        print("="*70)
    
    elif choice == "2":
        # Decrypt with password
        print()
        password = input("Enter master password: ").strip()
        
        if not password:
            print("❌ Password cannot be empty!")
            return
        
        print()
        print("🔓 Decrypting all encrypted files...")
        print()
        
        encryptor = CodeEncryptor(password)
        
        # Decrypt skill directory
        results = encryptor.decrypt_directory('skill')
        
        print()
        print("="*70)
        print("📊 Decryption Results:")
        print("="*70)
        print(f"✅ Success: {results['success']} files")
        print(f"❌ Failed: {results['failed']} files")
        print()
        print("="*70)
    
    elif choice == "3":
        # Encrypt with random key
        print()
        print("🔒 Encrypting all Python files with random key...")
        print()
        
        encryptor = CodeEncryptor()
        
        # Encrypt skill directory
        results = encryptor.encrypt_directory('skill')
        
        # Save key
        encryptor.save_key()
        
        print()
        print("="*70)
        print("📊 Encryption Results:")
        print("="*70)
        print(f"✅ Success: {results['success']} files")
        print(f"❌ Failed: {results['failed']} files")
        print(f"⏭️  Skipped: {results['skipped']} files")
        print()
        print("💡 Key saved to: encryption.key")
        print("⚠️  KEEP THIS FILE SAFE!")
        print("="*70)
    
    elif choice == "4":
        # Decrypt with key file
        print()
        key_file = input("Enter key file path (default: encryption.key): ").strip()
        
        if not key_file:
            key_file = 'encryption.key'
        
        print()
        print("🔓 Decrypting all encrypted files...")
        print()
        
        encryptor = CodeEncryptor.load_key(key_file)
        
        if not encryptor:
            print("❌ Failed to load key file!")
            return
        
        # Decrypt skill directory
        results = encryptor.decrypt_directory('skill')
        
        print()
        print("="*70)
        print("📊 Decryption Results:")
        print("="*70)
        print(f"✅ Success: {results['success']} files")
        print(f"❌ Failed: {results['failed']} files")
        print()
        print("="*70)
    
    else:
        print("❌ Invalid choice!")


if __name__ == "__main__":
    # Check if cryptography is installed
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        print("❌ cryptography library not installed!")
        print()
        print("📦 Installing cryptography...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
        print()
        print("✅ Installed! Please run this script again.")
        sys.exit(0)
    
    main()
