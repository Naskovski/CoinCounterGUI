import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from detector import detectCoins

def loadImage():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if file_path:
        detectCoins(file_path)

        coin_window = tkinter.Toplevel(menu)
        coin_window.title("CoinCounter")
        coin_window.geometry("800x600")

        # Read .txt file
        with open("./assets/results.txt", "r") as file:
            content = file.read()

        coin_data = tkinter.Label(coin_window, text=content, padx=20, pady=20)
        coin_data.pack(side="right", padx=20, pady=20)

        coin_image = tkinter.PhotoImage(file="./assets/result.png")

        image_width = 400
        image_height = int(coin_image.height() * (image_width/coin_image.width()))
        coin_image = coin_image.subsample(coin_image.width() // image_width, coin_image.height() // image_height)

        img_lbl = tkinter.ttk.Label(coin_window, image=coin_image, background=bgcolor)
        img_lbl.pack(side="left", padx=50, pady=20)

        coin_window.mainloop()



def close_app():
    menu.destroy()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # style vars
    bgcolor = "#fcfbf4"
    border_color = "#aa0033"
    #style = tkinter.ttk.Style()
    #style.configure('bt_style', foreground=bgcolor, font=("Helvetica", 12), border=border_color)

    #app
    menu = tkinter.Tk()
    menu.title("CoinCounter")
    menu.configure(bg=bgcolor)

    logo = tkinter.PhotoImage(file="./logo_small.png")
    logo_lbl = tkinter.ttk.Label(menu, image=logo, background=bgcolor)
    logo_lbl.pack(side="top", padx=50, pady=20)

    heading = tkinter.ttk.Label(text="CoinCounter", font=("Helvetica", 25), padding=10, background=bgcolor)
    heading.pack()

    btn_Open = tkinter.ttk.Button(menu, text="Load Image", command=loadImage)
    btn_Open.pack()

    btn_Close = tkinter.ttk.Button(menu, text="Close", command=close_app)
    btn_Close.pack()


    menu.mainloop()
