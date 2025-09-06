# server.py
import socket
import threading

HOST = "127.0.0.1"   # change to your LAN IP to allow others on your network
PORT = 5000

clients = {}  # conn -> name
lock = threading.Lock()

def broadcast(line: str, exclude=None):
    """Send a single text line (with newline) to all connected clients."""
    with lock:
        dead = []
        for conn in clients.keys():
            if conn is exclude:
                continue
            try:
                conn.sendall((line + "\n").encode("utf-8"))
            except Exception:
                dead.append(conn)
        for d in dead:
            clients.pop(d, None)
            try:
                d.close()
            except:
                pass

def handle_client(conn, addr):
    try:
        f = conn.makefile("r", encoding="utf-8", newline="\n")
        # First line from client is their display name
        name = f.readline().strip()
        if not name:
            name = f"{addr[0]}:{addr[1]}"

        with lock:
            clients[conn] = name

        broadcast(f"🟢 {name} joined the chat")

        for line in f:
            text = line.rstrip("\n")
            if not text:
                continue
            # Broadcast to everyone else
            broadcast(f"{name}: {text}", exclude=None)
    except Exception:
        pass
    finally:
        with lock:
            name = clients.pop(conn, "Unknown")
        broadcast(f"🔴 {name} left the chat")
        try:
            conn.close()
        except:
            pass

def main():
    print(f"Server starting on {HOST}:{PORT} …")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print("Server is ready. Waiting for clients…")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
