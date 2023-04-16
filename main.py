# UNIVERSIDAD DEL VALLE DE GUATEMALA
# FACULTAD DE INGENIERÍA
# DEPARTAMENTO DE CIENCIAS DE LA COMPUTACIÓN
# BASES DE DATOS 2
# CHRISTOPHER GARCÍA 20541
# MARIA ISABEL SOLANO 20504

import tkinter as tk
import json
import datetime
import os
import time

from ddl.functions import *
from dml.functions import *

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
                "scan", "delete", "deleteall", "count", "truncate" 
            ]

            if (cm != "clear"):
                if cm in commands:
                    tm = datetime.datetime.now().strftime("%S")
                    cmdLine = f"\nhbase(main):{tm}> {command}"
                    self.show_results(cmdLine)

                else:
                    tm = datetime.datetime.now().strftime("%S")
                    cmdLine = f"\nhbase(main):{tm}> Comando {command} desconocido"
                    self.show_results(cmdLine)
            
            if(cm == "create"):
                timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                n = len(data) + 1
                nameRegion = "Region"+str(n)
                start_time = time.time()
                TableName, newHfile = create(timestamp, command)
                if(newHfile != None):
                    data[nameRegion] = newHfile
                    # Actualizar la db
                    with open(self.db, 'w') as f:
                        json.dump(data, f, indent=4)

                    end_time = time.time()
                    tiempo = end_time - start_time

                    result = f"0 row(s) in {tiempo} seconds\n=> Hbase::Table - {TableName}"
                    self.show_results(result)
                else:
                    end_time = time.time()
                    tiempo = end_time - start_time
                    formato = "Formato: create '<table name>', '<ColumnFamily1>', '<ColumnFamily2>', ..."
                    result = f"{TableName}\n{formato}\n0 row(s) in {tiempo} seconds"
                    self.show_results(result)
                #print(json.dumps(newHfile, indent=4))

            elif(cm == "list"):
                if len(command.strip().split(" ")) > 1:
                    start_time = time.time()
                    end_time = time.time()
                    tiempo = end_time - start_time
                    result = "Argumentos adicionales no reconocidos\nFormato: list"
                    self.show_results(result)
                else:
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
                if(TableName != None):
                    end_time = time.time()
                    tiempo = end_time - start_time
                    result = f"TABLE {TableName} {resultDisable} in {tiempo} seconds"
                    with open(self.db, 'w') as f:
                        json.dump(newData, f, indent=4)
                    self.show_results(result)
                else:
                    end_time = time.time()
                    tiempo = end_time - start_time
                    formato = "Formato: disable '<table name>'"
                    result = f"{resultDisable}\n{formato}\nResult in {tiempo} seconds"
                    self.show_results(result)
                
            elif(cm == "enable"):
                timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                start_time = time.time()  
                resultEnable, TableName, newData = enableTable(data, command, timestamp)
                if(TableName != None):
                    end_time = time.time()
                    tiempo = end_time - start_time
                    result = f"TABLE {TableName} {resultEnable} in {tiempo} seconds"
                    with open(self.db, 'w') as f:
                        json.dump(newData, f, indent=4)
                    self.show_results(result)
                else:
                    end_time = time.time()
                    tiempo = end_time - start_time
                    formato = "Formato: enable '<table name>'"
                    result = f"{resultEnable}\n{formato}\nResult in {tiempo} seconds"
                    self.show_results(result)
            
            elif(cm == "is_enabled"):
                start_time = time.time()  
                isEnabled = checkStatus(data, command)
                end_time = time.time()
                tiempo = end_time - start_time
                formato = "Formato: is_enabled '<table name>'"
                result = f"{isEnabled}\n{formato}\n0 row(s) in {tiempo} seconds"
                self.show_results(result)
            
            elif(cm == "alter"):
                timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                start_time = time.time()  
                alterData, action, cf, tname, newtname = alterTable(data, command, timestamp)
                if(tname != None):
                    end_time = time.time()
                    tiempo = end_time - start_time
                    result = ""
                    
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
                else:
                    end_time = time.time()
                    tiempo = end_time - start_time
                    formato = "Formato 1: alter '<table name>', 'delete' => '<Column Family name>'\n"
                    formato += "Formato 2: alter '<table name>', 'ModifyName' => '<Column Family name>', '<New Column Family name>\n"
                    result = f"{action}\n{formato}0 row(s){tiempo} seconds"
                    self.show_results(result)

            elif (cm == "drop"):
                start_time = time.time()  
                dropResult, alterData, tbName = dropTable(data, command)
                if(tbName    != None):
                    end_time = time.time()
                    tiempo = end_time - start_time
                    result = f"{dropResult}\n0 row(s) in {tiempo} seconds"
                    with open(self.db, 'w') as f:
                        json.dump(alterData, f, indent=4)
                    self.show_results(result)
                else:
                    end_time = time.time()
                    tiempo = end_time - start_time
                    formato = "Formato: drop '<table name>'"
                    result = f"{dropResult}\n{formato}\n0 row(s) in {tiempo} seconds"
                    self.show_results(result)

            elif (cm == "drop_all"):
                start_time = time.time()  
                dropResult, alterData, resultCm = dropAll(data, command)
                if (resultCm != None):
                    end_time = time.time()
                    tiempo = end_time - start_time
                    result = f"{dropResult}\n0 row(s) in {tiempo} seconds"
                    with open(self.db, 'w') as f:
                        json.dump(alterData, f, indent=4)
                    self.show_results(result)
                else:
                    end_time = time.time()
                    tiempo = end_time - start_time
                    formato = "drop_all '<regex>'"
                    result = f"{dropResult}\n{formato}\n0 row(s) in {tiempo} seconds"
                    self.show_results(result)

            elif (cm == "describe"):
                start_time = time.time()  
                result, rows, cmRes = describe(data, command)
                if(cmRes != None):
                    end_time = time.time()
                    tiempo = end_time - start_time
                    result = f"{result}{tiempo} seconds"
                    self.show_results(result)
                else:
                    end_time = time.time()
                    tiempo = end_time - start_time
                    formato = "Formato: describe '<table name>'"
                    result = f"{result}\n{formato}\n{rows} row(s) in {tiempo} seconds"
                    self.show_results(result)

            elif (cm == "put"):
                start_time = time.time()
                commandOutput = ""

                newData, errmsg = put(command, data)

                if (type(newData) != str):
                    commandOutput = errmsg

                else: 
                    data = json.loads(newData)

                    with open(self.db, 'w') as f:
                        json.dump(data, f, indent= 4)

                    end_time = time.time()
                    commandOutput+= "\n"
                    commandOutput += "0 fila(s) en " + format(end_time - start_time, ".4f") + " segundos \n"

                self.show_results(commandOutput)

            elif (cm == "get"):
                commandOutput = get(command, data)
                self.show_results(commandOutput)

            elif (cm == "scan"):
                commandOutput = scan(command, data)
                self.show_results(commandOutput)

            elif (cm == "delete"):
                start_time = time.time()
                commandOutput = ""

                newData, errmsg = delete(command, data)

                if (type(newData) != str):
                    commandOutput = errmsg

                else: 
                    data = json.loads(newData)

                    with open(self.db, 'w') as f:
                        json.dump(data, f, indent= 4)

                    end_time = time.time()
                    commandOutput+= "\n"
                    commandOutput += "0 fila(s) en " + format(end_time - start_time, ".4f") + " segundos \n"

                self.show_results(commandOutput)
                
            elif (cm == "deleteall"):
                start_time = time.time()
                commandOutput = ""

                newData, errmsg = deleteAll(command, data)

                if (type(newData) != str):
                    commandOutput = errmsg

                else: 
                    data = json.loads(newData)

                    with open(self.db, 'w') as f:
                        json.dump(data, f, indent= 4)

                    end_time = time.time()
                    commandOutput+= "\n"
                    commandOutput += "0 fila(s) en " + format(end_time - start_time, ".4f") + " segundos \n"

                self.show_results(commandOutput)
                
            elif (cm == "count"):
                commandOutput = countF(command, data)
                self.show_results(commandOutput)
                
            elif (cm == "truncate"):
                start_time = time.time()
                commandOutput = ""

                newData, errmsg = truncate(command, data)

                if (type(newData) != str):
                    commandOutput = errmsg

                else: 
                    data = json.loads(newData)

                    with open(self.db, 'w') as f:
                        json.dump(data, f, indent= 4)

                    end_time = time.time()
                    commandOutput+= "\n"
                    commandOutput += "0 fila(s) en " + format(end_time - start_time, ".4f") + " segundos \n"

                self.show_results(commandOutput)

            else:
                if cm == "clear":
                    self.output_text.delete('1.0', tk.END)
                else:
                    self.output_text.insert(tk.END, "Comando desconocido" +"\n")
        
        self.input_entry.delete(0, tk.END)
        
if __name__ == "__main__":
    hbase_simulator = HBaseSimulator()
    hbase_simulator.root.mainloop()
    