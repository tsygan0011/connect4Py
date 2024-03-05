# Imports
import tkinter as tk
from tkinter.ttk import *

import Bot as bot
import startup_page as sp

# Global Var
player_list = []
btn_list = []
turn_list = []
p1 = []
p2 = []
turn = True
draw = False
difficulty_num = 0
colheights = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0
}
bot1 = bot.c4_bot(difficulty_num, p1, p2, 2, colheights)


# Functions
def game_build():
    """
    {This function builds the game and initiates
    the game logic for the game in general}
    :return: NONE
    """
    global difficulty_num
    # Build level query first:
    if difficulty_num == 0:
        difficulty_sel()
    else:
        print(difficulty_num)
        root = tk.Tk()
        root.geometry("800x840")
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
                    width="12",
                    height="6",
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
                width="10",
                height="4",
                command=lambda vi=v: drop(vi),
                font=('Helvetica, 12')
            ))
            btn_list[v].grid(row=7, column=v)
        text_val = ""
        if turn == True:
            text_val = "Red's Turn"
        else:
            text_val = "Yellow's Turn"
        whos_turn = tk.Label(
            f_a,
            text=text_val,
            font=('Helvetica, 26')
        )
        whos_turn.pack()
        turn_list.append(whos_turn)

        # Button to back and exit
        back_btn = tk.Button(
            f_b,
            text="Back",
            command=lambda vi=root: back(vi),
            font = ('Helvetica, 12'),
        )
        back_btn.grid(row=8, column=0,padx=15,pady=15)
        # reload button
        reload_btn = tk.Button(
            f_b,
            text="Reload",
            command=lambda vi=root: reload(vi),
            font = ('Helvetica, 12'),
        )
        reload_btn.grid(row=8, column=1,padx=15,pady=15)
        exit_main_btn = tk.Button(
            f_b,
            text="Exit",
            command=root.destroy,
            font = ('Helvetica, 12'),
        )
        exit_main_btn.grid(row=8, column=2,padx=15,pady=15)
        # loop through
        root.mainloop()


def drop(button_id):
    """
    {This function reacts to the on click of each "drop" button}
    :param button_id: ID of the button
    :return: Does not return a value
    """
    global turn
    global bot1
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
        if bot1:
            bot1 = None
    elif draw:
        winner_winner("Draw")
    if bot1:
        if player != bot1.player:
            if msg != 'Piece cannot be placed, please select another slot':
                drop(bot1.make_move())


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
    global difficulty_num
    title = "Winner!"
    if player_name != "Draw":
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
    winner_msg = ""
    if player_name == "Yellow Player":
        winner_msg = "You lost to a bot lol, scrubbbbbb"
        turn_list[0].configure(text="You lost to a bot lol, scrubbbbbb")
    elif player_name == "Draw":
        winner_msg = "The game has come to a draw state"
        turn_list[0].configure(text="Round results in a Draw")
    else:
        if difficulty_num > 2:
            winner_msg = "You have beaten death bot holy moly!\nCookies for you champ!"
            turn_list[0].configure(text=player_name + " has won")
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
        text="Close",
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


