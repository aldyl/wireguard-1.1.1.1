import tkinter as tk
import subprocess
from handle_time import get_time_diference, pretty_time
from handle_bytes import pretty_bytes
import subprocess

def on_wg():
    # execute all commands at once using Popen
    wg_process = subprocess.Popen(
        ["wgon"], stdout=subprocess.PIPE)
    # get the output of command
    output = wg_process.communicate()[0].decode('utf-8')
    return_code = wg_process.returncode
    if return_code == 0:
        print(output)
    else:
        print(f"Command failed with return code {return_code}")


def off_wg():
    pass

# Create a function to run wg show command and update thinker interface


def show_wg(root, label_list):

    # execute all commands at once using Popen
    wg_process = subprocess.Popen(
        "sudo wg show wgcf-profile endpoints | cut -f2; sudo wg show wgcf-profile latest-handshakes | cut -f2; sudo wg show wgcf-profile transfer | cut -f2 ; sudo wg show wgcf-profile transfer | cut -f3", shell=True, stdout=subprocess.PIPE)

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

    else:
        endpoint = handshake = received = sent = "disconnected"

    # set values for labels
    for i, label in enumerate(label_list):
        if i == 0:
            if endpoint is not ("disconnected"):
                label.config(text="connected")
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
root.title("WG Show GUI")

titles = ["Status", "Endpoint", "Handshake", "Received", "Sent"]
label_list = []

# create labels in a loop
for i, title in enumerate(titles):
    label = tk.Label(root, text=title)
    label.grid(row=i, column=0, padx=10, pady=10, sticky="e")

# loop to create and append to the list
for i, title in enumerate(titles):
    label = tk.Label(root, text="disconnected")
    label.grid(row=i, column=1, padx=10, pady=10, sticky="w")
    label_list.append(label)


# Create a button to run the show_wg function
show_button = tk.Button(root, text="Show WG Configuration",
                        command=lambda: show_wg(root, label_list))
show_button.grid(row=1, column=3, padx=10, pady=10)

# Create a button to run the show_wg function
show_button = tk.Button(root, text="Activate", command=on_wg)
show_button.grid(row=2, column=3, padx=10, pady=10)


# Create a button to run the show_wg function
show_button = tk.Button(root, text="Desactivate", command=off_wg)
show_button.grid(row=3, column=3, padx=10, pady=10)


# Start the application
root.mainloop()
