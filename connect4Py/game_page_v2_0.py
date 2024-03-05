# Imports
import tkinter as tk
from tkinter.ttk import *

import startup_page as sp

# Global Var
player_list = []
btn_list = []
turn = True
turn_list = []
p1 = []
p2 = []
draw = False


# Functions
def game_build():
    """
    {This function builds the game and initiates
    the game logic for the game in general}
    :return: NONE
    """
    root = tk.Tk()
    root.geometry("400x420")
    root.eval("tk::PlaceWindow . center")
    root.title("Connect-4-Xisits")
    f = Frame(root)
    f.pack()
    f_a = Frame(root)
    f_a.pack()
    f_b = Frame(root)
    f_b.pack()

    # Insert Blocks
    alphabet_list = ["a", "b", "c", "d", "e", "f", "g"]
    for x in range(7):
        namer = alphabet_list[x]
        for i in range(6):
            num = i
            val_name = namer + str(num)
            val = val_name
            val_name = tk.Text(
                f,
                width="6",
                height="3",
                fg="gray",
                bg="gray"
            )
            val_name.insert(tk.INSERT, val)
            val_name.grid(row=6 - i, column=x)
            val_name.bindtags((str(val_name), str(root), "all"))
            player_list.append(val_name)

    # Insert Buttons
    for v in range(7):
        # namer = alphabet_list[v]
        btn_name = "Btn " + str(v)
        btn = btn_name
        btn = "Btn " + namer
        btn_list.append(tk.Button(
            f,
            text="Drop",
            width="6",
            height="3",
            command=lambda vi=v: drop(vi)
        ))
        btn_list[v].grid(row=7, column=v)
    text_val = ""
    if turn == True:
        text_val = "Red's Turn"
    else:
        text_val = "Yellow's Turn"
    whos_turn = tk.Label(
        f_a,
        text=text_val
    )
    whos_turn.pack()
    turn_list.append(whos_turn)

    # Button to back and exit
    back_btn = Button(
        f_b,
        text="Back",
        command=lambda vi=root: back(vi)

    )
    back_btn.grid(row=8, column=0)
    # reload button
    reload_btn = Button(
        f_b,
        text="Reload",
        command=lambda vi=root: reload(vi)
    )
    reload_btn.grid(row=8, column=1)
    exit_main_btn = Button(
        f_b,
        text="Exit",
        command=root.destroy
    )
    exit_main_btn.grid(row=8, column=2)
    # loop through
    root.mainloop()


def drop(button_id):
    """
    {This function reacts to the on click of each "drop" button}
    :param button_id: ID of the button
    :return: Does not return a value
    """
    global turn
    player = 0

    if turn:
        player = 1
    else:
        player = 2

    msg, status, position = validateinput(button_id + 1, player)
    # print(status)
    if position != 90:
        cur_pos = int(position) - (button_id + 1) * 10 - 1 + 6 * button_id
        # print(cur_pos)
        update_list(cur_pos)
    print(msg)

    if status:
        if turn:
            # Flipped as the system has updated the players already
            # so the current turn get will be opposite of the winner result
            winner_winner("Yellow Player")
        else:
            winner_winner("Red Player")
    elif draw:
        winner_winner("Draw")


def update_list(subval):
    # calling on Global variable
    global turn
    if turn == False:
        # Colour the block
        # True for player r, False for player y
        player_list[subval].configure(fg="yellow", bg="yellow")
        player_list[subval].delete("1.0", "end")
        player_list[subval].insert(tk.INSERT, 'y')
        player_list[subval].update()
        turn = True
        turn_list[0].configure(text="Red's Turn")

    else:
        player_list[subval].configure(fg="red", bg="red")
        player_list[subval].delete("1.0", "end")
        player_list[subval].insert(tk.INSERT, 'r')
        player_list[subval].update()
        turn = False
        turn_list[0].configure(text="Yellow's Turn")


