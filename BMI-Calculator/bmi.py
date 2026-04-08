import tkinter as tk
from tkinter import messagebox

# 🎯 Calculate BMI
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get()) / 100  # cm → meters

        if weight <= 0 or height <= 0:
            raise ValueError

        bmi = weight / (height ** 2)

        # 🧠 Category
        if bmi < 18.5:
            category = "Underweight 😟"
            tip = "Eat more nutritious food 🍎"
        elif 18.5 <= bmi < 25:
            category = "Normal 😊"
            tip = "Keep it up! 💪"
        elif 25 <= bmi < 30:
            category = "Overweight 😐"
            tip = "Exercise regularly 🏃"
        else:
            category = "Obese 😟"
            tip = "Consult a doctor 🩺"

        result = f"Your BMI: {bmi:.2f}\n\nCategory: {category}\n{tip}"
        result_label.config(text=result)

    except:
        messagebox.showerror("Error", "Enter valid numbers!")

# 🎨 UI
root = tk.Tk()
root.title("BMI Calculator 💪")
root.geometry("400x500")
root.config(bg="#0f172a")

frame = tk.Frame(root, bg="#0f172a")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title
tk.Label(frame, text="BMI Calculator",
         font=("Segoe UI", 22, "bold"),
         fg="white", bg="#0f172a").pack(pady=10)

# Weight
tk.Label(frame, text="Weight (kg)",
         font=("Segoe UI", 12),
         fg="#cbd5f5", bg="#0f172a").pack()

weight_entry = tk.Entry(frame,
                        font=("Segoe UI", 14),
                        bg="#1e293b", fg="white",
                        justify="center")
weight_entry.pack(pady=5)

# Height
tk.Label(frame, text="Height (cm)",
         font=("Segoe UI", 12),
         fg="#cbd5f5", bg="#0f172a").pack()

height_entry = tk.Entry(frame,
                        font=("Segoe UI", 14),
                        bg="#1e293b", fg="white",
                        justify="center")
height_entry.pack(pady=5)

# Button
tk.Button(frame, text="Calculate BMI",
          font=("Segoe UI", 12, "bold"),
          bg="#38bdf8", fg="black",
          activebackground="#0ea5e9",
          relief="flat", padx=10, pady=5,
          command=calculate_bmi).pack(pady=15)

# Result
result_label = tk.Label(frame, text="",
                        font=("Segoe UI", 14),
                        fg="#e2e8f0", bg="#0f172a",
                        justify="center")
result_label.pack(pady=20)

root.mainloop()
