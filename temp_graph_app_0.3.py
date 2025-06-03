import matplotlib.pyplot as plt 
import tkinter as tk
from tkinter import messagebox
import webbrowser

def cleartxt():
    txt.delete("1.0", "end")

def submit():
    global stp, day, dayttl, days
    stp += 1
    if stp == 1:
        dayttl = txt.get("1.0", "end-1c")
        dayttl = int(dayttl)
        scrn.config(text = f"Type the temperature of day {day + 1}.")
        cleartxt()
    else:
        daytempinfo.append(txt.get("1.0", "end-1c").strip())
        cleartxt()
        day += 1
        if day == dayttl:
            root.destroy()
            days = list(range(1, int(dayttl) + 1))
            daytempinfo_float = [float(temp.strip()) for temp in daytempinfo]
            fig = plt.figure()
            fig.canvas.manager.set_window_title("Temperature graph")
            unit_l = f"°{unit.get()}"
            summary = "\n".join([f"Day {i + 1}: {temp}{unit_l}" for i, temp in enumerate(daytempinfo_float)])
            if messagebox.askyesno("Summary", f"Here's your data:\n\n{summary}\n\nShow the graph?"):
                plt.plot(days, daytempinfo_float, marker='o', label='Temperature')
                plt.title('Temperature over days')
                plt.xlabel('Day')
                plt.ylabel(f'Temperature in {unit_l}')
                plt.grid(True)
                plt.xticks(days)
                plt.show()
            else:
                root.quit()
        else:
            scrn.config(text = f"Type the temperature of day {day + 1}.")

root = tk.Tk()
root.title("Temperature chart")
root.config(bg = "lightblue", pady = 100, padx = 150)

scrn = tk.Label(root, text = "Type in how many days the graph has to cover.", bg = "lightblue")
scrn.grid(row = 2, column = 1)

stp = 0 #step (0 is inputing the number of days in total; 1 is inputing the temps of each day.)
dayttl = 0 #total days
day = 0 #now inputed day
daytempinfo = [] #storing info about temps
days = None #stores how many days in total, later as a list for the graph
unit = tk.StringVar(value = "C")

unit_label = tk.Label(root, text = "Select unit:", bg = "lightblue")
unit_label.grid(row = 1, column = 0)

c_radio = tk.Radiobutton(root, text = "(°C)", variable = unit, value = "C", width = 2, bg = "lightblue")
c_radio.grid(row = 2, column = 0)
f_radio = tk.Radiobutton(root, text = "(°F)", variable = unit, value = "F", width = 2, bg = "lightblue")
f_radio.grid(row = 3, column = 0)

txt = tk.Text(root, height = 1, width = 2, bg = "darkblue", fg = "white")
txt.grid(row = 1, column = 1)

submitbtn = tk.Button(root, text = "Submit", command = lambda: submit(), bg = "orange1")
submitbtn.grid(row = 3, column = 1)

menu = tk.Menu(root)
root.config(menu = menu)
options = tk.Menu(menu)
menu.add_cascade(label = "options", menu = options)
options.add_command(label = "clear", command = lambda: cleartxt())
options.add_separator()
options.add_command(label = "Author", command = lambda: webbrowser.open_new('https://github.com/AlogiLupiee'))

root.mainloop()