def winner_winner(player_name):
    title = "Winner!"
    if player_name == "Draw":
        title = "Draw"
    popup = tk.Toplevel()
    popup.geometry("220x90")
    popup.title(title)
    # Declaring frames
    frame1 = Frame(popup)
    frame2 = Frame(frame1)
    frame3 = Frame(frame1)
    frame1.pack()
    frame2.pack()
    frame3.pack()

    # Edit the text to say who won
    if player_name == "Draw":
        winner_msg = "The game has come to a draw state"
        turn_list[0].configure(text="Round results in a Draw")
    else:
        winner_msg = "<< " + player_name + " Wins >>\nCookies for you champ!"
        turn_list[0].configure(text=player_name + " has won")

    # Widgets to display
    win_label = Label(
        frame2,
        text=winner_msg,
    )
    exit_btn = Button(
        frame3,
        text="Exit",
        command=popup.destroy
    )
    win_label.grid(row="0", column="1")
    exit_btn.grid(row="1", column="1")

    # Disable the game buttons
    for btn in btn_list:
        btn.bindtags((str(btn), str(popup), "all"))
        btn.configure(fg="gray")
        btn.update()

    win = True
    try:
        while win:
            popup.update()
        return
    except tk.TclError:
        print("breakit")


def back(game_page):
    global btn_list, player_list, turn_list, turn, p1, p2, draw, bot1
    player_list = []
    btn_list = []
    turn_list = []
    p1 = []
    p2 = []
    turn = True
    draw = False
    game_page.destroy()
    sp.start()


def reload(game_page):
    """
    Function to reload the game to the initial state
    :param game_page:
    :return:
    """
    global btn_list, player_list, turn_list, turn, p1, p2, draw, bot1
    player_list = []
    btn_list = []
    turn_list = []
    p1 = []
    p2 = []
    turn = True
    draw = False
    game_page.destroy()
    game_build()

# Jing Liang codes
# which path is open for bot + how many more needed
# position of the missing pieces
# how many pieces is needed before victory


def validateinput(userinput, player):
    highestpiece = 0
    msg = ''

    # checks for highest piece
    for x in p1:
        if int(x[0]) == userinput and int(x[1]) > highestpiece:
            highestpiece = int(x[1])
    for x in p2:
        if int(x[0]) == userinput and int(x[1]) > highestpiece:
            highestpiece = int(x[1])

    # checks if the piece can be placed
    try:
        if highestpiece < 6:
            placement = '%s%s' % (userinput, highestpiece + 1)
            msg = 'Piece placed'

            # places piece and add into list
            # print("Printing Placement: " + str(placement))
            if player == 1:
                p1.append(placement)
            elif player == 2:
                p2.append(placement)

            decide = nextnum(player)
            # print("Printing Decide: " + str(decide))
        else:
            msg = 'Piece cannot be placed, please select another slot'

        return msg, decide, placement
    except UnboundLocalError:
        return msg, False, 90


def wincon(pieces, nextpiece, first, second, player):
    winner = False

    # check if player has won
    for i in range(1, 4):
        nextpiece = '%s%s' % (int(nextpiece[0]) + int(first), int(nextpiece[1]) + int(second))
        if nextpiece not in pieces:
            break
        elif i == 3:
            winner = True

    return winner


def nextnum(player):
    pieces = []
    winner = False
    msg = ''
    global draw

    if player == 1:
        pieces = p1
    elif player == 2:
        pieces = p2

    for x in pieces:
        if int(x[0]) > 3:  # checks to the left
            winner = wincon(pieces, x, '-1', '0', player)
            if winner:
                break

        if int(x[0]) > 3 and int(x[1]) < 4:  # checks diagonally left
            winner = wincon(pieces, x, '-1', '1', player)
            if winner:
                break

        if int(x[0]) < 5:  # checks to the right
            winner = wincon(pieces, x, '1', '0', player)
            if winner:
                break

        if int(x[0]) < 5 and int(x[1]) < 4:  # checks diagonally right
            winner = wincon(pieces, x, '1', '1', player)
            if winner:
                break

        if int(x[1]) < 4:  # checks upwards
            winner = wincon(pieces, x, '0', '1', player)
            if winner:
                break

    if winner:
        msg = 'Player ' + str(player) + ' wins!!!'
    elif len(p1) + len(p2) == 42:
        msg = 'Its a draw'
        draw = True
        print(msg)
    else:
        msg = 'Keep going~'

    return winner
