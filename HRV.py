import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# --- MEDICAL LOGIC FUNCTION ---
def generate_ecg():
    try:
        user_bpm = float(entry.get())
        
        if user_bpm > 100:
            status, color = "Tachycardia", "red"
        elif user_bpm < 60:
            status, color = "Bradycardia", "blue"
        else:
            status, color = "Normal Sinus Rhythm", "green"

        # Math for realistic waves
        time = np.linspace(0, 5, 2000)
        signal = np.zeros_like(time)
        
        def heart_bump(t, center, width, height):
            return height * np.exp(-((t - center)**2) / (2 * width**2))

        seconds_per_beat = 60 / user_bpm
        peak_times = np.arange(0.2, 5, seconds_per_beat)

        for pt in peak_times:
            signal += heart_bump(time, pt - 0.1, 0.03, 0.2)   # P wave
            signal += heart_bump(time, pt, 0.015, 1.5)        # QRS complex
            signal += heart_bump(time, pt + 0.15, 0.05, 0.4)  # T wave
        
        signal += np.random.normal(0, 0.02, len(time)) # Noise

        # Update the Plot
        ax.clear()
        ax.plot(time, signal, color=color)
        ax.set_title(f"ECG Simulation: {status} ({user_bpm} BPM)")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Voltage (mV)")
        canvas.draw()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for BPM")

# --- GUI SETUP ---
root = tk.Tk()
root.title("BME Heart Monitor Simulator")

# Input Frame
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Enter Patient BPM:").pack(side=tk.LEFT)
entry = tk.Entry(frame)
entry.pack(side=tk.LEFT, padx=5)
btn = tk.Button(frame, text="Run Analysis", command=generate_ecg)
btn.pack(side=tk.LEFT)

# Graph Area
fig, ax = plt.subplots(figsize=(8, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()