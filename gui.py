#!/bin/python3

import tkinter as tk
import subprocess
from PIL import ImageTk, Image
import random
import time

def pretty_bytes(bytes):
    if bytes == 0:
        return '0 B'
    
    sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0

    while bytes >= 1024 and i < len(sizes) - 1:
        bytes /= 1024
        i += 1

    return f'{round(bytes,2)} {sizes[i]}'

def test_pretty_bytes():
    # Test lower bound (zero bytes)
    assert pretty_bytes(0) == '0 B'
    
    # Test within first size unit (bytes)
    assert pretty_bytes(42) == '42 B'
    
    # Test rounding down
    assert pretty_bytes(1023) == '1023 B'
    
    # Test rounding to two decimal places
    assert pretty_bytes(1234567) == '1.18 MB'
    
    # Test exact representable value in binary (binary-based systems)
    assert pretty_bytes(536870912) == '512.0 MB'
    
    # Test upper bound (terabytes)
    assert pretty_bytes(1099511627776) == '1.0 TB'


def pretty_time(left):

    intervals = (
        ('year', 31536000),  # 60 * 60 * 24 * 365
        ('day', 86400),     # 60 * 60 * 24
        ('hour', 3600),     # 60 * 60
        ('minute', 60),
        ('second', 1),
        )
    
    buf = []
    include_cero = False
    for name, count in intervals:
        value = int(left / count)

        if left < 1:
            buf.append(" 0 seconds")
            break

        if value > 0:
            buf.append(" %d %s%s" % (value, name, "s" if value > 1 else ""))
            left -= value * count
            include_cero = True
        
        elif include_cero:
            buf.append(" %d %s%s" % (value, name, "s"))
    
    index = len(buf) - 1  # start at the end of the list

    while buf[index].startswith(" 0 ") and index > 0:
        del buf[index]  # remove any 0 from the list
        index -= 1
        
    return buf


def get_time_diference(seconds):
    seconds = time.time() - seconds
    return seconds

def test_pretty_time():
    # Test case 1: Input of 0 seconds should return "0 seconds"
    left = 0
    print(pretty_time(left))
    assert pretty_time(left) == [" 0 seconds"]

    # Test case 2: Input of 1 second should return "1 second"
    left = 1
    print(pretty_time(left))
    assert pretty_time(left) == [" 1 second"]

    # Test case 3: Input of 65 seconds should return "1 minute, 5 seconds"
        # Test case 2: Input of 1 second should return "1 second"
    left = 65
    print(pretty_time(left))
    assert pretty_time(left) == [" 1 minute"," 5 seconds"]


    # Test case 4: Input of 3650 seconds should return "1 hour, 0 minutes, 50 seconds"
    left = 3650
    print(pretty_time(left))
    assert pretty_time(left) == [" 1 hour", " 0 minutes"," 50 seconds"]
    

    # Test case 5: Input of 31536000 seconds (1 year) should return "1 year"
    left = 31536000
    print(pretty_time(left))
    assert pretty_time(left) == [" 1 year"]

    #Random
    left = random.randint(50, 31536000*2)
    print(pretty_time(left))

def on_wg(show_button_off):
    # execute all commands at once using Popen
    wg_process = subprocess.Popen(
        ["wgon"], stdout=subprocess.PIPE)
    # get the output of command
    output = wg_process.communicate()[0].decode('utf-8')
    return_code = wg_process.returncode
    if return_code == 0:
        show_button_off.config(state="normal")
        print(output)
    else:
        print(f"Command failed with return code {return_code}")


def off_wg(show_button_on):
    # execute all commands at once using Popen
    wg_process = subprocess.Popen(
        ["wgoff"], stdout=subprocess.PIPE)
    # get the output of command
    output = wg_process.communicate()[0].decode('utf-8')
    return_code = wg_process.returncode
    if return_code == 0:
        show_button_on.config(state="normal")
        print(output)
    else:
        print(f"Command failed with return code {return_code}")


def show_wg_continuously(root, label_list, show_button_on, show_button_off):
    def call_show_wg(show_button_on, show_button_off):
        if root.focus_get() == root:

            if show_button_off['state'] == 'normal':
                show_wg(root, label_list, show_button_on, show_button_off)

        root.after(1000, lambda: call_show_wg(show_button_on, show_button_off))

    call_show_wg(show_button_on, show_button_off)

# Create a function to run wg show command and update thinker interface


def show_wg(root, label_list, show_button_on, show_button_off):

    # execute all commands at once using Popen
    wg_process = subprocess.Popen(
        "wg show wgcf-profile endpoints | cut -f2;  wg show wgcf-profile latest-handshakes | cut -f2;  wg show wgcf-profile transfer | cut -f2 ; wg show wgcf-profile transfer | cut -f3", shell=True, stdout=subprocess.PIPE)

    # get the output of all commands
    output = wg_process.communicate()[0].decode('utf-8')
    split_out = output.split("\n")

    # parse the output to get each variable

    if len(split_out) == 5:

        endpoint, handshake, received, sent, _ = split_out

        handshake = "".join(pretty_time(get_time_diference(int(handshake))))
        handshake = handshake + " ago"

        received = pretty_bytes(int(received))
        sent = pretty_bytes(int(sent))

        label_list[0].config(text="CONNECTED")
        show_button_off.config(state="normal")
        show_button_on.config(state="disable")

    else:

        status = endpoint = handshake = received = sent = "disconnected"
        label_list[0].config(text=status)
        show_button_off.config(state="disabled")
        show_button_on.config(state="normal")

    # set values for labels
    for i, label in enumerate(label_list):

        if i == 1:
            label.config(text=endpoint)
        elif i == 2:
            label.config(text=handshake)
        elif i == 3:
            label.config(text=received)
        elif i == 4:
            label.config(text=sent)

    root.update()


# Create the main window
root = tk.Tk()
root.title("Warp Cloudflare")

root.geometry('300x320')

# Load the image using PhotoImage
bg_image = tk.PhotoImage(file='bg.png')

# Create a Label widget with the image
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# load the image file
img = Image.open('wg_cloud_logo.png')

# create a PhotoImage object to be used as the icon
icon = ImageTk.PhotoImage(img)

# set the icon of the root window
root.iconphoto(True, icon)

titles = ["Status", "Endpoint", "Handshake", "Received", "Sent"]
label_list = []

# create labels in a loop
for i, title in enumerate(titles):
    label = tk.Label(root, text=title, background="#c5e5fc")
    label.grid(row=i, column=0, padx=10, pady=10, sticky="e")

# loop to create and append to the list
for i, title in enumerate(titles):
    label = tk.Label(root, text="disconnected", background="#d2e5f4")
    label.grid(row=i, column=1, padx=10, pady=10, sticky="w")
    label_list.append(label)

# Create a button to run the show_wg function
show_button_on = tk.Button(root, text="Activate",
                           command=lambda: on_wg(show_button_off), bg="#ffffff")
show_button_on.grid(row=5, column=1, padx=10, pady=10, ipadx=40)

# Create a button to run the show_wg function
show_button_off = tk.Button(
    root, text="Desactivate", command=lambda: off_wg(show_button_on), bg="#ffdad6")
show_button_off.grid(row=6, column=1, padx=10, pady=10, ipadx=30)


show_wg_continuously(root, label_list, show_button_on, show_button_off)

# Start the application
root.mainloop()
