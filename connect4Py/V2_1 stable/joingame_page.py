from scapy.all import *
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import tkinter.constants as tkConst
import multi_game as mg
import startup_page as sp

def build_join():
    # Declaring nonlocals
    ownip = get_if_addr(conf.iface)
    oppip = ''
    oppipfound = []

    jg_page = Tk()
    jg_page.geometry("400x420")
    jg_page.title("Join Game")

    # Creating Frames
    jgMainFr = Frame(jg_page)
    jgMainFr.pack()
    jg_instcn_label_fr = Frame(jgMainFr)
    jg_instcn_label_fr.pack()
    jg_gameip_lsbox_fr = Frame(jgMainFr)
    jg_gameip_lsbox_fr.pack()
    jg_searchgame_btn_fr = Frame(jgMainFr)
    jg_searchgame_btn_fr.pack(pady=15)
    jg_gamecode_fr = Frame(jgMainFr)
    jg_gamecode_fr.pack(pady=15)
    jg_connect_btn_fr = Frame(jgMainFr)
    jg_connect_btn_fr.pack(pady=5)

    # Declaring gamecode as StringVar()
    gamecode = StringVar()

    # Join game instruction Label
    jg_instcn_label = Label(
        jg_instcn_label_fr,
        text="Please select a game and enter game code\nto connect to Player 1",
        fg='red',
        font=('Aerial, 12')
    ).pack()

    # Enter game code label
    jg_gamecode_label = Label(
        jg_gamecode_fr,
        text="Enter Player 1 Game Code: ",
        font=('Aerial, 12')
    )
    jg_gamecode_label.pack(side='left')

    # Game IP listbox
    jg_gameip_lsbox = Listbox(
        jg_gameip_lsbox_fr,
        height=8,
        width=30,
        bg='grey',
        font=('Aerial, 16'),
    )
    jg_gameip_lsbox.pack(side='left')

    # Game IP scrollbar
    jg_gameip_lsbox_scrlbar = Scrollbar(jg_gameip_lsbox_fr)
    jg_gameip_lsbox.config(yscrollcommand=jg_gameip_lsbox_scrlbar.set)
    jg_gameip_lsbox_scrlbar.config(command=jg_gameip_lsbox.yview)
    jg_gameip_lsbox_scrlbar.pack(side="right", fill=BOTH)

    def sniff4start(pkt):
        if pkt[0][IP].dst == ownip and str(pkt[0][Raw].load)[2:-1] == 'connect4game ' + gamecode.get() + ' STARTO':
            print("Start packet gotten")
            return True
        else:
            print("Irrelevent packet")
            return False

    def connect():
        gc = gamecode.get()
        print("Game Code entered " + gc)
        try:
            gameip = jg_gameip_lsbox.get(jg_gameip_lsbox.curselection())
            if len(gc) == 6:
                try:
                    int(gc)
                    pkt = IP(dst=gameip, src=ownip) / ICMP() / str(gc)
                    send(pkt)
                    startsnifferthread = AsyncSniffer(filter="icmp[icmptype] == icmp-echo", lfilter=sniff4start, prn=startGamepkt, count=1)
                    startsnifferthread.start()
                    messagebox.showinfo("Notice","Waiting for PLayer 1 to press the Start button")
                except ValueError:
                    print("Invalid")
                    messagebox.showerror("Invalid Input", "Please enter a valid Game Code!")
                    # gamecode.set("")
            elif len(gc) < 6:
                print("Game code entered is too short!")
                messagebox.showerror("Invalid Input", "Game code entered is too short!")
                gamecode.set("")
                try:
                    int(gc)
                except ValueError:
                    print("Invalid")
                    messagebox.showerror("Invalid Input", "Please enter a valid Game Code!")
                    # gamecode.set("")

            elif len(gc) > 6:
                print("Game Code entered is too long!")
                messagebox.showerror("Invalid Input", "Game Code entered is too long!")
                gamecode.set("")
                try:
                    int(gc)
                except ValueError:
                    print("Invalid")
                    messagebox.showerror("Invalid Input", "Please enter a valid Game Code!")
                    # gamecode.set("")
        except:
            messagebox.showerror("Error", "Please select a game first!")


    def sniff4games(pkt):
        nonlocal oppip
        nonlocal oppipfound

        oppip = pkt[IP].src

        if pkt[IP].dst == '255.255.255.255' and str(pkt[Raw].load)[2:-1] == 'connect4game':
            if oppip not in oppipfound:
                oppipfound.append(oppip)
                return True
        return False

            # return pkt.sprintf("Found: " + oppip + " oppopfoundlist: " + str(oppipfound))
    def startGamepkt(pkt):
        jg_page.event_generate("<<StartGame>>", when="now")

    def startGame(event):
        print("linking to game")
        # threading.Thread(target=mg.game_build, args=(ownip,oppip,1,gamecode.get())).start()
        gamesnifferthread.stop()
        oppip = jg_gameip_lsbox.get(jg_gameip_lsbox.curselection())
        jg_page.destroy()
        print(f"{ownip}, {oppip}, 0, {gamecode.get()}")
        mg.game_build(ownip,oppip,1,gamecode.get())

    def refreshlist():
        nonlocal ownip
        nonlocal oppipfound

        # reset nonlocals
        oppipfound = []

        jg_gameip_lsbox.delete(0, 'end')

    def updateGameList(pkt):
        nonlocal ownip
        nonlocal oppipfound

        jg_gameip_lsbox.insert(END, pkt[0][IP].src)
        # jg_gameip_lsbox.delete(0, 'end')
        #
        # for i in range(0, gamefoundcount):
        #     jg_gameip_lsbox.insert(END, oppipfound[i])

    def back():
        print("back button pressed")
        gamesnifferthread.stop()
        jg_page.destroy()
        sp.start()

    # Game Code Entry Box
    gamecode_entry = Entry(
        jg_gamecode_fr,
        textvariable=gamecode,
        font=('Aerial, 12'),
        width=17,
        bg='cyan'
    ).pack(side='right')

    # Creating Buttons
    jg_searchgame_btn = Button(
        jg_searchgame_btn_fr,
        text="Refresh list",
        font=('Aerial,16'),
        padx=75,
        bd=3,
        command=refreshlist,
    )
    jg_searchgame_btn.pack()

    jg_connect_btn = Button(
        jg_connect_btn_fr,
        text="Connect",
        font=('Aerial,16'),
        padx=60,
        command=connect,
        bd=3)
    jg_connect_btn.pack(side='left',padx=5)

    jg_back_btn = Button(
        jg_connect_btn_fr,
        text="Back",
        font=('Aerial,16'),
        padx=75,
        bd=3,
        command=back,
    )
    jg_back_btn.pack(side='right',padx=5)

    jg_page.bind("<<StartGame>>", startGame)

    gamesnifferthread = AsyncSniffer(filter="icmp[icmptype] == icmp-echo", lfilter=sniff4games, prn=updateGameList)
    gamesnifferthread.start()

    jg_page.mainloop()
