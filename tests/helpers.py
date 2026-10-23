"""Gemeinsame Hilfen für Tests, die einen echten Server-Prozess starten."""
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Server:
    def __init__(self, db_path):
        self.db_path = db_path
        self.port = free_port()
        self.base = f"http://127.0.0.1:{self.port}"
        self.proc = None

    def start(self):
        env = {**os.environ, "TODO_DB": self.db_path}
        code = f"import app; app.app.run(host='127.0.0.1', port={self.port}, debug=False)"
        self.proc = subprocess.Popen(
            [sys.executable, "-c", code],
            cwd=ROOT,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        deadline = time.time() + 10
        while time.time() < deadline:
            if self.proc.poll() is not None:
                raise RuntimeError("Server ist beim Start beendet worden")
            try:
                urllib.request.urlopen(self.base + "/api/todos", timeout=1).close()
                return
            except OSError:
                time.sleep(0.1)
        self.stop()
        raise RuntimeError("Server wurde nicht rechtzeitig erreichbar")

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            self.proc.wait(timeout=5)

    def request(self, method, path, body=None):
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(
            self.base + path, data=data, method=method, headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                raw = r.read()
                return r.status, (json.loads(raw) if raw else None)
        except urllib.error.HTTPError as e:
            raw = e.read()
            return e.code, (json.loads(raw) if raw else None)
