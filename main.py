
# 

import tkinter as tk
import json
import datetime
import os

class HBaseSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HBase Simulator")

        self.input_label = tk.Label(self.root, text="Ingrese comando:")
        self.input_label.pack()

        self.input_entry = tk.Entry(self.root, width=50)
        self.input_entry.pack()
        self.input_entry.bind("<Return>", lambda event: self.execute_command())

        self.submit_button = tk.Button(self.root, text="Ejecutar", command=self.execute_command)
        self.submit_button.pack()

        self.output_text = tk.Text(self.root, height=20, width=80)
        self.output_text.pack()
        
        # Se crea un archivo de historial para tener los comandos ingresados
        self.historial_file = "./data/historial.txt"
        if not os.path.exists(self.historial_file):
            with open(self.historial_file, "w") as f:
                f.write("Comandos ingresados:\n")

    def execute_command(self):
        command = self.input_entry.get()
        timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
        # Se evalua si se limpiará o cerrara la "terminal"
        if command == "clear":
            self.output_text.delete('1.0', tk.END)
            
        elif command.lower() == "exit":
            self.root.quit()

        # Aquí podrías procesar el comando y obtener los resultados
        # En este ejemplo, simplemente lo mostraremos en la pantalla
        prueba = None
        with open("./data/HFile.json") as archivo:
            # Se leen Regions con HFiles
            prueba = json.load(archivo)

            cs = command.split(" ")
            cm = cs[0].lower() # Comando Separado
            
            # Escribir el comando en el archivo de historial
            with open(self.historial_file, "a") as f:
                f.write(f"{timestamp}: {command}\n")

            if(cm == "create"):
                pass

            elif(cm == "list"):
                pass  

            elif(cm == "disable"):
                pass  
            
            elif(cm == "isEnabled"):
                pass  
            
            elif(cm == "alter"):
                pass  

            elif (cm == "drop"):
                self.output_text.insert(tk.END, "Es un put: " + cm + " \n")

            elif (cm == "drop_all"):
                self.output_text.insert(tk.END, "Es un put: " + cm + " \n")

            elif (cm == "describe"):
                self.output_text.insert(tk.END, "Es un put: " + cm + " \n")

            elif (cm == "put"):
                self.output_text.insert(tk.END, "Es un put: " + cm + " \n")

            elif (cm == "get"):
                self.output_text.insert(tk.END, "Es un put: " + cm + " \n")

            elif (cm == "scan"):
                self.output_text.insert(tk.END, "Es un put: " + cm + " \n")

            elif (cm == "delete"):
                self.output_text.insert(tk.END, "Es un put: " + cm + " \n")
                
            elif (cm == "delete_all"):
                self.output_text.insert(tk.END, "Es un put: " + cm + " \n")

            elif (cm == "count"):
                self.output_text.insert(tk.END, "Es un put: " + cm + " \n")
                
            elif (cm == "truncate"):
                self.output_text.insert(tk.END, "Es un put: " + cm + " \n")

            else:
                if cm == "clear":
                    self.output_text.delete('1.0', tk.END)
                else:
                    self.output_text.insert(tk.END, "Comando desconocido" +"\n")
        
        self.input_entry.delete(0, tk.END)
        
if __name__ == "__main__":
    hbase_simulator = HBaseSimulator()
    hbase_simulator.root.mainloop()
    