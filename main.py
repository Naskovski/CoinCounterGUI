import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from detector import detectCoins


def second_window_logic():
    def update_canvas(event):
        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=images[0])
        for i in images_listbox.curselection():
            value = int(images_listbox.get(i)[:2])
            canvas.create_image(0, 0, anchor="nw", image=images[value])

    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if file_path:
        detectCoins(file_path)

        # Read .txt file
        with open("./assets/results.txt", "r") as file:
            content = file.read()

        # Layout
        coin_window = tkinter.Toplevel(menu)
        coin_window.title("CoinCounter")
        coin_window.geometry("800x600")

        coin_window.columnconfigure(0, weight=2)
        coin_window.columnconfigure(1, weight=1)
        coin_window.rowconfigure(0, weight=1)
        coin_window.rowconfigure(1, weight=3)

        total_value_display = ttk.Frame(coin_window)
        lines = content.splitlines()
        total_value = lines[0][13:]

        total_value_lbl = tkinter.ttk.Label(total_value_display, text=total_value, font=("Helvetica", 30), justify="center")
        total_value_lbl.pack(side="top", anchor="n")

        denari_lbl = ttk.Label(total_value_display, text="Денари", font=("Helvetica", 15), justify="center")
        denari_lbl.pack()

        total_value_display.grid(row=0, column=1)

        coin_image = tkinter.PhotoImage(file="./assets/result0.png")

        image_width = 400
        image_height = int(coin_image.height() * (image_width/coin_image.width()))

        canvas = tkinter.Canvas(coin_window, width=image_width + 60, height=image_height + 60)
        canvas.grid(row=0, column=0, rowspan=2, sticky="n")

        images_listbox = tkinter.Listbox(coin_window, selectmode=tkinter.MULTIPLE)
        images_listbox.bind("<<ListboxSelect>>", update_canvas)

        images = {}

        for i in [0, 1, 2, 5, 10, 50]:
            images[i] = tkinter.PhotoImage(file="./assets/result"+str(i)+".png")
            images[i] = images[i].subsample(images[i].width() // image_width, images[i].height() // image_height)


        for i in range(5):
            images_listbox.insert(tkinter.END, lines[i+3])
            images_listbox.select_set(i)


        images_listbox.grid(row=1, column=1)

        update_canvas(None)



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

    heading = tkinter.ttk.Label(text="CoinCounter", font=("Helvetica", 25), background=bgcolor)
    heading.pack(padx=20)

    btn_Open = tkinter.ttk.Button(menu, text="Load Image", command=second_window_logic)
    btn_Open.pack()

    btn_Close = tkinter.ttk.Button(menu, text="Close", command=close_app)
    btn_Close.pack()


    menu.mainloop()
