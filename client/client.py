import socket
import time

def send_request():
    try:
        lb_address = 'load_balancer'
        lb_port = 8001
        print(f"Connecting to load balancer at {lb_address}:{lb_port}")
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((lb_address, lb_port))
        message = "Hello, server!"
        
        start_time = time.time() # Record start time
        
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        
        end_time = time.time() # Record end time
        
        rtt = end_time - start_time # Calculate RTT
        print(f"Received from server: {data.decode()}, RTT: {rtt:.6f} seconds")
        
        client_socket.close()
        
        return rtt  # Return the RTT value
    except ConnectionRefusedError as cre:
        print("Connection refused:", cre)
        print("Make sure the load balancer and servers are running.")
        return None
    except Exception as e:
        print("Error:", e)
        return None

if __name__ == "__main__":
    num_requests = 5  # Number of requests to send
    delay_between_requests = 1  # Delay between each request in seconds
    total_rtt = 0.0  # Initialize total RTT
    for _ in range(num_requests):
        rtt = send_request()
        if rtt is not None:
            total_rtt += rtt
        time.sleep(delay_between_requests)  # Introduce delay between requests
    
    if total_rtt != 0:
        average_rtt = total_rtt / num_requests
        print(f"Average RTT: {average_rtt:.6f} seconds")
    else:
        print("No valid RTT measurements to calculate average.")
