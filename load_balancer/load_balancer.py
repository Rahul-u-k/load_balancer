import socket

def start_load_balancer():
    server_addresses = [('server1', 8000), ('server2', 8000)]  # Update with actual server names
    server_index = 0

    lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_socket.bind(('0.0.0.0', 8001))  # Listen on all network interfaces
    lb_socket.listen(5)
    print("Load balancer started, listening on port 8001...")

    while True:
        client_conn, client_addr = lb_socket.accept()
        print(f"Connection from client {client_addr}")

        server_addr = server_addresses[server_index]
        server_index = (server_index + 1) % len(server_addresses)

        server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_conn.connect(server_addr)

        data = client_conn.recv(1024)
        if not data:
            break

        print(f"Sending data to server: {data.decode()}")
        server_conn.sendall(data)

        response = server_conn.recv(1024)
        print(f"Received response from server: {response.decode()}")

        client_conn.sendall(response)
        client_conn.close()
        server_conn.close()

if __name__ == "__main__":
    start_load_balancer()
