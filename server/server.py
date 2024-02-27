import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8000))  # Listen on all network interfaces
    server_socket.listen(1)
    print("Server started, listening on port 8000...")
    
    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received data: {data.decode()}")
        conn.sendall(data)
        conn.close()

if __name__ == "__main__":
    start_server()
