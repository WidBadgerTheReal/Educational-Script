"""
Educational Network Sniffer
A basic packet sniffer for learning purposes - demonstrates network traffic capture and analysis
WARNING: Use only on networks you own or have explicit permission to monitor
"""

import socket
import struct
import textwrap
import sys

# Network packet constants
ETH_HEADER_LEN = 14
IPV4_HEADER_MIN_LEN = 20
TCP_HEADER_MIN_LEN = 20
UDP_HEADER_LEN = 8

def main():
    """Main function to start packet sniffing"""
    print("=" * 70)
    print("EDUCATIONAL NETWORK SNIFFER")
    print("=" * 70)
    print("WARNING: Use only on authorized networks")
    print("Press Ctrl+C to stop\n")
    
    # Create raw socket to capture all packets
    # Note: Requires administrator/root privileges
    try:
        # For Linux
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    except AttributeError:
        # For Windows (requires WinPcap/Npcap)
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
            conn.bind((get_local_ip(), 0))
            conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        except Exception as e:
            print(f"Error creating socket: {e}")
            print("Try running as administrator/root")
            sys.exit(1)
    
    packet_count = 0
    
    try:
        while True:
            # Receive packet data
            raw_data, addr = conn.recvfrom(65535)
            packet_count += 1
            
            print(f"\n{'=' * 70}")
            print(f"PACKET #{packet_count}")
            print(f"{'=' * 70}")
            
            # Parse Ethernet frame
            eth_header = parse_ethernet_frame(raw_data)
            print(format_ethernet_header(eth_header))
            
            # Check if IPv4 packet
            if eth_header['protocol'] == 8:  # IPv4
                ipv4_header = parse_ipv4_packet(raw_data[ETH_HEADER_LEN:])
                print(format_ipv4_header(ipv4_header))
                
                # Parse transport layer protocols
                ip_header_len = (ipv4_header['version_ihl'] & 0xF) * 4
                data_offset = ETH_HEADER_LEN + ip_header_len
                
                # TCP Protocol
                if ipv4_header['protocol'] == 6:
                    tcp_header = parse_tcp_segment(raw_data[data_offset:])
                    print(format_tcp_header(tcp_header))
                    
                    # Extract payload
                    tcp_header_len = (tcp_header['offset_reserved'] >> 4) * 4
                    payload_offset = data_offset + tcp_header_len
                    payload = raw_data[payload_offset:]
                    
                    if payload:
                        print("\n[PAYLOAD DATA]")
                        print(format_payload(payload))
                
                # UDP Protocol
                elif ipv4_header['protocol'] == 17:
                    udp_header = parse_udp_segment(raw_data[data_offset:])
                    print(format_udp_header(udp_header))
                    
                    # Extract payload
                    payload_offset = data_offset + UDP_HEADER_LEN
                    payload = raw_data[payload_offset:]
                    
                    if payload:
                        print("\n[PAYLOAD DATA]")
                        print(format_payload(payload))
                
                # ICMP Protocol
                elif ipv4_header['protocol'] == 1:
                    icmp_header = parse_icmp_packet(raw_data[data_offset:])
                    print(format_icmp_header(icmp_header))
                
                # Other protocols
                else:
                    print(f"\n[OTHER PROTOCOL: {ipv4_header['protocol']}]")
            
    except KeyboardInterrupt:
        print(f"\n\n{'=' * 70}")
        print(f"Sniffing stopped. Total packets captured: {packet_count}")
        print(f"{'=' * 70}")
        sys.exit(0)


# ==================== ETHERNET LAYER PARSING ====================

def parse_ethernet_frame(data):
    """Parse Ethernet frame header"""
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:ETH_HEADER_LEN])
    return {
        'dest_mac': format_mac_address(dest_mac),
        'src_mac': format_mac_address(src_mac),
        'protocol': proto
    }

def format_mac_address(bytes_addr):
    """Format MAC address to readable string"""
    return ':'.join(map('{:02x}'.format, bytes_addr)).upper()

def format_ethernet_header(header):
    """Format Ethernet header for display"""
    protocol_name = {
        8: 'IPv4',
        1544: 'ARP',
        56710: 'IPv6'
    }.get(header['protocol'], f"Unknown (0x{header['protocol']:04x})")
    
    return f"""
[ETHERNET FRAME]
    Destination MAC: {header['dest_mac']}
    Source MAC:      {header['src_mac']}
    Protocol:        {protocol_name}"""


# ==================== IPv4 LAYER PARSING ====================

def parse_ipv4_packet(data):
    """Parse IPv4 packet header"""
    version_ihl, tos, total_length, identification, flags_fragment, ttl, protocol, checksum, src, dest = \
        struct.unpack('! B B H H H B B H 4s 4s', data[:IPV4_HEADER_MIN_LEN])
    
    return {
        'version_ihl': version_ihl,
        'version': version_ihl >> 4,
        'ihl': version_ihl & 0xF,
        'tos': tos,
        'total_length': total_length,
        'identification': identification,
        'flags_fragment': flags_fragment,
        'ttl': ttl,
        'protocol': protocol,
        'checksum': checksum,
        'src': format_ipv4_address(src),
        'dest': format_ipv4_address(dest)
    }

