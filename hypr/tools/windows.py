#!/bin/python3
from argparse import ArgumentParser
import subprocess
import json 

# Returns a list of all json window objects per workspace
def get_workspace_windows():
    command = "hyprctl clients -j"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = json.loads(process.communicate()[0])

    windows = []
    for output in data:
        address = output['address']
        workspace = output['workspace']
        title = output['title']
        pid = output['pid']
        pinned = output['pinned']
        floating = output['floating']
        fullscreen = output['fullscreen']
        # if pid in pids:
        #     continue
        # else:
        #     pids.append(pid)
        if workspace['id'] >= 1: 
            windows.append({'a': address,
                            'w': workspace,
                            't': title,
                            'p':pid,
                            'pin': pinned,
                            'floating': floating,
                            'fullscreen': fullscreen,
                            })
    return windows

def parse_windows(windows): 
    string_windows = []
    indices = []
    for i_ws, ws in enumerate(windows):
        id = ws['w']['id']
        title = ws['t']
        pin = 'P' if ws['pin'] else ''
        floating = 'F' if ws['floating'] else ''
        fullscreen = 'f' if ws['fullscreen'] else ''
        s = f'<b>{id}</b>\t[{pin}{floating}{fullscreen}]\t{title}'
        string_windows.append(s)
        indices.append(i_ws)
    return string_windows, indices
        
        

# Executes wofi with the given input string
def show_wofi(windows):
    command = "wofi -p \"Windows: \" -d -i -m -k /dev/null --hide-scroll"
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    return process.communicate(input=windows)[0]

# Returns the sway window id of the window that was selected by the user inside wofi
def parse_id(strings, selected, windows):
    selected = selected.decode("UTF-8")[:-1] # Remove new line character
    index = strings.index(selected)
    return windows[index]['a']

# Switches the focus to the given id
def switch_window(address):
    command = f"hyprctl dispatch focuswindow address:{address}"
    print(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.communicate()[0]

# Entry point
if __name__ == "__main__":
    parser = ArgumentParser(description="Wofi based window switcher")
    ws_windows = get_workspace_windows()
    strings, indices = parse_windows(ws_windows)
    wofi_string = "\n".join(strings).encode("UTF-8")
    selected = show_wofi(wofi_string)
    selected_id = parse_id(strings, selected, ws_windows)
    switch_window(selected_id)
