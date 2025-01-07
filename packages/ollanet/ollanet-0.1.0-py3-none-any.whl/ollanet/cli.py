import os
import threading
from .api import app
from .ngrok_handler import run_ngrok
from simple_term_menu import TerminalMenu
import uvicorn
import subprocess
import sys
import click

def run_fastapi(port):
    uvicorn.run(app, host="0.0.0.0", port=int(port))

@click.command()
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    port = input("Enter the port number to run the FastAPI server: ").strip()
    authtoken = input("Enter your ngrok authtoken: ").strip()
    
    options = ["http", "https"]
    terminal_menu = TerminalMenu(options, title="Select protocol:")
    protocol_index = terminal_menu.show()
    protocol = options[protocol_index]
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * os.get_terminal_size().columns)
    
    fastapi_thread = threading.Thread(target=run_fastapi, args=(port,))
    fastapi_thread.start()
    
    run_ngrok(protocol, port, authtoken)