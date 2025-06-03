import matplotlib.pyplot as plt 
import tkinter as tk
from tkinter import messagebox

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
            summary = "\n".join([f"Day {i + 1}: {temp}°C" for i, temp in enumerate(daytempinfo_float)])
            if messagebox.askyesno("Summary", f"Here's your data:\n\n{summary}\n\nShow the graph?"):
                plt.plot(days, daytempinfo_float, marker='o', label='Temperature')
                plt.title('Temperature over days')
                plt.xlabel('Day')
                plt.ylabel('Temperature in °C')
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

scrn = tk.Label(root, text = "Type in how many days the graph has to cover.")
scrn.grid(row = 2, column = 1)

stp = 0 #step (0 is inputing the number of days in total; 1 is inputing the temps of each day.)
dayttl = 0 #total days
day = 0 #now inputed day
daytempinfo = [] #storing info about temps
days = None #stores how many days in total, later as a list for the graph

txt = tk.Text(root, height = 1, width = 2)
txt.grid(row = 1, column = 1)

submitbtn = tk.Button(root, text = "Submit", command = lambda: submit())
submitbtn.grid(row = 3, column = 1)

menu = tk.Menu(root)
root.config(menu = menu)
options = tk.Menu(menu)
menu.add_cascade(label = "options", menu = options)
options.add_command(label = "clear", command = lambda: cleartxt())

root.mainloop()
