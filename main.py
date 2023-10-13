import tkinter as tk
from tkinter import ttk
import sqlite3
import pypresence
import time
def create_or_check_client_id_table():
    conn = sqlite3.connect('rpc_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS client_id (client_id TEXT)''')
    conn.commit()
    conn.close()

def create_or_check_rpc_settings_table():
    conn = sqlite3.connect('rpc_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS rpc_settings (
                        state TEXT,
                        details TEXT,
                        large_image TEXT,
                        small_image TEXT,
                        large_text TEXT,
                        small_text TEXT,
                        start INTEGER,
                        button_label1 TEXT,
                        button_url1 TEXT,
                        button_label2 TEXT,
                        button_url2 TEXT,
                        use_start_timestamp INTEGER)''')
    conn.commit()
    conn.close()

def save_rpc_data():
    state = state_entry.get() or None
    details = details_entry.get() or None
    large_image = large_image_entry.get() or None
    small_image = small_image_entry.get() or None
    large_text = large_text_entry.get() or None
    small_text = small_text_entry.get() or None
    start = start_entry.get() or int(time.time())
    button_label1 = button_label1_entry.get() or ""
    button_url1 = button_url1_entry.get() or None
    button_label2 = button_label2_entry.get() or ""
    button_url2 = button_url2_entry.get() or None
    use_start_timestamp = start_timestamp_var.get()

    RPC.connect()
    start = int(start) if use_start_timestamp else None
    buttons = []
    if button_label1:
        buttons.append({"label": button_label1, "url": button_url1})
    if button_label2:
        buttons.append({"label": button_label2, "url": button_url2})

    RPC.update(
        state=state,
        details=details,
        large_image=large_image,
        small_image=small_image,
        large_text=large_text,
        small_text=small_text,
        start=start,
        buttons=buttons
    )

    conn = sqlite3.connect('rpc_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM rpc_settings')
    cursor.execute('INSERT INTO rpc_settings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (state, details, large_image, small_image, large_text, small_text, start, button_label1, button_url1, button_label2, button_url2, use_start_timestamp))
    conn.commit()
    conn.close()

def save_client_id():
    client_id = client_id_entry.get()
    create_or_check_client_id_table()
    conn = sqlite3.connect('rpc_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM client_id')
    cursor.execute('INSERT INTO client_id VALUES (?)', (client_id,))
    conn.commit()
    conn.close()
    RPC.client_id = client_id

root = tk.Tk()
root.title("Discord RPC Bot")

style = ttk.Style()
style.configure('TLabel', font=('Arial', 10))
style.configure('TButton', font=('Arial', 10))

# Create and place control elements on the form
client_id_label = ttk.Label(root, text="Client ID:")
client_id_label.grid(row=0, column=0, padx=10, pady=5)
client_id_entry = ttk.Entry(root, font=('Arial', 10))
client_id_entry.grid(row=0, column=1, padx=10, pady=5)

state_label = ttk.Label(root, text="State:")
state_label.grid(row=1, column=0, padx=10, pady=5)
state_entry = ttk.Entry(root, font=('Arial', 10))
state_entry.grid(row=1, column=1, padx=10, pady=5)

details_label = ttk.Label(root, text="Details:")
details_label.grid(row=2, column=0, padx=10, pady=5)
details_entry = ttk.Entry(root, font=('Arial', 10))
details_entry.grid(row=2, column=1, padx=10, pady=5)

large_image_label = ttk.Label(root, text="Large Image:")
large_image_label.grid(row=3, column=0, padx=10, pady=5)
large_image_entry = ttk.Entry(root, font=('Arial', 10))
large_image_entry.grid(row=3, column=1, padx=10, pady=5)

small_image_label = ttk.Label(root, text="Small Image:")
small_image_label.grid(row=4, column=0, padx=10, pady=5)
small_image_entry = ttk.Entry(root, font=('Arial', 10))
small_image_entry.grid(row=4, column=1, padx=10, pady=5)

large_text_label = ttk.Label(root, text="Large Text:")
large_text_label.grid(row=5, column=0, padx=10, pady=5)
large_text_entry = ttk.Entry(root, font=('Arial', 10))
large_text_entry.grid(row=5, column=1, padx=10, pady=5)

small_text_label = ttk.Label(root, text="Small Text:")
small_text_label.grid(row=6, column=0, padx=10, pady=5)
small_text_entry = ttk.Entry(root, font=('Arial', 10))
small_text_entry.grid(row=6, column=1, padx=10, pady=5)

start_label = ttk.Label(root, text="Start Timestamp (leave empty for current time):", font=('Arial', 10))
start_label.grid(row=7, column=0, padx=10, pady=5)
start_entry = ttk.Entry(root, font=('Arial', 10))
start_entry.grid(row=7, column=1, padx=10, pady=5)

start_timestamp_var = tk.IntVar()
start_timestamp_checkbutton = ttk.Checkbutton(root, text="Use Start Timestamp", variable=start_timestamp_var, style='TCheckbutton')
start_timestamp_checkbutton.grid(row=8, columnspan=2, padx=10, pady=5)

button_label1_label = ttk.Label(root, text="Button Label 1:")
button_label1_label.grid(row=9, column=0, padx=10, pady=5)
button_label1_entry = ttk.Entry(root, font=('Arial', 10))
button_label1_entry.grid(row=9, column=1, padx=10, pady=5)

button_url1_label = ttk.Label(root, text="Button URL 1:")
button_url1_label.grid(row=10, column=0, padx=10, pady=5)
button_url1_entry = ttk.Entry(root, font=('Arial', 10))
button_url1_entry.grid(row=10, column=1, padx=10, pady=5)

button_label2_label = ttk.Label(root, text="Button Label 2:")
button_label2_label.grid(row=11, column=0, padx=10, pady=5)
button_label2_entry = ttk.Entry(root, font=('Arial', 10))
button_label2_entry.grid(row=11, column=1, padx=10, pady=5)

button_url2_label = ttk.Label(root, text="Button URL 2:")
button_url2_label.grid(row=12, column=0, padx=10, pady=5)
button_url2_entry = ttk.Entry(root, font=('Arial', 10))
button_url2_entry.grid(row=12, column=1, padx=10, pady=5)

save_button = ttk.Button(root, text="Start and save", command=lambda: [save_client_id(), save_rpc_data()], style='TButton')
save_button.grid(row=13, columnspan=2, padx=10, pady=5)

RPC = pypresence.Presence(client_id=None)

def load_client_id():
    create_or_check_client_id_table()
    conn = sqlite3.connect('rpc_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM client_id')
    data = cursor.fetchone()
    conn.close()
    if data:
        client_id_entry.insert(0, data[0])
        RPC.client_id = data[0]

load_client_id()

def load_saved_data():
    create_or_check_rpc_settings_table()
    conn = sqlite3.connect('rpc_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rpc_settings')
    data = cursor.fetchone()
    conn.close()
    if data:
        state_entry.insert(0, data[0] or "")
        details_entry.insert(0, data[1] or "")
        large_image_entry.insert(0, data[2] or "")
        small_image_entry.insert(0, data[3] or "")
        large_text_entry.insert(0, data[4] or "")
        small_text_entry.insert(0, data[5] or "")
        start_entry.insert(0, data[6] or "")
        start_timestamp_var.set(data[11] or 0)
        button_label1_entry.insert(0, data[7] or "")  # Добавляем значения для кнопки 1
        button_url1_entry.insert(0, data[8] or "")  # Добавляем значения для URL кнопки 1
        button_label2_entry.insert(0, data[9] or "")  # Добавляем значения для кнопки 2
        button_url2_entry.insert(0, data[10] or "")  # Добавляем значения для URL кнопки 2

load_saved_data()

try:
    root.mainloop()
except KeyboardInterrupt:
    RPC.close()
