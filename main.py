import tkinter
from tkinter import *
from tkinter import ttk


#TEST3
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # style vars
    bgcolor = "#fcfbf4"
    border_color = "#aa0033"
    #style = tkinter.ttk.Style()
    #style.configure('bt_style', foreground=bgcolor, font=("Helvetica", 12), border=border_color)

    #app
    top = tkinter.Tk()
    top.title("CoinCounter")
    top.configure(bg=bgcolor)

    logo = tkinter.PhotoImage(file="./logo_small.png")
    logo_lbl = tkinter.ttk.Label(top, image=logo, background=bgcolor)
    logo_lbl.pack(side="top", padx=50, pady=20)

    heading = tkinter.ttk.Label(text="CoinCounter", font=("Helvetica", 25), padding=10, background=bgcolor)
    heading.pack()

    btn_Open = tkinter.ttk.Button(text="Load Image")
    btn_Open.pack()

    btn_Close = tkinter.ttk.Button(text="Close")
    btn_Close.pack()







    top.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
