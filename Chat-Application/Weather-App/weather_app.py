import tkinter as tk
from tkinter import messagebox
import requests
import geocoder
from PIL import Image, ImageTk

#  Your API key (already added)
API_KEY = "48917ba0dc3fef8d205d66ec4e4d86f9"


#  Get Location
def get_location():
    try:
        g = geocoder.ip('me')
        return g.city if g.city else None
    except:
        return None


#  Get Weather Icon
def get_icon(icon_code):
    url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    img_data = requests.get(url).content

    with open("icon.png", "wb") as f:
        f.write(img_data)

    return "icon.png"


#  Get Weather
def get_weather():
    city = city_entry.get().strip()

    if city == "":
        city = get_location()

    if not city:
        messagebox.showerror("Error", "Location not found")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        res = requests.get(url)
        data = res.json()

        if str(data.get("cod")) != "200":
            messagebox.showerror("Error", "City not found")
            return

        temp = data["main"]["temp"]
        weather = data["weather"][0]["main"]
        humidity = data["main"]["humidity"]
        icon_code = data["weather"][0]["icon"]

        # Icon
        icon_path = get_icon(icon_code)
        img = Image.open(icon_path)
        img = ImageTk.PhotoImage(img)

        icon_label.config(image=img, bg="#0f172a")
        icon_label.image = img

        #  Mood messages
        if weather == "Clear":
            mood = "😎 Bright sunny day!"
        elif weather == "Clouds":
            mood = "☁️ Cloudy and calm!"
        elif weather == "Rain":
            mood = "🌧️ Take an umbrella!"
        elif weather == "Mist":
            mood = "🌫️ Low visibility!"
        else:
            mood = "🌍 Have a great day!"

        result = f"📍 {city}\n\n🌡 {temp}°C\n☁ {weather}\n💧 {humidity}%\n\n{mood}"

        result_label.config(text=result)

    except Exception as e:
        messagebox.showerror("Error", str(e))


#  UI
root = tk.Tk()
root.title("Ultimate Weather App 🌤️")
root.geometry("420x550")
root.config(bg="#0f172a")

frame = tk.Frame(root, bg="#0f172a")
frame.place(relx=0.5, rely=0.5, anchor="center")

#  Clouds
cloud_label = tk.Label(root, text="☁️ ☁️ ☁️",
                       font=("Segoe UI", 20),
                       bg="#0f172a", fg="white")
cloud_label.pack(pady=5)

# Title
title = tk.Label(frame, text="Weather App",
                 font=("Segoe UI", 22, "bold"),
                 fg="#ffffff", bg="#0f172a")
title.pack(pady=10)

# Entry
city_entry = tk.Entry(frame,
                      font=("Segoe UI", 14),
                      width=25,
                      justify="center",
                      bg="#1e293b",
                      fg="white",
                      insertbackground="white")
city_entry.pack(pady=10)

# Button
tk.Button(frame, text="Get Weather",
          font=("Segoe UI", 12, "bold"),
          bg="#38bdf8", fg="black",
          activebackground="#0ea5e9",
          relief="flat", padx=10, pady=5,
          command=get_weather).pack(pady=10)

# Icon
icon_label = tk.Label(frame, bg="#0f172a")
icon_label.pack()

# Result
result_label = tk.Label(frame, text="",
                        font=("Segoe UI", 14),
                        fg="#e2e8f0", bg="#0f172a",
                        justify="center")
result_label.pack(pady=20)

root.mainloop()
