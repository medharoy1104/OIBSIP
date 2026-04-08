import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext
import os

host = '127.0.0.1'
port = 12345
CHAT_FILE = "chat.txt"

# GUI setup
root = tk.Tk()
root.withdraw()

username = simpledialog.askstring("Username", "Enter your name:", parent=root)

root.deiconify()
root.title("Chat App")
root.geometry("500x600")
root.configure(bg="#1e1e1e")

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((host, port))
except:
    print("Server not running")
    exit()

# Chat area
chat_area = scrolledtext.ScrolledText(
    root,
    bg="black",
    fg="white",
    font=("Arial", 12)
)
chat_area.pack(padx=10, pady=10, fill="both", expand=True)
chat_area.config(state='disabled')

# Load previous chat
if os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "r") as f:
        chat_area.config(state='normal')
        for line in f:
            chat_area.insert(tk.END, line)
        chat_area.config(state='disabled')

# Message entry
msg_entry = tk.Entry(root, width=50, bg="gray", fg="white", font=("Arial", 12))
msg_entry.pack(padx=10, pady=5, fill="x")

def send_message():
    msg = msg_entry.get()
    if msg.strip() == "":
        return

    message = f"{username}: {msg}"
    client.send(message.encode())
    msg_entry.delete(0, tk.END)

send_button = tk.Button(root, text="Send", bg="green", fg="white", command=send_message)
send_button.pack(pady=5)

# ENTER key support
msg_entry.bind("<Return>", lambda event: send_message())

# Display message
def display_message(message):
    chat_area.config(state='normal')

    if message.startswith(username + ":"):
        msg = message.replace(username + ":", "You:")
        chat_area.insert(tk.END, msg + "\n", "self")
    else:
        chat_area.insert(tk.END, message + "\n", "other")

    chat_area.config(state='disabled')
    chat_area.yview(tk.END)

    # Save chat
    with open(CHAT_FILE, "a") as f:
        f.write(message + "\n")

# Colors
chat_area.tag_config("self", foreground="cyan")
chat_area.tag_config("other", foreground="lightgreen")

# Receive messages
def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            root.after(0, display_message, message)
        except:
            break

threading.Thread(target=receive, daemon=True).start()

root.mainloop()
