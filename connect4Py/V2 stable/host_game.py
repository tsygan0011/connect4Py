from scapy.all import *
from tkinter import *
from tkinter.constants import DISABLED, NORMAL
import tkinter as tk
import random
import multi_game as mg
import startup_page as sp
#FIX: enabling start button does not work!

# Delcaring nonlocals
def build_host():
    gamecodels = [random.randrange(0, 9), random.randrange(0, 9), random.randrange(0, 9), random.randrange(0, 9),
                  random.randrange(0, 9), random.randrange(0, 9)]
    ownip = get_if_addr(conf.iface)
    oppip = ""
    cgTxtDsipStr = ""
    connectedBool = False
    broadcast =True

    print(gamecodels)

    def stopfilter(pkt):
        nonlocal ownip
        nonlocal gamecodels

        if pkt[IP].dst == ownip and str(pkt[Raw].load)[2:-1] == ''.join(str(elem) for elem in gamecodels):
            return True
        else:
            return False

    def establishConnection(pkt):
        nonlocal ownip
        nonlocal gamecodels
        nonlocal oppip
        nonlocal cgTxtDsipStr
        nonlocal connectedBool

        cgTxtDsipStr = "Trying to connect with Player 2...\n"
        cgTxtDsip.insert(tk.END, cgTxtDsipStr)

        if pkt:
            oppip = pkt[0][IP].src
            cgTxtDsipStr = "Player 2 has connected at " + oppip + "\n"
            cgTxtDsip.insert(tk.END, cgTxtDsipStr)
            startBtn.configure(state=NORMAL)
            print("connection has been established")
        else:
            cgTxtDsipStr = "No join request has been recieved\n"
            cgTxtDsip.insert(tk.END, cgTxtDsipStr)
            print("connection failed")

    def setGameCode():
        # Setting each digit of game code to each Entry boxes
        strv1.set(gamecodels[0])
        strv2.set(gamecodels[1])
        strv3.set(gamecodels[2])
        strv4.set(gamecodels[3])
        strv5.set(gamecodels[4])
        strv6.set(gamecodels[5])

    def sendGameBC():
        nonlocal broadcast
        pkt = fragment(IP(src=ownip, dst='255.255.255.255') / ICMP() / 'connect4game')
        while broadcast:
            send(pkt)
            print(ownip + " " + oppip)
            time.sleep(5)

    def startGame():
        nonlocal broadcast
        gamestr = 'connect4game ' + ''.join(str(elem) for elem in gamecodels) + ' STARTO'
        pkt = fragment(IP(src=ownip, dst=oppip) / ICMP() /gamestr)
        send(pkt)
        broadcast=False
        root.destroy()
        print(f"{ownip}, {oppip}, 0, {''.join(str(elem) for elem in gamecodels)}")
        mg.game_build(ownip,oppip,0,''.join(str(elem) for elem in gamecodels))


    def back():
        nonlocal broadcast
        broadcast=False
        root.destroy()
        sp.start()


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
    cgButtonFr = Frame(cgMainFr, pady=20, padx=5)
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

    # Buttons
    startBtn = Button(
        cgButtonFr,
        text="Start!",
        font=('Aerial,16'),
        command=startGame,
        state=DISABLED,
        pady=10,
        padx=45,
        bd=3)

    backBtn = Button(
        cgButtonFr,
        text="Back",
        font=('Aerial,16'),
        command=back,
        pady=10,
        padx=45,
        bd=3)  # add command to go back to prev menu

    startBtn.pack(side='left', padx=20)
    backBtn.pack(side='right', padx=20)

    setGameCode()
    broadcastthread = threading.Thread(target=sendGameBC, daemon=True)
    joinsniffthread =  AsyncSniffer(filter="icmp[icmptype] == icmp-echo", lfilter=stopfilter, count=1, prn=establishConnection)
    broadcastthread.start()
    joinsniffthread.start()

    root.mainloop()
