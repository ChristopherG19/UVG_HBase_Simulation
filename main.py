
# 

import tkinter as tk
import json
import datetime
import os
import time

from ddl.functions import *

class HBaseSimulator:
    def __init__(self):
        
        self.db = "./data/HFile.json"
        
        self.root = tk.Tk()
        self.root.title("HBase Simulator")

        self.input_label = tk.Label(self.root, text="Ingrese comando:")
        self.input_label.pack()

        self.input_entry = tk.Entry(self.root, width=60)
        self.input_entry.pack()
        self.input_entry.bind("<Return>", lambda event: self.execute_command())

        self.submit_button = tk.Button(self.root, text="Ejecutar", command=self.execute_command)
        self.submit_button.pack()

        self.output_text = tk.Text(self.root, height=35, width=100)
        self.output_text.pack()
        self.output_text.config(state=tk.DISABLED)
        
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
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Se evalua si se limpiará o cerrara la "terminal"
        if command == "clear":
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete('1.0', tk.END)
            self.output_text.config(state=tk.DISABLED)
            
        elif command.lower() == "exit":
            self.root.quit()

        # Procesamiento de comando
        data = None
        with open(self.db) as archivo:
            # Se leen Regions con HFiles
            data = json.load(archivo)

            cs = command.split(" ")
            cm = cs[0].lower() # Comando Separado
            
            # Escribir el comando en el archivo de historial
            with open(self.historial_file, "a") as f:
                f.write(f"{timestamp}: {command}\n")
                
            commands = [
                "create", "list", "disable", "enable", "is_enabled", "alter",
                "drop", "drop_all", "describe", "put", "get",
                "scan", "delete", "delete_all", "count", "truncate" 
            ]

            if (cm != "clear"):
                if cm in commands:
                    tm = datetime.datetime.now().strftime("%S")
                    cmdLine = f"\nhbase(main):{tm}> {command}"
                    self.show_results(cmdLine)

                else:
                    tm = datetime.datetime.now().strftime("%S")
                    cmdLine = f"\nhbase(main):{tm}> Comando {cm} desconocido"
                    self.show_results(cmdLine)

            if(cm == "create"):
                timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                n = len(data) + 1
                nameRegion = "Region"+str(n)
                start_time = time.time()
                TableName, newHfile = create(timestamp, command)[0], create(timestamp, command)[1]

                data[nameRegion] = newHfile
                # Actualizar la db
                with open(self.db, 'w') as f:
                    json.dump(data, f, indent=4)

                end_time = time.time()
                tiempo = end_time - start_time

                result = f"0 row(s) in {tiempo} seconds\n=> Hbase::Table - {TableName}"
                self.show_results(result)
                #print(json.dumps(newHfile, indent=4))

            elif(cm == "list"):
                start_time = time.time()
                table_names = listTables(data)
                end_time = time.time()
                tiempo = end_time - start_time
                result = "TABLE\n" + "\n".join(table_names) + f"\nTook {tiempo} seconds\n=> " + str(table_names)
                self.show_results(result)

            elif(cm == "disable"):
                timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                start_time = time.time()  
                resultDisable, TableName, newData = disableTable(data, command, timestamp)
                end_time = time.time()
                tiempo = end_time - start_time
                result = f"TABLE {TableName} {resultDisable} in {tiempo} seconds"
                with open(self.db, 'w') as f:
                    json.dump(newData, f, indent=4)
                self.show_results(result)
                
            elif(cm == "enable"):
                timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                start_time = time.time()  
                resultEnable, TableName, newData = enableTable(data, command, timestamp)
                end_time = time.time()
                tiempo = end_time - start_time
                result = f"TABLE {TableName} {resultEnable} in {tiempo} seconds"
                with open(self.db, 'w') as f:
                    json.dump(newData, f, indent=4)
                self.show_results(result)
            
            elif(cm == "is_enabled"):
                start_time = time.time()  
                isEnabled = checkStatus(data, command)
                end_time = time.time()
                tiempo = end_time - start_time
                result = f"{isEnabled}\n0 row(s) in {tiempo} seconds"
                self.show_results(result)
            
            elif(cm == "alter"):
                timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                start_time = time.time()  
                alterData, action, cf, tname, newtname = alterTable(data, command, timestamp)
                end_time = time.time()
                tiempo = end_time - start_time
                result = "ERROR"
                
                if(action == 'disabled'):
                    result = f"{tname} disabled, no changes\n0 row(s){tiempo} seconds"
                elif (action == 'delete'):
                    result = f"{cf} deleted from {tname} in {tiempo} seconds"
                elif (action == 'ModifyName'):
                    result = f"{cf} change to {newtname} in table {tname} in {tiempo} seconds"
                else:
                    result = f"Table {tname} {action} in {tiempo} seconds"
                with open(self.db, 'w') as f:
                    json.dump(alterData, f, indent=4)
                self.show_results(result)

            elif (cm == "drop"):
                start_time = time.time()  
                dropResult, alterData = dropTable(data, command)
                end_time = time.time()
                tiempo = end_time - start_time
                result = f"{dropResult}\n0 row(s) in {tiempo} seconds"
                with open(self.db, 'w') as f:
                    json.dump(alterData, f, indent=4)
                self.show_results(result)

            elif (cm == "drop_all"):
                start_time = time.time()  
                dropResult, alterData = dropAll(data, command)
                end_time = time.time()
                tiempo = end_time - start_time
                result = f"{dropResult}\n0 row(s) in {tiempo} seconds"
                with open(self.db, 'w') as f:
                    json.dump(alterData, f, indent=4)
                self.show_results(result)

            elif (cm == "describe"):
                start_time = time.time()  
                result = describe(data, command)
                end_time = time.time()
                tiempo = end_time - start_time
                result = f"{result}{tiempo} seconds"
                self.show_results(result)

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
    