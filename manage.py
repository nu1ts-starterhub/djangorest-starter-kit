#!/usr/bin/env python
import os
import sys
import subprocess
import atexit

def start_docker_compose():
    print("🚀 Starting all docker-compose services...")
    subprocess.run(["docker", "compose", "up", "-d"], check=True)
    print("✅ All services started.")

def stop_docker_compose():
    print("🛑 Stopping all docker-compose services...")
    try:
        subprocess.run(["docker", "compose", "stop"], check=True)
        print("✅ All services stopped.")
    except subprocess.CalledProcessError:
        print("⚠️ Failed to stop services.")

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    
    if len(sys.argv) > 1 and sys.argv[1] in ["runserver", "migrate", "shell"]:
        if os.environ.get("RUN_MAIN") or sys.argv[1] != "runserver":
            start_docker_compose()
            atexit.register(stop_docker_compose)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()