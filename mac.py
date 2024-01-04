import re
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Function to validate a MAC address format
def is_valid_mac_address(mac):
    mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return re.match(mac_pattern, mac)

# Function to handle the "Check MAC Address" button click event
def check_mac_address():
    mac = mac_entry.get()
    if is_valid_mac_address(mac):
        result_label.config(text=f"Add MAC address to ISE: {mac}", foreground="green")
    else:
        result_label.config(text="Invalid MAC address format. Please use the format XX:XX:XX:XX:XX:XX.", foreground="red")

# Create the main window
root = tk.Tk()
root.title("ISE Voucher")

# Create a label
label = ttk.Label(root, text="Enter a MAC address (e.g. 00:1A:2B:3C:4D:5E):")
label.pack(pady=10)

# Create an entry widget for MAC address input
mac_entry = ttk.Entry(root)
mac_entry.pack(pady=5)

# Create a button to check the MAC address
check_button = ttk.Button(root, text="Add MAC Address", command=check_mac_address)
check_button.pack(pady=5)

# Create a label to display the validation result
result_label = ttk.Label(root, text="", font=("Arial", 12))
result_label.pack()

# Center the window on the screen
root.update_idletasks()
width = 400
height = 150
x = (root.winfo_screenwidth() - width) // 2
y = (root.winfo_screenheight() - height) // 2
root.geometry(f"{width}x{height}+{x}+{y}")

# Start the main loop
root.mainloop()
