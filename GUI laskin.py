### GUI laskin, credit NeuralNine
###
import tkinter as tk

laskutoimitus = ""

def lisää_laskutoimitus(symboli):
    global laskutoimitus
    laskutoimitus += str(symboli)
    teksti_tulos.delete(1.0, "end")
    teksti_tulos.insert(1.0, laskutoimitus)
    
def evaluaatio():
    global laskutoimitus
    try:
        laskutoimitus = str(eval(laskutoimitus))
        teksti_tulos.delete(1.0, "end")
        teksti_tulos.insert(1.0, laskutoimitus )
    except:
        clear_field()
        teksti_tulos.insert(1.0, "Virhetapahtuma")

    
def tyhjennä_alue():
    global laskutoimitus
    laskutoimitus = ""
    teksti_tulos.delete(1.0, "end")

root = tk.Tk()
root.geometry("300x275")
teksti_tulos = tk.Text(root, height=2, width=16, font=("Arial", 24), fg="white", bg="Black")
teksti_tulos.grid(columnspan=5)


nappi1 = tk.Button(root, text="1", command=lambda: lisää_laskutoimitus(1), width=5, font=("Arial", 14), fg="white", bg="black")
nappi1.grid(row=2, column=1)
nappi2 = tk.Button(root, text="2", command=lambda: lisää_laskutoimitus(2), width=5, font=("Arial", 14), fg="white", bg="black")
nappi2.grid(row=2, column=2)
nappi3 = tk.Button(root, text="3", command=lambda: lisää_laskutoimitus(3), width=5, font=("Arial", 14), fg="white", bg="black")
nappi3.grid(row=2, column=3)
nappi4 = tk.Button(root, text="4", command=lambda: lisää_laskutoimitus(4), width=5, font=("Arial", 14), fg="white", bg="black")
nappi4.grid(row=3, column=1)
nappi5 = tk.Button(root, text="5", command=lambda: lisää_laskutoimitus(5), width=5, font=("Arial", 14), fg="white", bg="black")
nappi5.grid(row=3, column=2)
nappi6 = tk.Button(root, text="6", command=lambda: lisää_laskutoimitus(6), width=5, font=("Arial", 14), fg="white", bg="black")
nappi6.grid(row=3, column=3)
nappi7 = tk.Button(root, text="7", command=lambda: lisää_laskutoimitus(7), width=5, font=("Arial", 14), fg="white", bg="black")
nappi7.grid(row=4, column=1)
nappi8 = tk.Button(root, text="8", command=lambda: lisää_laskutoimitus(8), width=5, font=("Arial", 14), fg="white", bg="black")
nappi8.grid(row=4, column=2)
nappi9 = tk.Button(root, text="9", command=lambda: lisää_laskutoimitus(9), width=5, font=("Arial", 14), fg="white", bg="black")
nappi9.grid(row=4, column=3)
nappi0 = tk.Button(root, text="0", command=lambda: lisää_laskutoimitus(0), width=5, font=("Arial", 14), fg="white", bg="black")
nappi0.grid(row=5, column=2)
nappi_plus = tk.Button(root, text="+", command=lambda: lisää_laskutoimitus("+"), width=5, font=("Arial", 14), fg="white", bg="black")
nappi_plus.grid(row=2, column=4)
nappi_minus = tk.Button(root, text="-", command=lambda: lisää_laskutoimitus("-"), width=5, font=("Arial", 14), fg="white", bg="black")
nappi_minus.grid(row=3, column=4)
nappi_kerto = tk.Button(root, text="*", command=lambda: lisää_laskutoimitus("*"), width=5, font=("Arial", 14), fg="white", bg="black")
nappi_kerto.grid(row=4, column=4)
nappi_jako = tk.Button(root, text="/", command=lambda: lisää_laskutoimitus("/"), width=5, font=("Arial", 14), fg="white", bg="black")
nappi_jako.grid(row=5, column=4)
nappi_sulku1 = tk.Button(root, text="(", command=lambda: lisää_laskutoimitus("("), width=5, font=("Arial", 14), fg="white", bg="black")
nappi_sulku1.grid(row=5, column=1)
nappi_sulku2 = tk.Button(root, text=")", command=lambda: lisää_laskutoimitus(")"), width=5, font=("Arial", 14), fg="white", bg="black")
nappi_sulku2.grid(row=5, column=3)
nappi_tyhjennä = tk.Button(root, text="C", command=tyhjennä_alue, width=11, font=("Arial", 14), fg="white", bg="black")
nappi_tyhjennä.grid(row=6, column=3, columnspan=2)
nappi_tulos = tk.Button(root, text="=", command=evaluaatio, width=11, font=("Arial", 14), fg="white", bg="black")
nappi_tulos.grid(row=6, column=1, columnspan=2)
root.mainloop()
