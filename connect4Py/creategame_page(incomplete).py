from scapy.all import *
from tkinter import *
from tkinter.constants import DISABLED, NORMAL
import tkinter as tk
import random
#FIX: enabling start button does not work!

# Delcaring globals
gamecodels = [random.randrange(0, 9), random.randrange(0, 9), random.randrange(0, 9), random.randrange(0, 9),
              random.randrange(0, 9), random.randrange(0, 9)]
ownip = get_if_addr(conf.iface)
oppip = ""
cgTxtDsipStr = ""
connectedBool = False
print(gamecodels)

# Creating UI
root = Tk()
root.geometry("400x420")
root.title("Create Game")

# Creating Frames
cgMainFr = Frame(root)
cgMainFr.pack()
cgLabelFr1 = Frame(cgMainFr)
cgLabelFr1.pack()
cgLabelFr2 = Frame(cgMainFr)
cgLabelFr2.pack()
cgCodeFr = Frame(cgMainFr)
cgCodeFr.pack()
cgTxtDispFr = Frame(cgMainFr, pady=20, padx=10)
cgTxtDispFr.pack()
cgButtonFr = Frame(cgMainFr, pady=15, padx=5)
cgButtonFr.pack()

# Gamecode Label
gamecodeTLabel = Label(cgLabelFr1, text="Provide Game Code to Player 2 to connect.", fg='red')
gamecodeTLabel.grid(row=1, column=0)
gamecodeTLabel.config(font=("Aerial", 14))
gamecodeLabel = Label(cgLabelFr2, text="Game Code: ")
gamecodeLabel.grid(row=1, column=0)
gamecodeLabel.config(font=("Aerial", 26))

# Declaring StringVar() to set text in Game code Entry Boxes
strv1 = StringVar()
strv2 = StringVar()
strv3 = StringVar()
strv4 = StringVar()
strv5 = StringVar()
strv6 = StringVar()

# Creating Entry Boxes for Game Code
Entry(cgCodeFr, textvariable=strv1, state=DISABLED, font=("Aerial", 26), width=2, justify="center").grid(
    row=1, column=1)
Entry(cgCodeFr, textvariable=strv2, state=DISABLED, font=("Aerial", 26), width=2, justify="center").grid(
    row=1, column=2)
Entry(cgCodeFr, textvariable=strv3, state=DISABLED, font=("Aerial", 26), width=2, justify="center").grid(
    row=1, column=3)
Entry(cgCodeFr, textvariable=strv4, state=DISABLED, font=("Aerial", 26), width=2, justify="center").grid(
    row=1, column=4)
Entry(cgCodeFr, textvariable=strv5, state=DISABLED, font=("Aerial", 26), width=2, justify="center").grid(
    row=1, column=5)
Entry(cgCodeFr, textvariable=strv6, state=DISABLED, font=("Aerial", 26), width=2, justify="center").grid(
    row=1, column=6)

# Text display
cgTxtDsip = Text(cgTxtDispFr, height=8, width=52, font=("Aerial,16"), bg='black', fg='white')
cgTxtDsipStr = "Please connect when Player 2 is ready to connect.\n"
cgTxtDsip.insert(tk.END, cgTxtDsipStr)
cgTxtDsip.pack()

def stopfilter(pkt):
    global ownip
    global gamecodels
    global oppip
    oppip = str(pkt[IP].src)

    print("packet got")
    print("checking " + ownip + " agianst " + pkt[IP].dst)
    print("checking ", type(ownip), " agianst ", type(pkt[IP].dst))

    if pkt[IP].dst == ownip and str(pkt[Raw].load)[2:-1] == ''.join(str(elem) for elem in gamecodels):
        return True
    else:
        return False

def establishConnection():
    global ownip
    global gamecodels
    global oppip
    global cgTxtDsipStr
    global connectedBool

    cgTxtDsipStr = "Trying to connect with Player 2...\n"
    cgTxtDsip.insert(tk.END, cgTxtDsipStr)
    cgTxtDsip.update()

    pkt = sniff(filter="icmp", lfilter=stopfilter, count=1, timeout=10)
    if pkt:
        cgTxtDsipStr = "Trying to connect with Player 2...\n"
        cgTxtDsip.insert(tk.END, cgTxtDsipStr)
        startBtn.configure(state=NORMAL)
        print("connection has been established")
    else:
        print("connection failed")

# Buttons
tryconnect = Button(
    cgButtonFr,
    text="Connect",
    font=('Aerial,16'),
    command=establishConnection,
    pady=10,
    padx=20)

startBtn = Button(
    cgButtonFr,
    text="Start!",
    font=('Aerial,16'),
    state=DISABLED,
    pady=10,
    padx=20)

backBtn = Button(
    cgButtonFr,
    text="Back",
    font=('Aerial,16'),
    pady=10,
    padx=30) #add command to go back to prev menu

tryconnect.pack(side='left',padx=10)
startBtn.pack(side='left',padx=10)
backBtn.pack(side='right',padx=10)

def setGameCode():
    # Setting each digit of game code to each Entry boxes
    strv1.set(gamecodels[0])
    strv2.set(gamecodels[1])
    strv3.set(gamecodels[2])
    strv4.set(gamecodels[3])
    strv5.set(gamecodels[4])
    strv6.set(gamecodels[5])

def sendGameBC():

    pkt = fragment(IP(src=ownip, dst='255.255.255.255') / ICMP() / 'connect4game')
    send(pkt)


setGameCode()
while 1:
    sendGameBC()
    print(ownip+" "+oppip)
    root.update_idletasks()
    root.update()



