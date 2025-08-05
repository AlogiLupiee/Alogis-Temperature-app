import matplotlib.pyplot as plt 
import tkinter as tk
from tkinter import messagebox, ttk
from webbrowser import open_new
import datetime as dt

def update_humidity_label(value):
    humidity_display_label.config(text = f"{int(float(value))}%")

def toggle_inputs():
    if include_pressure.get():
        pressure_entry.config(state = "normal")
    else:
        pressure_entry.config(state = "disabled")
    if include_humidity.get():
        humidity_slider.config(state = "normal")
        humidity_display_label.config(state = "normal")
        update_humidity_label(humidity_var.get())
    else:
        humidity_slider.config(state = "disabled")
        humidity_display_label.config(state = "disabled")

# shows graph and asks to save data
def graph_show():
    root.withdraw() 
    
    days = list(range(1, dayttl + 1))
    daytempinfo_float = [float(temp.strip()) for temp in daytempinfo]
    unit_l = f"°{unit.get()}"
    summary_days = []
    
    for i in range(dayttl):
        line = f"Day {i + 1}: {daytempinfo_float[i]}{unit_l}"
        if daypressureinfo[i] != "N/A":
            line += f", Pressure: {daypressureinfo[i]} hPa"
        if dayhumidityinfo[i] != "N/A":
            line += f", Humidity: {dayhumidityinfo[i]}%"
        line += f", Weather: {dayweatherinfo[i]}"
        summary_days.append(line)
        
    summary = "\n".join(summary_days)
    
    if messagebox.askyesno("Summary", f"Here's your data:\n\n{summary}\n\nShow the graph?"):
        plt.figure().canvas.manager.set_window_title("Temperature graph")
        plt.plot(days, daytempinfo_float, marker = 'o', label = 'Temperature')
        plt.title('Temperature over days')
        plt.xlabel('Day')
        plt.ylabel(f'Temperature in {unit_l}')
        plt.grid(True)
        plt.xticks(days)
        plt.tight_layout()
        plt.show()
        
        if messagebox.askyesno("Export to text file?", "Click yes if you want your info to be saved to a .txt file?"):
            try:
                daytime = dt.datetime.now()
                timestamp_entry = f"--- {daytime.strftime('%x')} @ {daytime.strftime('%X')} ---"
                with open("Temperature_info.txt", "a", encoding = "utf-8") as f:
                    f.write(f"{timestamp_entry}\n{summary}\n\n")
                messagebox.showinfo("Success", "Information successfully saved to Temperature_info.txt")
            except Exception as e:
                messagebox.showerror("Error Saving File", f"An error occurred while saving: {e}")
    root.quit()

# clears input window 
def cleartxt():
    txt.delete("1.0", "end")
    pressure_entry.delete(0, "end")

# all the operations after submitting
def submit():
    global stp, day, dayttl, temp
    stp += 1
    if stp == 1:
        dayttl_input = txt.get("1.0", "end-1c")
        try:
            dayttl = int(dayttl_input)
            if dayttl < 1:
                raise ValueError("The number of days must be at least 1") 
            if dayttl > 20:
                if not messagebox.askokcancel("Too many days", f"Are you sure you want to input {dayttl} days?\nThis might be a long process."):
                    dayttl = 0
                    stp -= 1
                    cleartxt()
                else:
                    scrn.config(text = f"Type the temperature of day {day + 1} and choose the weather.")
                    cleartxt()
            else:
                scrn.config(text = f"Type the temperature of day {day + 1} and choose the weather.")
                cleartxt()
        except ValueError:
            stp -= 1
            messagebox.showerror("Invalid input", "Please enter a whole number greater than 0.")
            cleartxt()
    else:
        try:
            temp = float(txt.get("1.0", "end-1c").strip())
            if include_pressure.get():
                pressure_val = float(pressure_entry.get().strip())
                daypressureinfo.append(pressure_val)
            else:
                daypressureinfo.append("N/A")
            if include_humidity.get():
                dayhumidityinfo.append(humidity_var.get())
            else:
                dayhumidityinfo.append("N/A")
            
            daytempinfo.append(str(temp))
            dayweatherinfo.append(weather.get())
            cleartxt()
            day += 1
            if day == dayttl:
                graph_show()
            else:
                scrn.config(text = f"Type the temperature of day {day + 1} and choose the weather.")
        except ValueError:
            messagebox.showerror("Invalid input", "Please ensure Temperature and Pressure are valid numbers.")

# root
root = tk.Tk()
root.title("Temperature Chart")
root.config(bg = "lightblue", pady = 20, padx = 20)

# main screen for showing commands
scrn = tk.Label(root, text = "Type in how many days the graph has to cover.", bg = "lightblue")
scrn.grid(row = 0, column = 1, columnspan = 3)

