📘 Safe Code Executor – Learning Project

A simple and secure system that executes untrusted Python code inside a restricted Docker container, through a Flask API.
This project demonstrates Docker sandboxing, timeouts, resource limits, and safe execution techniques.

🚀 Features

Run Python code safely in Docker

Web UI for entering and running code

Automatic timeout (10 seconds)

Memory limit (128m)

CPU limit (0.5)

PID limit (64)

No network access (--network none)

Code length validation (max 5000 chars)

Optional read-only filesystem

File system isolation (docker mount)

📁 Project Structure
safe-code-executor/
├── app.py               # Flask API server
├── executor.py          # Docker sandbox logic
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Web UI for testing
└── README.md            # Documentation

🛠️ Installation & Setup
1️⃣ Install dependencies

Create a virtual environment:

python3 -m venv venv
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Make sure Docker is installed and running:

docker run hello-world

2️⃣ Run the Flask API
python3 app.py


Open in browser:

http://127.0.0.1:5000


You will see a UI where you can write Python code and run it.

🌐 API Usage
POST /run
Request Body:
{
  "code": "print('Hello World')"
}

Successful Response:
{
  "output": "Hello World\n"
}

Error Response Example:
{
  "error": "Execution timed out after 10 seconds"
}

🛡️ Docker Sandbox Security

When the API receives code, it creates a temporary file and runs:

docker run --rm \
  --network none \
  --memory 128m \
  --cpus 0.5 \
  --pids-limit 64 \
  -v <tempdir>:/app \
  -w /app \
  python:3.11-slim \
  python code.py

Security Features:
Feature	Purpose
--network none	Blocks internet access
--memory 128m	Prevents memory bombs
--cpus 0.5	Limits CPU usage
--pids-limit 64	Prevents fork bombs
Temporary directory mount	Keeps host filesystem safe
Timeout (10s)	Stops infinite loops
--read-only (optional)	Prevents file modification
Code size limit	Prevents huge code submissions
🧪 Security Tests Performed
✔ Test 1 — Normal Code
print("Hello World")


Result: Works correctly.

✔ Test 2 — Infinite Loop
while True:
    pass


Result:
⏳ Times out after 10 seconds.

✔ Test 3 — Memory Limit
x = "a" * 1000000000


Result:
🚫 Container gets killed due to memory limit (128MB).

✔ Test 4 — Network Block
import requests
requests.get("http://example.com")


Result:
❌ ModuleNotFoundError OR network blocked.

✔ Test 5 — Filesystem Isolation
with open("/etc/passwd") as f:
    print(f.read())


Result:
Shows container’s passwd, not host’s.

✔ Test 6 — Write File
with open("/tmp/test.txt", "w") as f:
    f.write("hello")
print("done")


Result:
✔ Works inside container only.

With --read-only:
❌ PermissionError.

🎓 What I Learned

How to run untrusted Python code safely

Using Docker containers as sandboxes

Applying memory, CPU, PID, network restrictions

Preventing infinite loops with timeouts

How container filesystems are isolated from the host

Building a simple Python + Flask API

Executing code inside Docker using subprocess

Documenting and testing a small DevOps project

📌 Future Improvements
Easy

Prettier UI

Syntax highlighting

JavaScript runner (Node.js)

Medium

Multi-file support

Save execution history

Advanced

Run containers as non-root

Custom seccomp profile

Study container escape attacks

👤 Author

Mallula Yaswanth