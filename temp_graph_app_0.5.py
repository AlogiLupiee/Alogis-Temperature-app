import matplotlib.pyplot as plt 
import tkinter as tk
from tkinter import messagebox
import webbrowser

def cleartxt():
    txt.delete("1.0", "end")

def submit():
    global stp, day, dayttl, days, temp
    stp += 1
    if stp == 1:
        dayttl = txt.get("1.0", "end-1c")
        try:
            dayttl = int(dayttl)
            if dayttl < 1:
                raise ValueError("The number of days must be at least 1") 
            scrn.config(text = f"Type the temperature of day {day + 1} and choose the weather.")
            cleartxt()
        except ValueError:
            stp -= 1
            messagebox.showerror("Invalid input", "Enter a number of days, that is bigger than 1 and an number.")
            cleartxt()
    else:
        temp_input = txt.get("1.0", "end-1c").strip()
        try:
            temp = float(temp_input)
            daytempinfo.append(txt.get("1.0", "end-1c").strip())
            dayweatherinfo.append(weather.get())
            cleartxt()
            day += 1
            if day == dayttl:
                root.destroy()
                days = list(range(1, int(dayttl) + 1))
                daytempinfo_float = [float(temp.strip()) for temp in daytempinfo]
                fig = plt.figure()
                fig.canvas.manager.set_window_title("Temperature graph")
                unit_l = f"°{unit.get()}"
                summary = "\n".join([f"Day {i + 1}: {temp}{unit_l}, weather: {dayweatherinfo[i]}" for i, temp in enumerate(daytempinfo_float)])
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
                scrn.config(text = f"Type the temperature of day {day + 1} and choose the weather.")
        except ValueError:
            stp -= 1
            messagebox.showerror("Invalid input", "Enter a valid number.")
            cleartxt()

root = tk.Tk()
root.title("Temperature chart")
root.config(bg = "lightblue", pady = 100, padx = 150)

scrn = tk.Label(root, text = "Type in how many days the graph has to cover.", bg = "lightblue")
scrn.grid(row = 2, column = 1)

stp = 0 #step (0 is inputing the number of days in total; 1 is inputing the temps of each day.)
dayttl = 0 #total days
day = 0 #now inputed day
daytempinfo = [] #stores info about temps
dayweatherinfo = []  # stores weather for each day
days = None #stores how many days in total, later as a list for the graph
temp = None
unit = tk.StringVar(value = "C")
weather = tk.StringVar(value="☀️")

unit_label = tk.Label(root, text = "Select unit:", bg = "lightblue")
unit_label.grid(row = 1, column = 0)

c_radio = tk.Radiobutton(root, text = "(°C)", variable = unit, value = "C", width = 2, bg = "lightblue")
c_radio.grid(row = 2, column = 0)
f_radio = tk.Radiobutton(root, text = "(°F)", variable = unit, value = "F", width = 2, bg = "lightblue")
f_radio.grid(row = 3, column = 0)

weather_label = tk.Label(root, text="Select weather:", bg = "lightblue")
weather_label.grid(row=1, column=2)

sunny_radio = tk.Radiobutton(root, text="☀️ Sunny", variable=weather, value="☀️", bg = "yellow")
sunny_radio.grid(row=2, column=2)
cloudy_radio = tk.Radiobutton(root, text="☁️ Cloudy", variable=weather, value="☁️", bg = "gray50")
cloudy_radio.grid(row=3, column=2)
rainy_radio = tk.Radiobutton(root, text="🌧️ Rainy", variable=weather, value="🌧️", bg = "blue")
rainy_radio.grid(row=4, column=2)
snowy_radio = tk.Radiobutton(root, text="❄️ Snowy", variable=weather, value="❄️", bg = "snow")
snowy_radio.grid(row=5, column=2)

txt = tk.Text(root, height = 1, width = 2, bg = "darkblue", fg = "white")
txt.grid(row = 1, column = 1)

submitbtn = tk.Button(root, text = "Submit", command = lambda: submit(), bg = "red")
submitbtn.grid(row = 3, column = 1)

menu = tk.Menu(root)
root.config(menu = menu)
options = tk.Menu(menu)
menu.add_cascade(label = "options", menu = options)
options.add_command(label = "clear", command = lambda: cleartxt())
options.add_separator()
options.add_command(label = "Author", command = lambda: webbrowser.open_new('https://github.com/AlogiLupiee'))

root.mainloop()
