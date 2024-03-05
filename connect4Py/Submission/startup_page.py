# Imports
import tkinter as tk
from tkinter.ttk import *

import game_page as gp
import integrated_game as ig
import host_game as hg
import joingame_page as jp


# Functions
def start():
    """
    This function starts the application
    :return: NONE
    """
    # Declare Start page, and create all widgets related
    start_page = tk.Tk()
    start_page.geometry("400x420")
    start_page.eval("tk::PlaceWindow . center")
    start_page.title("Connect-4-Xist")
    start_page.configure(bg="black")
    frame_a = tk.Frame(start_page)
    frame_b = tk.Frame(frame_a)
    frame_c = tk.Frame(start_page)
    frame_a.pack()
    frame_b.pack()
    frame_c.pack()
    # Title
    title_lbl = Label(
        frame_b,
        text="\n\n\n\n"
             "Welcome to Connect-4-Xist",
        font=("Helvetica", 18),
        foreground="white",
        background="black",
        padding="10"
    )
    title_lbl.pack()

    # Buttons
    multiplayer_btn = tk.Button(
        frame_c,
        text="1 Vs 1 Offline",
        fg="white",
        bg="green",
        width=15,
        padx=10,
        pady=10,
        command=lambda vi=start_page: break_recreate(vi)
    )
    online_btn = tk.Button(
        frame_c,
        text="1 Vs 1 Online",
        fg="white",
        bg="orange",
        width=15,
        padx=10,
        pady=10,
        command=lambda vi=start_page: break_recreate_online(vi, start_page.slaves())
    )
    singleplayer_btn = tk.Button(
        frame_c,
        text="Vs AI (Good luck)",
        fg="white",
        bg="blue",
        width=15,
        padx=10,
        pady=10,
        command=lambda vi=start_page: break_recreate_bot(vi)
    )
    ex_btn = tk.Button(
        frame_c,
        text="Exit",
        fg="white",
        bg="red",
        width=15,
        padx=10,
        pady=10,
        command=start_page.destroy
    )

    multiplayer_btn.grid(row=0, column=1)
    online_btn.grid(row=1, column=1)
    singleplayer_btn.grid(row=2, column=1)
    ex_btn.grid(row=3, column=1)

    # Loop it
    start_page.selection_clear()
    start_page.mainloop()


def break_recreate(start_page):
    start_page.destroy()
    gp.game_build()


def break_recreate_online(start_page, widgetlist):
    # destroy the current widgets.
    for val in widgetlist:
        val.destroy()

    # Create and add in widget
    frame_d = tk.Frame(start_page)
    frame_e = tk.Frame(start_page)
    frame_d.pack()
    frame_e.pack()

    online_lbl = tk.Label(
        frame_d,
        text="\n\n\n\n"
             "Do you wish to host or join game?",
        font=("Helvetica", 18),
        foreground="white",
        background="black",
        justify = tk.CENTER
    )
    create_btn = tk.Button(
        frame_e,
        text="Host Game",
        fg="white",
        bg="green",
        width=15,
        padx=10,
        pady=10,
        command=lambda : create_game(start_page)
    )
    join_btn = tk.Button(
        frame_e,
        text="Join Game",
        fg="white",
        bg="blue",
        width=15,
        padx=10,
        pady=10,
        command=lambda : join_game(start_page)
    )
    back_btn = tk.Button(
        frame_e,
        text="Back",
        fg="white",
        bg="red",
        width=15,
        padx=10,
        pady=10,
        command=lambda : back(start_page)
    )
    online_lbl.grid(row = 0, column = 1)
    create_btn.grid(row = 1, column = 1)
    join_btn.grid(row = 2, column = 1)
    back_btn.grid(row = 3, column = 1)
    start_page.update()

def back(start_page):
    start_page.destroy()
    start()

def break_recreate_bot(start_page):
    start_page.destroy()
    ig.game_build()

def create_game(start_page):
    start_page.destroy()
    hg.build_host()

def join_game(start_page):
    start_page.destroy()
    jp.build_join()