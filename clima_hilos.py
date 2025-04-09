"""Diseñar e implementar un programa que simule una estación meteorológica, capaz de
realizar múltiples tareas simultáneamente mediante el uso de hilos (threads) para garantizar
un funcionamiento eficiente."""

import threading
import time
import random
import csv
from datetime import datetime
from collections import deque
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

datos_climaticos = {"temperatura": 25.0, "humedad": 50.0, "presion": 1013.0}
data_lock = threading.Lock()

historial = {
    "tiempo": deque(maxlen=50),
    "temperatura": deque(maxlen=50),
    "humedad": deque(maxlen=50),
    "presion": deque(maxlen=50)
}

def generar_datos():
    while True:
        with data_lock:

            datos_climaticos["temperatura"] += random.uniform(-2, 2)
            datos_climaticos["humedad"] += random.uniform(-20, 20)
            datos_climaticos["presion"] += random.uniform(-80, 80)

            datos_climaticos["temperatura"] = max(0, min(27, datos_climaticos["temperatura"]))
            datos_climaticos["humedad"] = max(30, min(82, datos_climaticos["humedad"]))
            datos_climaticos["presion"] = max(600, min(751, datos_climaticos["presion"]))
        time.sleep(1)

def registrar_datos():
    with open("datos_climaticos.csv", mode="w", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["Fecha", "Hora", "Temperatura", "Humedad", "Presion"])

    while True:
        with data_lock:
            ahora = datetime.now()
            fila = [
                ahora.date(),
                ahora.strftime("%H:%M:%S"),
                round(datos_climaticos["temperatura"], 2),
                round(datos_climaticos["humedad"], 2),
                round(datos_climaticos["presion"], 2)
            ]
        with open("datos_climaticos.csv", mode="a", newline="") as archivo:
            csv.writer(archivo).writerow(fila)
        time.sleep(1)

def interfaz_grafica():
    def actualizar_grafica():
        with data_lock:
            ahora = datetime.now().strftime("%H:%M:%S")
            historial["tiempo"].append(ahora)
            historial["temperatura"].append(datos_climaticos["temperatura"])
            historial["humedad"].append(datos_climaticos["humedad"])
            historial["presion"].append(datos_climaticos["presion"])

        ax1.clear()
        ax2.clear()
        ax3.clear()

        ax1.plot(historial["tiempo"], historial["temperatura"], color='red')
        ax1.set_title("Temperatura (°C)")
        ax1.set_ylabel("°C")
        ax1.set_xticklabels(historial["tiempo"], rotation=45, ha="right")
        ax1.grid(True)

        ax2.plot(historial["tiempo"], historial["humedad"], color='blue')
        ax2.set_title("Humedad (%)")
        ax2.set_ylabel("%")
        ax2.set_xticklabels(historial["tiempo"], rotation=45, ha="right")
        ax2.grid(True)

        ax3.plot(historial["tiempo"], historial["presion"], color='green')
        ax3.set_title("Presión (hPa)")
        ax3.set_ylabel("hPa")
        ax3.set_xticklabels(historial["tiempo"], rotation=45, ha="right")
        ax3.grid(True)

        descripcion.set(f"Temperatura: {round(datos_climaticos['temperatura'],1)} °C | "
                        f"Humedad: {round(datos_climaticos['humedad'],1)} % | "
                        f"Presión: {round(datos_climaticos['presion'],1)} hPa")

        canvas.draw()
        root.after(1000, actualizar_grafica)

    root = tk.Tk()
    root.title("Estación Meteorológica")

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 8), constrained_layout=True)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    descripcion = tk.StringVar()
    label = ttk.Label(root, textvariable=descripcion, font=("Arial", 14))
    label.pack(pady=10)

    actualizar_grafica()
    root.mainloop()

hilos = [
    threading.Thread(target=generar_datos),
    threading.Thread(target=registrar_datos),
    threading.Thread(target=interfaz_grafica),
]

for hilo in hilos:
    hilo.daemon = True
    hilo.start()

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    print("Programa finalizado.")
