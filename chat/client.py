# client.py
import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

SERVER_HOST_DEFAULT = "127.0.0.1"
SERVER_PORT_DEFAULT = 5000

class ChatClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Chat — Tkinter")
        self.sock = None
        self.connected = False
        self.name = None

        # --- UI Layout ---
        self.root.geometry("540x560")
        self.root.minsize(420, 420)

        # Header
        header = ttk.Frame(self.root, padding=8)
        header.pack(fill="x")
        self.title_label = ttk.Label(header, text="Python Chat", font=("Segoe UI", 16, "bold"))
        self.title_label.pack(side="left")
        self.status_var = tk.StringVar(value="Disconnected")
        self.status = ttk.Label(header, textvariable=self.status_var)
        self.status.pack(side="right")

        # Chat area (read-only Text + Scrollbar)
        body = ttk.Frame(self.root, padding=(8, 0, 8, 0))
        body.pack(fill="both", expand=True)

        self.chat_text = tk.Text(body, wrap="word", state="disabled", height=20)
        self.chat_text.pack(side="left", fill="both", expand=True, padx=(0, 6), pady=8)

        scrollbar = ttk.Scrollbar(body, command=self.chat_text.yview)
        scrollbar.pack(side="right", fill="y", pady=8)
        self.chat_text["yscrollcommand"] = scrollbar.set

        # Input area
        bottom = ttk.Frame(self.root, padding=8)
        bottom.pack(fill="x")

        self.msg_var = tk.StringVar()
        self.entry = ttk.Entry(bottom, textvariable=self.msg_var)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_btn = ttk.Button(bottom, text="Send", command=self.send_message)
        self.send_btn.pack(side="right")

        # Menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        conn_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Connection", menu=conn_menu)
        conn_menu.add_command(label="Connect…", command=self.connect_dialog)
        conn_menu.add_command(label="Disconnect", command=self.disconnect)

        # Style (subtle, presentable)
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except:
            pass

        # Tags for coloring chat lines
        self.chat_text.tag_configure("you", foreground="#1b5e20")      # dark green
        self.chat_text.tag_configure("peer", foreground="#0d47a1")     # dark blue
        self.chat_text.tag_configure("system", foreground="#616161")   # gray/secondary
        self.chat_text.tag_configure("time", foreground="#9e9e9e", font=("Segoe UI", 8))

        # Prompt for connection at start
        self.root.after(200, self.connect_dialog)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------- Networking ----------
    def connect_dialog(self):
        if self.connected:
            messagebox.showinfo("Already connected", "You are already connected.")
            return
        name = simpledialog.askstring("Display Name", "Enter your name:")
        if not name:
            return
        host = simpledialog.askstring("Server Address", "Enter server IP/Host:", initialvalue=SERVER_HOST_DEFAULT)
        if not host:
            return
        port = simpledialog.askinteger("Server Port", "Enter server port:", initialvalue=SERVER_PORT_DEFAULT, minvalue=1, maxvalue=65535)
        if not port:
            return
        self.connect(name.strip(), host.strip(), port)

    def connect(self, name, host, port):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            # Send our display name as the first line
            self.sock.sendall((name + "\n").encode("utf-8"))
            self.connected = True
            self.name = name
            self.status_var.set(f"Connected as {name} @ {host}:{port}")
            self.append_system(f"Connected to {host}:{port} as {name}")
            threading.Thread(target=self.receive_loop, daemon=True).start()
            self.entry.focus_set()
        except Exception as e:
            self.connected = False
            self.sock = None
            messagebox.showerror("Connection failed", f"Could not connect: {e}")

    def disconnect(self):
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            try:
                self.sock.close()
            except:
                pass
        self.connected = False
        self.sock = None
        self.status_var.set("Disconnected")
        self.append_system("Disconnected.")

    def receive_loop(self):
        try:
            f = self.sock.makefile("r", encoding="utf-8", newline="\n")
            for line in f:
                text = line.rstrip("\n")
                if text:
                    self.root.after(0, self.append_peer, text)
        except Exception:
            pass
        finally:
            # If server drops, update UI
            if self.connected:
                self.root.after(0, self.append_system, "Connection closed by server.")
                self.connected = False
                self.root.after(0, lambda: self.status_var.set("Disconnected"))

    # ---------- UI helpers ----------
    def append(self, msg, tag="system"):
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_text.config(state="normal")
        self.chat_text.insert("end", msg + "\n", (tag,))
        self.chat_text.insert("end", f"   {timestamp}\n", ("time",))
        self.chat_text.see("end")
        self.chat_text.config(state="disabled")

    def append_system(self, msg):
        self.append(f"ⓘ {msg}", "system")

    def append_peer(self, raw_line):
        # raw_line could be "Name: message" or a system line like "🟢 Name joined…"
        if ": " in raw_line and not raw_line.startswith(("🟢", "🔴")):
            self.append(raw_line, "peer")
        else:
            self.append(raw_line, "system")

    def append_you(self, msg):
        self.append(f"You: {msg}", "you")

    # ---------- Actions ----------
    def send_message(self):
        text = self.msg_var.get().strip()
        if not text:
            return
        if not self.connected or not self.sock:
            messagebox.showwarning("Not connected", "Please connect to a server first.")
            return
        try:
            self.sock.sendall((text + "\n").encode("utf-8"))
            self.append_you(text)   # show immediately in your UI
            self.msg_var.set("")
        except Exception as e:
            messagebox.showerror("Send failed", f"Could not send message: {e}")
            self.disconnect()

    def on_close(self):
        self.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientApp(root)
    root.mainloop()
