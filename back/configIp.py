import socket

def get_ipv4():
    """
    Retrieves the IPv4 address of the current server using its hostname.

    Returns:
        str: The IPv4 address of the server.
    """
    hostname = socket.gethostname()  
    ip_address = socket.gethostbyname(hostname)  
    return ip_address

ipv4_address = get_ipv4()