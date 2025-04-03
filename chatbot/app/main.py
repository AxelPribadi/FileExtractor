import sys
import subprocess

if __name__ == "__main__":
    # run chainlit from the main file 
    try:
        command = ["chainlit", "run", "app/bot/app.py", "-w"]
        subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr)
    except KeyboardInterrupt:
        print("Chatbot Session Ended")
    