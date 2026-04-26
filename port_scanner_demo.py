"""
Simple Educational Port Scanner
This script demonstrates basic port scanning techniques for educational purposes.
It scans a range of ports on a target host to check which ones are open.
WARNING: Only scan systems you own or have explicit permission to test.
"""

import socket
import sys
from datetime import datetime


def scan_port(target_ip, port, timeout=1):
    """
    Attempts to connect to a specific port on the target IP.
    
    Args:
        target_ip (str): IP address or hostname to scan
        port (int): Port number to check
        timeout (float): Connection timeout in seconds
    
    Returns:
        bool: True if port is open, False otherwise
    """
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # Attempt to connect to the port
        result = sock.connect_ex((target_ip, port))
        sock.close()
        
        # Return True if connection successful (port is open)
        return result == 0
    except socket.gaierror:
        print(f"Hostname could not be resolved: {target_ip}")
        return False
    except socket.error:
        print(f"Could not connect to server: {target_ip}")
        return False


def get_service_name(port):
    """
    Returns the common service name for well-known ports.
    
    Args:
        port (int): Port number
    
    Returns:
        str: Service name or "Unknown"
    """
    common_ports = {
        20: "FTP Data",
        21: "FTP Control",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        8080: "HTTP Proxy",
        8443: "HTTPS Alt"
    }
    return common_ports.get(port, "Unknown")


def scan_range(target_ip, start_port, end_port):
    """
    Scans a range of ports on the target host.
    
    Args:
        target_ip (str): Target IP address or hostname
        start_port (int): Starting port number
        end_port (int): Ending port number
    """
    print("\n" + "="*60)
    print(f"Port Scanner - Educational Tool")
    print("="*60)
    print(f"Target: {target_ip}")
    print(f"Port Range: {start_port} - {end_port}")
    print(f"Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    open_ports = []
    
    # Scan each port in the range
    for port in range(start_port, end_port + 1):
        print(f"Scanning port {port}...", end="\r")
        
        if scan_port(target_ip, port):
            service = get_service_name(port)
            print(f"[+] Port {port} is OPEN - Service: {service}")
            open_ports.append((port, service))
    
    # Display summary
    print("\n" + "="*60)
    print("Scan Complete!")
    print(f"Scan finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    if open_ports:
        print(f"\nFound {len(open_ports)} open port(s):")
        for port, service in open_ports:
            print(f"  - Port {port}: {service}")
    else:
        print("\nNo open ports found in the specified range.")
    
    print("\n")


def main():
    """
    Main function to handle user input and initiate the scan.
    """
    print("="*60)
    print("Simple Educational Port Scanner")
    print("WARNING: Only scan systems you own or have permission to test")
    print("="*60 + "\n")
    
    # Get target from user
    target = input("Enter target IP or hostname (e.g., localhost, 127.0.0.1): ").strip()
    
    if not target:
        print("Error: Target cannot be empty!")
        sys.exit(1)
    
    # Resolve hostname to IP
    try:
        target_ip = socket.gethostbyname(target)
        print(f"Resolved {target} to {target_ip}")
    except socket.gaierror:
        print(f"Error: Could not resolve hostname {target}")
        sys.exit(1)
    
    # Get port range from user
    try:
        start_port = int(input("Enter starting port (e.g., 1): ").strip())
        end_port = int(input("Enter ending port (e.g., 1024): ").strip())
        
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            print("Error: Invalid port range! Ports must be between 1-65535.")
            sys.exit(1)
            
    except ValueError:
        print("Error: Ports must be numeric values!")
        sys.exit(1)
    
    # Perform the scan
    try:
        scan_range(target_ip, start_port, end_port)
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
