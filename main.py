
# 

import tkinter as tk
import json
import datetime
import os


from dml.functions import *

class HBaseSimulator:
    def __init__(self):
        
        self.db = "./data/HFile.json"
        
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
        # self.output_text.config(state=tk.DISABLED)
        
        # Se crea un archivo de historial para tener los comandos ingresados
        self.historial_file = "./data/historial.txt"
        if not os.path.exists(self.historial_file):
            with open(self.historial_file, "w") as f:
                f.write("-----------------------\n")
                f.write("Comandos ingresados:\n")
        else:
            with open(self.historial_file, "a") as f:
                f.write("-----------------------\n")
                f.write("Comandos ingresados:\n")
                
    def show_results(self, value):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, value + "\n")
        self.output_text.config(state=tk.DISABLED)

    def execute_command(self):
        command = self.input_entry.get()
        timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
        # Se evalua si se limpiará o cerrara la "terminal"
        if command == "clear":
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete('1.0', tk.END)
            self.output_text.config(state=tk.DISABLED)
            
        elif command.lower() == "exit":
            self.root.quit()

        # Aquí podrías procesar el comando y obtener los resultados
        # En este ejemplo, simplemente lo mostraremos en la pantalla
        data = None
        with open(self.db) as archivo:
            # Se leen Regions con HFiles
            data = json.load(archivo)

            cs = command.split(" ")
            cm = cs[0].lower() # Comando Separado
            
            # Escribir el comando en el archivo de historial
            with open(self.historial_file, "a") as f:
                f.write(f"{timestamp}: {command}\n")

            print(cm)

            if(cm == "create"):
                timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                n = len(data) + 1
                nameRegion = "Region"+str(n)

                
                # escribir el diccionario actualizado en el archivo JSON
                with open(self.db, 'w') as f:
                    json.dump(data, f, indent=4)

                #print(json.dumps(newHfile, indent=4))

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
                start_time = time.time()
                commandOutput = ""

                newData = put(command, data)
                data = json.loads(newData)

                with open(self.db, 'w') as f:
                    json.dump(data, f, indent= 4)

                end_time = time.time()
                commandOutput+= "\n"
                commandOutput += "0 fila(s) en " + format(end_time - start_time, ".4f") + " segundos \n"

                self.output_text.insert(tk.END, commandOutput)

            elif (cm == "get"):
                commandOutput = get(command, data)
                self.output_text.insert(tk.END, commandOutput)

            elif (cm == "scan"):
                commandOutput = scan(command, data)
                self.output_text.insert(tk.END, commandOutput)

            elif (cm == "delete"):
                commandOutput = delete(command, data)
                self.output_text.insert(tk.END, commandOutput)
                
            elif (cm == "deleteall"):
                commandOutput = deleteAll(command, data)
                self.output_text.insert(tk.END, commandOutput)

            elif (cm == "count"):
                commandOutput = countF(command, data)
                self.output_text.insert(tk.END, commandOutput)
                
            elif (cm == "truncate"):
                commandOutput = truncate(command, data)
                self.output_text.insert(tk.END, commandOutput)

            else:
                if cm == "clear":
                    self.output_text.delete('1.0', tk.END)
                else:
                    self.output_text.insert(tk.END, "Comando desconocido" +"\n")
        
        self.input_entry.delete(0, tk.END)
        
if __name__ == "__main__":
    hbase_simulator = HBaseSimulator()
    hbase_simulator.root.mainloop()
    