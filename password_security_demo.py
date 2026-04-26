```python
"""
Educational Password Brute Force Tool
======================================
This script demonstrates password brute-forcing techniques for educational purposes only.
It should ONLY be used on systems you own or have explicit permission to test.

WARNING: Unauthorized access to computer systems is illegal.
This tool is for learning about password security.
"""

import hashlib
import itertools
import string
import time
from typing import List, Optional, Callable
import argparse


class PasswordBruteForcer:
    """
    Educational brute force password cracker that demonstrates
    various password cracking techniques.
    """
    
    def __init__(self, target_hash: str, hash_algorithm: str = 'sha256'):
        """
        Initialize the brute forcer with a target password hash.
        
        Args:
            target_hash: The hashed password to crack
            hash_algorithm: Hash algorithm used (md5, sha1, sha256, etc.)
        """
        self.target_hash = target_hash.lower()
        self.hash_algorithm = hash_algorithm
        self.attempts = 0
        self.start_time = None
        
    def _hash_password(self, password: str) -> str:
        """
        Hash a password using the specified algorithm.
        
        Args:
            password: Plain text password to hash
            
        Returns:
            Hexadecimal hash string
        """
        hash_object = hashlib.new(self.hash_algorithm)
        hash_object.update(password.encode('utf-8'))
        return hash_object.hexdigest()
    
    def _check_password(self, password: str) -> bool:
        """
        Check if a password matches the target hash.
        
        Args:
            password: Password to test
            
        Returns:
            True if password matches, False otherwise
        """
        self.attempts += 1
        return self._hash_password(password) == self.target_hash
    
    def dictionary_attack(self, wordlist_path: str) -> Optional[str]:
        """
        Perform a dictionary attack using a wordlist file.
        
        Args:
            wordlist_path: Path to the wordlist file
            
        Returns:
            The cracked password or None if not found
        """
        print(f"\n[*] Starting dictionary attack with {wordlist_path}")
        print(f"[*] Target hash: {self.target_hash}")
        print(f"[*] Hash algorithm: {self.hash_algorithm}\n")
        
        self.start_time = time.time()
        self.attempts = 0
        
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line_num, line in enumerate(file, 1):
                    password = line.strip()
                    
                    if self._check_password(password):
                        elapsed_time = time.time() - self.start_time
                        print(f"\n[+] PASSWORD FOUND: {password}")
                        print(f"[+] Attempts: {self.attempts}")
                        print(f"[+] Time elapsed: {elapsed_time:.2f} seconds")
                        return password
                    
                    # Progress indicator every 10000 attempts
                    if self.attempts % 10000 == 0:
                        elapsed = time.time() - self.start_time
                        rate = self.attempts / elapsed if elapsed > 0 else 0
                        print(f"[*] Tried {self.attempts} passwords ({rate:.0f} passwords/sec)", end='\r')
            
            print(f"\n[-] Password not found in dictionary after {self.attempts} attempts")
            return None
            
        except FileNotFoundError:
            print(f"[-] Error: Wordlist file '{wordlist_path}' not found")
            return None
    
    def brute_force_attack(self, 
                          charset: str = string.ascii_lowercase, 
                          min_length: int = 1, 
                          max_length: int = 4) -> Optional[str]:
        """
        Perform a brute force attack trying all combinations.
        
        Args:
            charset: Character set to use for brute forcing
            min_length: Minimum password length to try
            max_length: Maximum password length to try
            
        Returns:
            The cracked password or None if not found
        """
        print(f"\n[*] Starting brute force attack")
        print(f"[*] Target hash: {self.target_hash}")
        print(f"[*] Charset: {charset}")
        print(f"[*] Length range: {min_length}-{max_length}")
        print(f"[*] Hash algorithm: {self.hash_algorithm}\n")
        
        self.start_time = time.time()
        self.attempts = 0
        
        for length in range(min_length, max_length + 1):
            print(f"[*] Trying passwords of length {length}")
            
            for attempt in itertools.product(charset, repeat=length):
                password = ''.join(attempt)
                
                if self._check_password(password):
                    elapsed_time = time.time() - self.start_time
                    print(f"\n[+] PASSWORD FOUND: {password}")
                    print(f"[+] Attempts: {self.attempts}")
                    print(f"[+] Time elapsed: {elapsed_time:.2f} seconds")
                    return password
                
                # Progress indicator every 50000 attempts
                if self.attempts % 50000 == 0:
                    elapsed = time.time() - self.start_time
                    rate = self.attempts / elapsed if elapsed > 0 else 0
                    print(f"[*] Tried {self.attempts} passwords ({rate:.0f} passwords/sec)", end='\r')
        
        print(f"\n[-] Password not found after {self.attempts} attempts")
        return None
    
    def hybrid_attack(self, 
                     wordlist_path: str, 
                     append_digits: bool = True,
                     append_special: bool = True) -> Optional[str]:
        """
        Perform a hybrid attack: dictionary + common modifications.
        
        Args:
            wordlist_path: Path to the wordlist file
            append_digits: Try appending digits (0-99)
            append_special: Try appending special characters
            
        Returns:
            The cracked password or None if not found
        """
        print(f"\n[*] Starting hybrid attack")
        print(f"[*] Target hash: {self.target_hash}")
        print(f"[*] Wordlist: {wordlist_path}")
        print(f"[*] Hash algorithm: {self.hash_algorithm}\n")
        
        self.start_time = time.time()
        self.attempts = 0
        
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
                words = [line.strip() for line in file]
        except FileNotFoundError:
            print(f"[-] Error: Wordlist file '{wordlist_path}' not found")
            return None
        
        for word in words:
            # Try original word
            variations = [word]
            
            # Try capitalized versions
            variations.append(word.capitalize())
            variations.append(word.upper())
            
            # Try with appended digits
            if append_digits:
                for i in range(100):
                    variations.append(f"{word}{i}")
                    variations.append(f"{word.capitalize()}{i}")
            
            # Try with appended special characters
            if append_special:
                for char in "!@#$":
                    variations.append(f"{word}{char}")
                    variations.append(f"{word.capitalize()}{char}")
            
            for password in variations:
                if self._check_password(password):
                    elapsed_time = time.time() - self.start_time
                    print(f"\n[+] PASSWORD FOUND: {password}")
                    print(f"[+] Attempts: {self.attempts}")
                    print(f"[+] Time elapsed: {elapsed_time:.2f} seconds")
                    return password
            
            # Progress indicator
            if self.attempts % 10000 == 0:
                elapsed = time.time() - self.start_time
                rate = self.attempts / elapsed if elapsed > 0 else 0
                print(f"[*] Tried {self.attempts} passwords ({rate:.0f} passwords/sec)", end='\r')
        
        print(f"\n[-] Password not found after {self.attempts} attempts")
        return None


def create_sample_wordlist(filename: str = 'sample_wordlist.txt'):
    """
    Create a sample wordlist for demonstration purposes.
    
    Args:
        filename: Name of the wordlist file to create
    """
    common_passwords = [
        'password', '123456', '12345678', 'qwerty', 'abc123',
        'monkey', '1234567', 'letmein', 'trustno1', 'dragon',
        'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
        'bailey', 'passw0rd', 'shadow', '123123', '654321',
        'superman', 'qazwsx', 'michael', 'football', 'admin',
        'welcome', 'login', 'password1', 'test', 'demo'
    ]
    
    with open(filename, 'w') as f:
        for password in common_passwords:
            f.write(f"{password}\n")
    
    print(f"[+] Sample wordlist created: {filename}")


def demonstrate_password_cracking():
    """
    Demonstration function showing different cracking techniques.
    """
    print("=" * 70)
    print("EDUCATIONAL PASSWORD CRACKING DEMONSTRATION")
    print("=" * 70)
    print("\nWARNING: This tool is for educational purposes only!")
    print("Only use on systems you own or have permission to test.\n")
    
    # Create sample wordlist if it doesn't exist
    create_sample_wordlist()
    
    # Example 1: Dictionary Attack
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Dictionary Attack")
    print("=" * 70)
    
    # Create a test password hash
    test_password = "password123"
    test_hash = hashlib.sha256(test_password.encode()).hexdigest()
    
    print(f"\n[*] Test password (hidden in real scenario): {test_password}")
    print(f"[*] SHA256 hash to crack: {test_hash}")
    
    cracker = PasswordBruteForcer(test_hash, 'sha256')
    result = cracker.dictionary_attack('sample_wordlist.txt')
    
    # Example 2: Brute Force Attack (short password)
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Brute Force Attack (Numeric PIN)")
    print("=" * 70)
    
    test_pin = "1337"
    test_hash_pin = hashlib.sha256(test_pin.encode()).hexdigest()
    
    print(f"\n[*] Test PIN (hidden in real scenario): {test_pin}")
    print(f"[*] SHA256 hash to crack: {test_hash_pin}")
    
    cracker_pin = PasswordBruteForcer(test_hash_pin, 'sha256')
    result_pin = cracker_pin.brute_force_attack(charset=string.digits, min_length=4, max_length=4)
    
    # Example 3: Hybrid Attack
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Hybrid Attack")
    print("=" * 70)
    
    test_password_hybrid = "Password1"
    test_hash_hybrid = hashlib.sha256(test_password_hybrid.encode()).hexdigest()
    
    print(f"\n[*] Test password (hidden in real scenario): {test_password_hybrid}")
    print(f"[*] SHA256 hash to crack: {test_hash_hybrid}")
    
    cracker_hybrid = PasswordBruteForcer(test_hash_hybrid, 'sha256')
    result_hybrid = cracker_hybrid.hybrid_attack('sample_wordlist.txt')
    
    # Security Recommendations
    print("\n" + "=" * 70)
    print("PASSWORD SECURITY RECOMMENDATIONS")
    print("=" * 70)
    print("""
1. Use long passwords (12+ characters)
2. Use a mix of uppercase, lowercase, numbers, and special characters
3. Avoid common words and patterns
4. Use unique passwords for each account
5. Use a password manager
6. Enable two-factor authentication (2FA)
7. Use password hashing with salt (bcrypt, scrypt, Argon2)
8. Never store passwords in plain text
    """)


def main():
    """
    Main function with command-line interface.
    """
    parser = argparse.ArgumentParser(
        description='Educational Password Brute Force Tool',
        epilog='WARNING: Use only on systems you own or have permission to test!'
    )
    
    parser.add_argument('-t', '--target-hash', 
                       help='Target password hash to crack')
    parser.add_argument('-a', '--algorithm', 
                       default='sha256',
                       choices=['md5', 'sha1', 'sha256', 'sha512'],
                       help='Hash algorithm used (default: sha256)')
    parser.add_argument('-m', '--mode',
                       choices=['dictionary', 'brute', 'hybrid', 'demo'],
                       default='demo',
                       help='Attack mode (default: demo)')
    parser.add_argument('-w', '--wordlist',
                       default='sample_wordlist.txt',
                       help='Path to wordlist file')
    parser.add_argument('-c', '--charset',
                       default=string.ascii_lowercase,
                       help='Character set for brute force')
    parser.add_argument('--min-length',
                       type=int,
                       default=1,
                       help='Minimum password length for brute force')
    parser.add_argument('--max-length',
                       type=int,
                       default=4,
                       help='Maximum password length for brute force')
    
    args = parser.parse_args()
    
    if args.mode == 'demo':
        demonstrate_password_cracking()
    else:
        if not args.target_hash:
            print("[-] Error: Target hash required for non-demo modes")
            print("[-] Use --target-hash to specify the hash to crack")
            return
        
        cracker = PasswordBruteForcer(args.target_hash, args.algorithm)
        
        if args.mode == 'dictionary':
            cracker.dictionary_attack(args.wordlist)
        elif args.mode == 'brute':
            cracker.brute_force_attack(args.charset, args.min_length, args.max_length)
        elif args.mode == 'hybrid':
            cracker.hybrid_attack(args.wordlist)


if __name__ == "__main__":
    main()
```