stp = 0 
dayttl = 0
day = 0 
daytempinfo = [] 
dayweatherinfo = []  
temp = None
unit = tk.StringVar(value = "C")
weather = tk.StringVar(value = "☀️")

daypressureinfo = []
dayhumidityinfo = []
include_pressure = tk.BooleanVar()
include_humidity = tk.BooleanVar()
humidity_var = tk.IntVar(value = 50)

# unit Selection (Column 0)
unit_frame = tk.Frame(root, bg = "lightblue", padx = 10)
unit_frame.grid(row = 1, column = 0, sticky = "ns")
unit_label = tk.Label(unit_frame, text = "Select unit:", bg = "lightblue")
unit_label.pack()
c_radio = tk.Radiobutton(unit_frame, text = "(°C)", variable = unit, value = "C", bg = "lightblue")
c_radio.pack(anchor = "w")
f_radio = tk.Radiobutton(unit_frame, text = "(°F)", variable = unit, value = "F", bg = "lightblue")
f_radio.pack(anchor = "w")

# main Input (Column 1)
main_input_frame = tk.Frame(root, bg = "lightblue", padx = 10)
main_input_frame.grid(row = 1, column = 1)
temp_label = tk.Label(main_input_frame, text = "Temperature:", bg = "lightblue")
temp_label.pack()
txt = tk.Text(main_input_frame, height = 1, width = 10, bg = "darkblue", fg = "white")
txt.pack()

# weather Selection (Column 2)
weather_frame = tk.Frame(root, bg = "lightblue", padx = 10)
weather_frame.grid(row = 1, column = 2, sticky = "ns")
weather_label = tk.Label(weather_frame, text = "Select weather:", bg = "lightblue")
weather_label.pack()
sunny_radio = tk.Radiobutton(weather_frame, text = "☀️ Sunny", variable = weather, value = "☀️", bg = "yellow")
sunny_radio.pack(anchor = "w")
cloudy_radio = tk.Radiobutton(weather_frame, text = "☁️ Cloudy", variable = weather, value = "☁️", bg = "gray50")
cloudy_radio.pack(anchor = "w")
rainy_radio = tk.Radiobutton(weather_frame, text = "🌧️ Rainy", variable = weather, value = "🌧️", bg = "blue")
rainy_radio.pack(anchor = "w")
snowy_radio = tk.Radiobutton(weather_frame, text = "❄️ Snowy", variable = weather, value = "❄️", bg = "snow")
snowy_radio.pack(anchor = "w")

# optional Data Inputs (Column 4)
optional_frame = tk.Frame(root, bg = "lightblue", padx = 20)
optional_frame.grid(row = 1, column = 4, sticky = "ns")

info_label = tk.Label(optional_frame, text = "Include Info:", bg = "lightblue")
info_label.grid(row = 0, column = 0, columnspan = 3, pady = (0,5))

# pressure widgets
pressure_check = tk.Checkbutton(optional_frame, text = "Pressure (hPa)", variable = include_pressure, bg = "lightblue", command = toggle_inputs)
pressure_check.grid(row = 1, column = 0, sticky = "w")
pressure_entry = tk.Entry(optional_frame, width = 10, state = "disabled")
pressure_entry.grid(row = 1, column = 1, columnspan = 2)

# humidity widgets
humidity_check = tk.Checkbutton(optional_frame, text = "Humidity (%)", variable = include_humidity, bg = "lightblue", command = toggle_inputs)
humidity_check.grid(row = 2, column = 0, sticky = "w", pady = (5,0))
humidity_slider = ttk.Scale(optional_frame, from_ = 0, to = 100, orient = "horizontal", variable = humidity_var, state = "disabled", command = update_humidity_label)
humidity_slider.grid(row = 2, column = 1, pady = (5,0))
humidity_display_label = tk.Label(optional_frame, text = "50%", bg = "lightblue", width = 4)
humidity_display_label.grid(row = 2, column = 2, pady = (5,0), sticky = "w")

# submit Button
submitbtn = tk.Button(root, text = "Submit", command = submit, bg = "red", fg = "white")
submitbtn.grid(row = 2, column = 1)

# menu
menu = tk.Menu(root)
root.config(menu = menu)
options = tk.Menu(menu, tearoff = 0)
menu.add_cascade(label = "Options", menu = options)
options.add_command(label = "Clear", command = cleartxt)
options.add_separator()
options.add_command(label = "Author", command = lambda: open_new('https://github.com/AlogiLupiee'))

toggle_inputs()

root.mainloop()

# © 2025 Alogi. All Rights Reserved. | version 1.4 | WiP, possible bugs