import socket

def tcpConnection(host, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    received = None
    try:
        # Connect to server and send data
        sock.connect((host, port))
        sock.sendall(message)

        # Receive data from the server and shut down
        received = sock.recv(1024)
    except Exception as e:
        print str(e)
    finally:
        sock.close()
    if not received is None:
        return format(received)
    return None

