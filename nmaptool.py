import socket
import sys
import threading
import time
from tkinter import *
from tkinter import filedialog
# ==== Scan Vars ====
ip_s = 1
ip_f = 1024
log = []
ports = []
target = 'localhost'


def scanPort(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        c = s.connect_ex((target, port))
        if c == 0:
            m = ' Port %d \t[open]' % (port,)
            log.append(m)
            ports.append(port)
            listbox.insert("end", str(m))
            updateResult()
        s.close()
    except OSError:
        print('> Too many open sockets. Port ' + str(port))
    except:
        c.close()
        s.close()
        sys.exit()
    sys.exit()


def updateResult():
    rtext = " [ " + str(len(ports)) + " / " + str(ip_f) + " ] ~ " + str(target)
    L27.configure(text=rtext)


def startScan():
    global ports, log, target, ip_f
    clearScan()
    log = []
    ports = []
    # Get ports ranges from GUI
    ip_s = int(L24.get())
    ip_f = int(L25.get())
    # Start writing the log file
    log.append('> Nmap')
    log.append('=' * 14 + '\n')
    log.append(' Target:\t' + str(target))

    try:
        target = socket.gethostbyname(str(L22.get()))
        log.append(' IP Adr.:\t' + str(target))
        log.append(' Ports: \t[ ' + str(ip_s) + ' / ' + str(ip_f) + ' ]')
        log.append('\n')
        # Lets start scanning ports!
        while ip_s <= ip_f:
            try:
                scan = threading.Thread(target=scanPort, args=(target, ip_s))
                scan.setDaemon(True)
                scan.start()
            except:
                time.sleep(0.01)
            ip_s += 1
    except:
        m = '> Target ' + str(L22.get()) + ' not found.'
        log.append(m)
        listbox.insert(0, str(m))

def saveScan():
    global log, target, ports, ip_f
    log[5] = " Result:\t[ " + str(len(ports)) + " / " + str(ip_f) + " ]\n"
    
    # Get the content of the listbox and log
    result_content = "\n".join(log) + "\n\n"
    result_content += "\n".join(listbox.get(0, 'end'))

    # Open a file dialog for saving the result
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    
    if file_path:
        # Write the content to the selected file
        with open(file_path, "w") as file:
            file.write(result_content)


def clearScan():
    listbox.delete(0, 'end')


# ==== GUI ====
gui = Tk()
gui.title('Nmap')
gui.geometry("550x800")
gui.configure(bg="black")

# ==== Colors ====
m1c = '#00ee00'
bgc = '#222222'
dbg = '#000000'
fgc = '#111111'

gui.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc, activeForeground=bgc,
                  highlightColor=m1c, highlightBackground=m1c)

# ==== Labels ====
L11 = Label(gui, text="Nmap", font=("Helvetica", 16, 'underline'), bg="black", fg=m1c)
L11.place(x=16, y=10)

L21 = Label(gui, text="Target: ", bg="black", fg=m1c)
L21.place(x=16, y=90)

L22 = Entry(gui)
L22.place(x=180, y=90, width=150)
L22.insert(0, "localhost")

L23 = Label(gui, text="Ports: ", bg="black", fg=m1c)
L23.place(x=16, y=158)

L24 = Entry(gui)
L24.place(x=180, y=158, width=95)
L24.insert(0, "1")

L25 = Entry(gui)
L25.place(x=290, y=158, width=95)
L25.insert(0, "1024")

L26 = Label(gui, text="Results: ", bg="black", fg=m1c)
L26.place(x=16, y=220)
L27 = Label(gui, text="[ ... ]", bg="black", fg=m1c)
L27.place(x=180, y=220)

# ==== Ports list ====
frame = Frame(gui)
frame.place(x=16, y=275, width=650, height=415)
listbox = Listbox(frame, width=89, height=15)
listbox.place(x=0, y=0)
listbox.bind('<<ListboxSelect>>')
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# ==== Buttons / Scans ====
B11 = Button(gui, text="Start Scan", command=startScan, bg="green")
B11.place(x=16, y=600, width=150)

B21 = Button(gui, text="Save Result", command=saveScan, bg="green")
B21.place(x=180, y=600, width=150)

B31 = Button(gui, text="Clear", command=clearScan, bg="green")
B31.place(x=345, y=600, width=150)

# ==== Start GUI ====
gui.mainloop()
