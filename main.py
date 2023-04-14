
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
        
        if command == 'clear':
            self.output_text.delete('1.0', tk.END)

        # Aquí podrías procesar el comando y obtener los resultados
        # En este ejemplo, simplemente lo mostraremos en la pantalla
        prueba = None
        with open("./HFile.json") as archivo:
            # Se leen Regions con HFiles
            prueba = json.load(archivo)

            cs = command.split(" ")
            cm = cs[0].lower() # Comando Separado
            print(cm)

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
                self.output_text.insert(tk.END, "Comando desconocido" +"\n")
        
if __name__ == "__main__":
    hbase_simulator = HBaseSimulator()
    hbase_simulator.root.mainloop()
    