def difficulty_sel():
    """
    Function to build and query for difficulty
    :return: difficulty level (Int)
    """
    global difficulty_num
    difficulty_page = tk.Tk()
    difficulty_page.geometry("460x240")
    difficulty_page.eval("tk::PlaceWindow . center")
    difficulty_page.title("Difficulty level")
    # Declaring frames
    frame1 = Frame(difficulty_page)
    frame2 = Frame(frame1)
    frame3 = Frame(difficulty_page)
    frame4 = Frame(difficulty_page)
    frame1.pack()
    frame2.pack()
    frame3.pack()
    frame4.pack()

    # Widgets to display
    win_label = Label(
        frame2,
        text="Select the difficulty level of bot: ",
        font=('Helvetica',16),
    )
    lvl_one = tk.Button(
        frame3,
        text="Easy Boi",
        command=lambda: set_difficulty(1, difficulty_page),
        font=('Helvetica',16),
        bd=3
    )
    lvl_two = tk.Button(
        frame3,
        text="Kinda Easy",
        command=lambda: set_difficulty(2, difficulty_page),
        font=('Helvetica',16),
        bd=3
    )
    lvl_three = tk.Button(
        frame3,
        text="Da real shit",
        command=lambda: set_difficulty(3, difficulty_page),
        font=('Helvetica',16),
        bd=3
    )
    lvl_four = tk.Button(
        frame3,
        text="Serious shit",
        command=lambda: set_difficulty(4, difficulty_page),
        font=('Helvetica',16),
        bd=3
    )
    back_label = Label(
        frame4,
        text="Click to go back: ",
        font=('Helvetica',16),
    )
    back_btn = tk.Button(
        frame4,
        text="Lol scardy cat :)",
        command=lambda: back(difficulty_page),
        font=('Helvetica',16),
        bd=3
    )
    win_label.grid(row="0", column="1",pady=5,padx=5)
    lvl_one.grid(row="1", column="1",pady=5,padx=5)
    lvl_two.grid(row="1", column="2",pady=5,padx=5)
    lvl_three.grid(row="2", column="1",pady=5,padx=5)
    lvl_four.grid(row="2", column="2",pady=5,padx=5)
    back_label.grid(row="0", column="2",pady=5,padx=5)
    back_btn.grid(row="1", column="2",pady=5,padx=5)

    # loop till it gets difficulty number
    query_diff = True
    difficulty_page.mainloop()
    # difficulty.


def set_difficulty(diff, page):
    global bot1, p1, p2, colheights
    bot1 = bot.c4_bot(diff, p1, p2, 2, colheights)
    print("running " + str(diff))
    global difficulty_num
    difficulty_num = diff
    page.destroy()
    game_build()


def back(game_page):
    global btn_list, player_list, turn_list, turn, p1, p2, draw, bot1, colheights, difficulty_num
    player_list = []
    btn_list = []
    turn_list = []
    p1 = []
    p2 = []
    turn = True
    draw = False
    difficulty_num = 0
    colheights = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0
    }
    bot1 = bot.c4_bot(3, p1, p2, 2, colheights)
    game_page.destroy()
    sp.start()


def reload(game_page):
    """
    Function to reload the game to the initial state
    :param game_page:
    :return:
    """
    global btn_list, player_list, turn_list, turn, p1, p2, draw, bot1, colheights, difficulty_num
    player_list = []
    btn_list = []
    turn_list = []
    p1 = []
    p2 = []
    turn = True
    draw = False
    difficulty_num = 0
    colheights = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0
    }
    bot1 = bot.c4_bot(3, p1, p2, 2, colheights)
    game_page.destroy()

    game_build()


# Jing Liang codes
# which path is open for bot + how many more needed
# position of the missing pieces
# how many pieces is needed before victory


def validateinput(userinput, player):
    msg = ''

    # checks if the piece can be placed
    try:
        if colheights[userinput] < 6:
            # Place piece and increse height for col
            colheights[userinput] += 1
            placement = '%s%s' % (userinput, colheights[userinput])
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


def wincon(pieces, nextpiece, horizontal, vertical, player):
    winner = False

    # check if player has won
    for i in range(1, 4):
        nextpiece = '%s%s' % (int(nextpiece[0]) + int(horizontal), int(nextpiece[1]) + int(vertical))
        if nextpiece not in pieces:
            # if playing agianst a bot, let the bot know where to block
            if bot1:
                if i == 3:  # check for bot wincon with 3 in a row
                    bot1.wincon1110(player, nextpiece, horizontal, vertical)
                elif i == 2:  # check for bot wincon with 2 in a row
                    bot1.wincon1101_1100(player, nextpiece, horizontal, vertical)
                elif i == 1:
                    bot1.wincon1011_01010(player, nextpiece, horizontal, vertical)
                break

        elif i == 3:
            winner = True

    return winner


def nextnum(player):
    pieces = []
    winner = False
    msg = ''
    bot1.bot3winconlist.clear()
    bot1.bot2winconlist.clear()
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
    else:
        msg = 'Keep going~'

    # print(msg)
    # print(bot3winconlist)

    return winner
