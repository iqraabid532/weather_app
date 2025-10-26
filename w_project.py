
import requests
import json
import tkinter as tk
from tkinter import messagebox, ttk


API_KEY = "55f1c879a124b19404c49a3f4626ab66"  
BASE_URL = "https://api.openweathermap.org/data/2.5/"


def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter city name!")
        return

    mode = mode_var.get()
    url = BASE_URL + ("weather" if mode == "current" else "forecast")
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200:
            messagebox.showerror("Error", data.get("message", "Something went wrong"))
            return

        output_box.delete(1.0, tk.END)

        if mode == "current":
            show_current(data)
        else:
            show_forecast(data)

        if save_var.get():
            save_history(city, data, mode)

    except Exception as e:
        messagebox.showerror("Network Error", f"Failed to connect: {e}")

def show_current(data):
    weather = data["weather"][0]["description"].capitalize()
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]

    result = (
        f"🌤️ Current Weather in {data['name']}\n"
        f"Condition: {weather}\n"
        f"Temperature: {temp} °C\n"
        f"Humidity: {humidity}%\n"
        f"Wind Speed: {wind} m/s\n"
    )
    output_box.insert(tk.END, result)

def show_forecast(data):
    output_box.insert(tk.END, f"📅 5-Day Forecast for {data['city']['name']}\n\n")
    forecasts = data["list"]
    shown_dates = set()

    for entry in forecasts:
        date = entry["dt_txt"].split(" ")[0]
        if date not in shown_dates:
            shown_dates.add(date)
            desc = entry["weather"][0]["description"].capitalize()
            temp = entry["main"]["temp"]
            output_box.insert(tk.END, f"{date}: {desc}, {temp}°C\n")

def save_history(city, data, mode):
    try:
        with open("weather_history.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    entry = {
        "city": city,
        "mode": mode,
        "data": data,
    }
    history.append(entry)

    with open("weather_history.json", "w") as f:
        json.dump(history, f, indent=2)

    messagebox.showinfo("Saved", "Weather data saved successfully!")


root = tk.Tk()
root.title("🌦️ Weather App by iqra abid ")
root.geometry("400x500")

tk.Label(root, text="Enter City:", font=("Arial", 12, "bold")).pack(pady=5)
city_entry = tk.Entry(root, font=("Arial", 12), width=25)
city_entry.pack(pady=5)

mode_var = tk.StringVar(value="current")
tk.Label(root, text="Choose Mode:").pack(pady=5)
ttk.Radiobutton(root, text="Current Weather", variable=mode_var, value="current").pack()
ttk.Radiobutton(root, text="5-Day Forecast", variable=mode_var, value="forecast").pack()

save_var = tk.BooleanVar()
tk.Checkbutton(root, text="💾 Save to history", variable=save_var).pack(pady=5)

tk.Button(root, text="Get Weather", command=get_weather, bg="#4CAF50", fg="white",
          font=("Arial", 12, "bold"), width=20).pack(pady=10)

output_box = tk.Text(root, wrap="word", height=15, width=40, font=("Arial", 10))
output_box.pack(pady=10)

root.mainloop()