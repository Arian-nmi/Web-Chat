🗨️ Web-Chat

A real‑time chat web application built with Django Channels and WebSockets.
This project demonstrates how to add asynchronous, bidirectional communication to a Django project – moving beyond traditional HTTP request/response cycle.
🚀 Features

    Real‑time messaging with WebSockets

    Multiple chat rooms / group chat support

    User authentication (login / logout)

    Message history (saved to database)

    Simple and clean UI (HTML/CSS)

🛠️ Tech Stack
Category	Technologies
Backend	Django, Django Channels
Asynchronous	ASGI, WebSockets
Database	SQLite / PostgreSQL (configurable)
Frontend	HTML, CSS (custom), JavaScript (WebSocket API)

🧠 How It Works (Architecture)

    A user logs in and enters a chat room.

    The browser opens a WebSocket connection to the Django Channels server.

    Messages are sent and received asynchronously over the WebSocket.

    The server broadcasts messages to all connected clients in the same room.

    Messages are optionally persisted to the database (for history).

🗂️ Project Structure (main files)
Web-Chat/
├── apps/                # Chat application logic
├── config/              # Project settings, ASGI/WSGI config
├── templates/chat/      # HTML templates for chat UI
├── manage.py
└── requirements.txt

📌 Why This Project Matters (for recruiters)
This project proves that you can:

    Work with asynchronous Django (beyond traditional views)

    Implement WebSockets and real‑time features

    Handle persistent connections and broadcasting

    Write clean, maintainable Django code

📜 License
This project is open‑source and available under the MIT License.

👨‍💻 Author
Arian Naeimi
