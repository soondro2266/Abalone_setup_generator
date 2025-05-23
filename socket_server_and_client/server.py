import socket
import json

class Server():
    def __init__(self, host = "127.0.0.1", port = 9000):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        
    def run(self):
        self.sock.listen()
        print(f"Listen on port: {self.port}")
        conn, addr = self.sock.accept()
        with conn:
            print(f"Connected by: {addr}")
            while True:
                # return b'' when connection close (b'' will be treat as False)
                binary_data = conn.recv(1024)
                if not binary_data:
                    print(f"Connection closed: {addr}")
                    break
                data = json.loads(binary_data.decode())
                state = data["state"]
                action = data["action"]
                print(f"Received:\nstate = {state}\naction = {action}")
                """
                data process
                """
                conn.send(b"ok")  # or send next observation
    
