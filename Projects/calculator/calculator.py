import tkinter as tk

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.geometry("450x450")
        master.config(bg="gray")

        self.total = tk.StringVar(value="0")
        self.entered_number = tk.StringVar(value="")

        tk.Label(master, textvariable=self.total, font=("Helvetica", 14), bg="gray").grid(row=0, column=0, columnspan=4)
        tk.Entry(master, textvariable=self.entered_number, font=("Helvetica", 14), bg="lightgray").grid(row=1, column=0, columnspan=4)

        for i, symbol in enumerate("C  ÷789x456-123+0 .="):
            if symbol == " ":
                tk.Label(self.master, text="").grid(row=2 + i//4, column=i%4)
            else:
                tk.Button(self.master, text=symbol, padx=40, pady=20, font=("Helvetica", 14), bg="lightgray", command=lambda s=symbol: self.button_click(s)).grid(row=2 + i//4, column=i%4)

    def button_click(self, symbol):
        if symbol == "=":
            try:
                self.total.set(eval(self.entered_number.get()))
                self.entered_number.set("")
            except:
                self.total.set("Error")
                self.entered_number.set("")
        elif symbol == "C":
            self.total.set("0")
            self.entered_number.set("")
        else:
            self.entered_number.set(self.entered_number.get() + symbol)

root = tk.Tk()
calc = Calculator(root)
root.mainloop()