def format_ipv4_address(bytes_addr):
    """Format IPv4 address to readable string"""
    return '.'.join(map(str, bytes_addr))

def format_ipv4_header(header):
    """Format IPv4 header for display"""
    protocol_name = {
        1: 'ICMP',
        6: 'TCP',
        17: 'UDP'
    }.get(header['protocol'], f"Unknown ({header['protocol']})")
    
    return f"""
[IPv4 PACKET]
    Version:         {header['version']}
    Header Length:   {header['ihl'] * 4} bytes
    TTL:             {header['ttl']}
    Protocol:        {protocol_name}
    Source IP:       {header['src']}
    Destination IP:  {header['dest']}"""


# ==================== TCP LAYER PARSING ====================

def parse_tcp_segment(data):
    """Parse TCP segment header"""
    src_port, dest_port, sequence, acknowledgment, offset_reserved, flags, window, checksum, urgent_pointer = \
        struct.unpack('! H H L L B B H H H', data[:TCP_HEADER_MIN_LEN])
    
    return {
        'src_port': src_port,
        'dest_port': dest_port,
        'sequence': sequence,
        'acknowledgment': acknowledgment,
        'offset_reserved': offset_reserved,
        'flags': flags,
        'flag_urg': (flags & 32) >> 5,
        'flag_ack': (flags & 16) >> 4,
        'flag_psh': (flags & 8) >> 3,
        'flag_rst': (flags & 4) >> 2,
        'flag_syn': (flags & 2) >> 1,
        'flag_fin': flags & 1,
        'window': window,
        'checksum': checksum,
        'urgent_pointer': urgent_pointer
    }

def format_tcp_header(header):
    """Format TCP header for display"""
    flags = []
    if header['flag_urg']: flags.append('URG')
    if header['flag_ack']: flags.append('ACK')
    if header['flag_psh']: flags.append('PSH')
    if header['flag_rst']: flags.append('RST')
    if header['flag_syn']: flags.append('SYN')
    if header['flag_fin']: flags.append('FIN')
    
    flags_str = ', '.join(flags) if flags else 'None'
    
    return f"""
[TCP SEGMENT]
    Source Port:     {header['src_port']}
    Dest Port:       {header['dest_port']}
    Sequence:        {header['sequence']}
    Acknowledgment:  {header['acknowledgment']}
    Flags:           {flags_str}
    Window Size:     {header['window']}"""


# ==================== UDP LAYER PARSING ====================

def parse_udp_segment(data):
    """Parse UDP segment header"""
    src_port, dest_port, length, checksum = struct.unpack('! H H H H', data[:UDP_HEADER_LEN])
    
    return {
        'src_port': src_port,
        'dest_port': dest_port,
        'length': length,
        'checksum': checksum
    }

def format_udp_header(header):
    """Format UDP header for display"""
    return f"""
[UDP SEGMENT]
    Source Port:     {header['src_port']}
    Dest Port:       {header['dest_port']}
    Length:          {header['length']}
    Checksum:        {header['checksum']}"""


# ==================== ICMP LAYER PARSING ====================

def parse_icmp_packet(data):
    """Parse ICMP packet header"""
    icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
    
    return {
        'type': icmp_type,
        'code': code,
        'checksum': checksum
    }

def format_icmp_header(header):
    """Format ICMP header for display"""
    icmp_types = {
        0: 'Echo Reply',
        3: 'Destination Unreachable',
        8: 'Echo Request',
        11: 'Time Exceeded'
    }
    
    type_name = icmp_types.get(header['type'], f"Unknown ({header['type']})")
    
    return f"""
[ICMP PACKET]
    Type:            {type_name}
    Code:            {header['code']}
    Checksum:        {header['checksum']}"""


# ==================== UTILITY FUNCTIONS ====================

def format_payload(data, max_bytes=100):
    """Format payload data for display"""
    # Limit displayed data
    display_data = data[:max_bytes]
    
    # Try to decode as ASCII
    ascii_data = ''.join([chr(b) if 32 <= b <= 126 else '.' for b in display_data])
    
    # Create hex dump
    hex_lines = []
    for i in range(0, len(display_data), 16):
        chunk = display_data[i:i+16]
        hex_part = ' '.join(f'{b:02x}' for b in chunk)
        ascii_part = ''.join([chr(b) if 32 <= b <= 126 else '.' for b in chunk])
        hex_lines.append(f"    {i:04x}:  {hex_part:<48}  |{ascii_part}|")
    
    result = '\n'.join(hex_lines)
    
    if len(data) > max_bytes:
        result += f"\n    ... ({len(data) - max_bytes} more bytes)"
    
    return result

def get_local_ip():
    """Get local IP address (for Windows compatibility)"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


# ==================== PROGRAM ENTRY POINT ====================

if __name__ == '__main__':
    main()
