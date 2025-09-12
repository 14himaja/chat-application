# Chat Application

## Table of Contents

1. [Project Description](#project-description)  
2. [Features](#features)  
3. [Technology Stack](#technology-stack)  
4. [Design & Implementation Approaches](#design--implementation-approaches)  
5. [Setup & Installation](#setup--installation)  
6. [Usage](#usage)  
7. [Project Structure](#project-structure)  
8. [output](#output)


---

## Project Description

This project is a **Chat Application** built in Python, with both server and client components, along with a web component. It allows multiple clients to connect and exchange chat messages via a server, and also includes a web interface possibly for displaying or interacting with messages. The project includes both real-time communication (socket-based) and web front-end parts.

---

## Features

- Real-time text messaging between client(s) and server (console clients)  
- Web frontend to view/send messages (templates, static files)  
- Simple chat history or log (e.g. `chat_messages.txt`) to persist messages  
- Separation between client, server, and web components  

---

## Technology Stack

- **Python** (socket programming) for client-server communication  
- **Flask** (or another Python web framework) for web interface (templates + static assets)  
- HTML, CSS for the web frontend  
- File I/O (log file) to store or persist message history  

---

## Design & Implementation Approaches

- **Socket Programming**: Using Python sockets in `server.py` and `client.py` to manage real-time communication. This allows low-level control over connections and message passing.

- **Separation of Concerns**:  
  - `server.py` handles connection management and routing of messages between clients.  
  - `client.py` handles user input/output and sends messages to server.  
  - `app.py` + templates/static serve the web interface.

- **Persistent Chat Log**: Using a file (`chat_messages.txt`) as a basic storage for messages. Ensures that chat history is kept (at least during runtime or across restarts if file is read/written accordingly).

- **Web Interface**: Offers a way for users to view messages and potentially send via browser, which is more accessible than purely console-based clients.

- **Template / Static Assets Use**: Keeping HTML templates and CSS in separate folders (`templates/`, `static/`) for clean organization and maintainability.

---

## Setup & Installation

```bash
# Clone the repository
git clone https://github.com/14himaja/OIBSIP_python_programming_5.git
cd OIBSIP_python_programming_5

# (Optional) Create virtual environment
python3 -m venv venv
source venv/bin/activate         # on Linux / Mac
venv\Scripts\activate            # on Windows

# Install dependencies
# If using Flask or other web framework
pip install flask

# Run the server
python server.py

# Start a client (in separate terminal window)
python client.py

# Run the web interface
python app.py
```
## Usage

-Start server.py to accept client connections.

-Start one or more client.py instances; enter messages via console.

-Messages are sent to server, which broadcasts them to other clients.

-Use the web interface (app.py) to view the log of messages and optionally send messages (depending on how front end is implemented).

-Message history stored in chat_messages.txt can be reviewed via console or web.

## Project Structure
```
OIBSIP_python_programming_5/
├── server.py                # Handles socket server: accepts connections, routes messages
├── client.py                # Client side: connects to server, reads/sends user messages
├── app.py                   # Web interface: Flask app to display/send messages via browser
├── templates/index.html     # HTML templates for web UI
├── static/style.css         # CSS, JS, other frontend assets
├── chat_messages.txt        # Persistent chat history / log file
├── README.md                # Project documentation (this file)
└── (other configuration files if any)
```
## output
[chat application.webm](https://github.com/user-attachments/assets/f98648b6-5ccb-45ba-bfd4-834bb371c3ac)


## Navigate in browser to the address printed by app.py (http://127.0.0.1:5000/)
