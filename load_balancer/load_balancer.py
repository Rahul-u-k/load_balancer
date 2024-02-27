import socket
import threading
import time

class Server:
    def __init__(self, name, port, weight):
        self.name = name
        self.port = port
        self.weight = weight
        self.connections = 0
        self.last_check_time = time.time()

    def check_health(self):
        # Simulated health check, replace with actual implementation
        # Here, we're just checking if the server has handled any connections in the last 5 seconds
        if time.time() - self.last_check_time > 5:
            self.weight -= 1  # Decrease weight if no connections in the last 5 seconds
        else:
            self.weight += 1  # Increase weight if handling connections
        self.last_check_time = time.time()

class LoadBalancer:
    def __init__(self):
        self.servers = [
            Server('server1', 8000, 5),
            Server('server2', 8000, 5),
        ]
        self.lock = threading.Lock()

    def find_best_server(self):
        with self.lock:
            # Sort servers by weight in descending order
            sorted_servers = sorted(self.servers, key=lambda server: server.weight, reverse=True)
            return sorted_servers[0]

    def start(self):
        lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lb_socket.bind(('0.0.0.0', 8001))
        lb_socket.listen(5)
        print("Load balancer started, listening on port 8001...")

        while True:
            client_conn, client_addr = lb_socket.accept()
            print(f"Connection from client {client_addr}")

            server = self.find_best_server()
            print(f"Selected server: {server.name}")

            server.connections += 1
            server.check_health()

            server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_conn.connect((server.name, server.port))

            data = client_conn.recv(1024)
            if not data:
                break

            print(f"Sending data to server: {data.decode()}")
            server_conn.sendall(data)

            response = server_conn.recv(1024)
            print(f"Received response from server: {response.decode()}")

            client_conn.sendall(response)

            server.connections -= 1
            client_conn.close()
            server_conn.close()

if __name__ == "__main__":
    load_balancer = LoadBalancer()
    load_balancer.start()
