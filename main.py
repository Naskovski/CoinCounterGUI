import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from detector import detectCoins
import customtkinter as ctk
from PIL import Image, ImageTk


def second_window_logic():
    def update_canvas():
        x = int(canvas.winfo_width()/2) if canvas.winfo_height()>1 else 393
        y = int(canvas.winfo_height()/2) if canvas.winfo_height()>1 else 375

        canvas.delete("all")
        canvas.create_image(x, y, anchor="center", image=images[0])
        for i, var in checkbox_vars.items():
            if var.get() == 1:
                canvas.create_image(x, y, anchor="center", image=images[i])

    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if file_path:
        detectCoins(file_path)

        # Read .txt file
        with open("./assets/results.txt", "r") as file:
            content = file.read()

        # Layout
        coin_window = ctk.CTkToplevel(menu)
        coin_window.title("CoinCounter")
        coin_window.geometry("900x600")

        coin_window.columnconfigure(0, weight=2)
        coin_window.columnconfigure(1, weight=1)
        coin_window.rowconfigure(0, weight=1)
        coin_window.rowconfigure(1, weight=3)

        # total value
        total_value_display = ctk.CTkFrame(coin_window)
        lines = content.splitlines()
        total_value = lines[0][13:]

        total_value_lbl = ctk.CTkLabel(total_value_display, text=total_value, font=("Helvetica", 50), justify="center")
        total_value_lbl.pack(side="top", anchor="n", padx=10, pady=10)

        denari_lbl = ctk.CTkLabel(total_value_display, text="Денари", font=("Helvetica", 25), justify="center")
        denari_lbl.pack(pady=10)

        total_value_display.grid(row=0, column=1)

        #image display
        canvas = tkinter.Canvas(coin_window, background="black", borderwidth=0, highlightthickness=0)
        canvas.grid(row=0, column=0, rowspan=2, sticky="nsew")

        #checkbox
        images = {}

        checkbox_frame = ctk.CTkFrame(coin_window)
        checkbox_vars = {}
        j = 0
        for i in [0, 1, 2, 5, 10, 50]:
            coin_image = Image.open("./assets/result" + str(i) + ".png")
            image_height = 750
            image_width = int(coin_image.width * (image_height / coin_image.height))
            coin_image = coin_image.resize((image_width, image_height))
            images[i] = ImageTk.PhotoImage(coin_image)
            if i > 0:
                text = str(i) + (" денар: " if i==1 else " денари: " )+ lines[j + 3][:2]
                var = ctk.IntVar(value=1)
                checkbox = ctk.CTkCheckBox(checkbox_frame, text=text, variable=var, command=update_canvas)
                checkbox.pack(anchor="w")
                checkbox_vars[i] = var
                j+=1


        checkbox_frame.grid(row=1, column=1)
        update_canvas()
        coin_window.mainloop()
        update_canvas()


def close_app():
    menu.destroy()


if __name__ == '__main__':
    menu = ctk.CTk()
    menu.title("CoinCounter")
    menu.geometry("300x350")

    logo_img = Image.open("./logo.png")
    logo = ctk.CTkImage(light_image = logo_img,
                        dark_image = logo_img,
                        size = (93, 93))

    logo_lbl = ctk.CTkLabel(menu, text="", image=logo)
    logo_lbl.pack(side="top", padx=50, pady=20)

    heading = ctk.CTkLabel(menu, text="CoinCounter", font=("Helvetica", 40))
    heading.pack(padx=20, pady=10)

    btn_Open = ctk.CTkButton(menu, text="Вчитај Слика", command=second_window_logic)
    btn_Open.pack(pady=10)

    btn_Close = ctk.CTkButton(menu, text="Затвори", command=close_app)
    btn_Close.pack(pady=10)


    menu.mainloop()
