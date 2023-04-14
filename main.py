
# 

import tkinter as tk
import json

class HBaseSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HBase Simulator")

        self.input_label = tk.Label(self.root, text="Ingrese comando:")
        self.input_label.pack()

        self.input_entry = tk.Entry(self.root, width=50)
        self.input_entry.pack()

        self.submit_button = tk.Button(self.root, text="Ejecutar", command=self.execute_command)
        self.submit_button.pack()

        self.output_text = tk.Text(self.root, height=20, width=80)
        self.output_text.pack()

    def execute_command(self):
        command = self.input_entry.get()
        # Aquí podrías procesar el comando y obtener los resultados
        # En este ejemplo, simplemente lo mostraremos en la pantalla
        prueba = None
        with open("./HFile.json") as archivo:
            prueba = json.load(archivo)
            print(prueba)
        
if __name__ == "__main__":
    hbase_simulator = HBaseSimulator()
    hbase_simulator.root.mainloop()
    