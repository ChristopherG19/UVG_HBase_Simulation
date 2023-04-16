# Universidad del Valle de Guatemala
# Bases de datos 2
# HBase Simulation
# Grupo#5

import re
from tkinter import simpledialog, messagebox

def get_info(command):
    try:
        infoValues = command.split(" ", 1)[1]
    except:
        return (None, "Sintaxis inválida: Argumentos faltantes")
    dataInfo = infoValues.split(",", 1)
    TableName = dataInfo[0].replace("'", "").replace('"', '')
    return (TableName, dataInfo)

def get_table(Hfiles, command):
    Table = None
    TableName = get_info(command)[0]
    if(TableName == None):
        return Table
    
    for region in Hfiles:
        for table in Hfiles[region]:
            if table == TableName:
                Table = Hfiles[region]
                
    return Table

def get_table_names(Hfiles, regex):
    table_names = []
    for region in Hfiles:
        for table in Hfiles[region]:
            if re.match(regex, table) != None:
                table_names.append(table)
                
    return table_names

def exists(Hfiles, command):
    exist = False
    if (get_table(Hfiles, command) != None):
        exist = True
    return exist

def create(timestamp, command):
    try:
        infoValues = command.split(" ", 1)[1]
        dataInfo = infoValues.split(",", 1)
        TableName = dataInfo[0].replace("'", "")
        ColumnFamilies = dataInfo[1].strip().replace("'", "").replace('"', '').split(",")
        if((len(ColumnFamilies) == 1 and ColumnFamilies[0] == '') or any(x == " " for x in ColumnFamilies)):
            return ("Sintaxis inválida: Argumentos faltantes", None)
    except:
        return ("Sintaxis inválida: Argumentos faltantes", None)
    
    newRow = {}
    for columnF in ColumnFamilies: newRow[columnF.strip()] = {}
        
    newHFile = { "enabled": "True", "timestamp": timestamp, "rows": {"0": newRow}}
    new_Region = {TableName: newHFile}

    return (TableName, new_Region)
    
def listTables(Hfiles):
    table_names = []
    for region in Hfiles:
        for table in Hfiles[region]:
            table_names.append(table)
                
    return table_names

def disableTable(Hfiles, command, timestamp):
    TableName = get_info(command)[0]
    if(TableName == None):
        return (get_info(command)[1], None, Hfiles)
        
    if(not exists(Hfiles, command)):
        return ("not found, no changes", TableName, Hfiles)
    
    for region in Hfiles:
        for table in Hfiles[region]:
            if(TableName == table):
                if "enabled" in Hfiles[region][table] and Hfiles[region][table]["enabled"] == "True":
                    Hfiles[region][table]["timestamp"] = timestamp
                    Hfiles[region][table]["enabled"] = "False"
                    return ("disabled", TableName, Hfiles)
                else:
                    return ("Already disabled", TableName, Hfiles)

def enableTable(Hfiles, command, timestamp):
    TableName = get_info(command)[0]
    if(TableName == None):
        return (get_info(command)[1], None, Hfiles)
    
    if(not exists(Hfiles, command)):
        return ("not found, no changes", TableName, Hfiles)
    
    for region in Hfiles:
        for table in Hfiles[region]:
            if(TableName == table):
                if "enabled" in Hfiles[region][table] and Hfiles[region][table]["enabled"] == "False":
                    Hfiles[region][table]["timestamp"] = timestamp
                    Hfiles[region][table]["enabled"] = "True"
                    return ("enabled", TableName, Hfiles)
                else:
                    return ("Already enabled", TableName, Hfiles)

def checkStatus(Hfiles, command):
    if(not exists(Hfiles, command)):
        return "Table not found, no changes"
    
    TableName = get_info(command)[0]
    if(TableName == None):
        return (get_info(command)[1], TableName)
    
    isEnabled = False
    
    for region in Hfiles:
        for table in Hfiles[region]:
            if(TableName == table):
                if "enabled" in Hfiles[region][table]:
                    if (Hfiles[region][table]["enabled"] == "True"):
                        return (not isEnabled, TableName)
                    else:
                        return (isEnabled, TableName)
                
    return (isEnabled, TableName)

def alterTable(Hfiles, command, timestamp):
    TableName, CommandInfo = get_info(command)[0], [x.strip() for x in get_info(command)[1]][1]
    
    if(TableName == None):
        return (Hfiles, get_info(command)[1], None, None, None)
    
    if(not exists(Hfiles, command)):
        return (Hfiles, "not found, no changes", None, TableName, None)
    
    try:
        ActionAndInfo = [x.strip() for x in CommandInfo.replace("'", "").replace('"', '').split("=>")]
        if (ActionAndInfo[0] == "" or ActionAndInfo[1] == ""):
            return (Hfiles, "Sintaxis inválida: Argumentos faltantes", None, None, None)
    except:
        return (Hfiles, "Sintaxis inválida: Argumentos faltantes", None, None, None)
    
    for region in Hfiles:
        for table in Hfiles[region]:
            if TableName == table:
                if "enabled" in Hfiles[region][table] and Hfiles[region][table]["enabled"] == "True":
                    Hfiles[region][table]["timestamp"] = timestamp
                    for row_key, row_value in list(Hfiles[region][table]["rows"].items()):
                        for column_family, cfv in list(row_value.items()):
                            if ActionAndInfo[0] == "delete":
                                if column_family == ActionAndInfo[1]:
                                    del Hfiles[region][table]["rows"][row_key][column_family]
                            elif ActionAndInfo[0] == "ModifyName":
                                tempInfo = [x.strip() for x in ActionAndInfo[1].split(",")]
                                if column_family == tempInfo[0]:
                                    Hfiles[region][table]["rows"][row_key][tempInfo[1]] = Hfiles[region][table]["rows"][row_key].pop(column_family)
                                    return (Hfiles, ActionAndInfo[0], tempInfo[0], TableName, tempInfo[1])
                else:
                    return (Hfiles, "disabled", None, TableName, None)
                                
    return (Hfiles, ActionAndInfo[0], ActionAndInfo[1], TableName, None)
    
def dropTable(Hfiles, command):
    TableName, CommandInfo = get_info(command)
    
    if(TableName == None):
        return (CommandInfo, Hfiles, None)
    
    if(not exists(Hfiles, command)):
        return (f"Table {TableName} not found, no changes", Hfiles, TableName)
    
    veri, res = checkStatus(Hfiles, command)
    
    if(not veri == False):
        return (f"{TableName} is not disabled, not changes", Hfiles, TableName)
    
    for region in Hfiles:
        for table in Hfiles[region]:
            if TableName == table:
                del Hfiles[region]
                return (f"{TableName} dropped", Hfiles, TableName)
    
def dropAll(Hfiles, command):
    regex = get_info(command)[0]
    if(regex == None):
        return (get_info(command)[1], Hfiles, None)
    coincidences = get_table_names(Hfiles, regex)
    
    if(len(coincidences) > 0):
        messagebox.showinfo("Informacion", f"Encontramos {len(coincidences)} coincidencias {coincidences}")
        res = simpledialog.askstring("Confirmación", f"Deseas dropear todas las tablas que coincidan con '{regex}'? (Y/n)")
        if res and (res.lower() == "y"):
            res2 = simpledialog.askstring("Confirmación", "Necesito tu autorización para deshabilitar antes las tablas.\nDeseas continuar? (Y/n)")
            if res2 and (res2.lower() == "y"):
                to_delete = []
                # Se deshabilitan las tablas
                for TableName in coincidences:
                    for region in Hfiles:
                        for table in Hfiles[region]:
                            if(TableName == table):
                                if "enabled" in Hfiles[region][table] and Hfiles[region][table]["enabled"] == "True":
                                    Hfiles[region][table]["enabled"] = "False"
                                to_delete.append((region, table))
                messagebox.showinfo("Informacion", "Tablas deshabilitadas, procediendo a dropear")
                # Se dropean
                for region, table in to_delete:
                    del Hfiles[region]
                return (f"{len(coincidences)} tables successfully dropped", Hfiles, "Ok")
            else:
                print("Cancelando operacion")
                return ("No changes", Hfiles, "Ok")
        else:
            print("Cancelando operacion")
            return ("No changes", Hfiles, "Ok")
    else:
        return ("No hay coincidencias", Hfiles, "Ok")
    
def describe(Hfiles, command):
    TableName = get_info(command)[0]
    
    if(TableName == None):
        return (get_info(command)[1], 0, TableName)
    
    if(not exists(Hfiles, command)):
        return (f"Table {TableName} not found", 0, TableName)
    
    HfileT = get_table(Hfiles, command)
    status = ""
    columnFnames = set()
    countRows = 0
    for table in HfileT:
        for property in HfileT[table]:
            if HfileT[table]["enabled"] == "True":
                status = "ENABLED"
            else:
                status = "DISABLED"
            for row in HfileT[table]["rows"]:
                if row == '0':
                    countRows = 0
                else:
                    countRows = len(HfileT[table]["rows"])
                for value in HfileT[table]["rows"][row]:
                    columnFnames.add(value)
    columnFnames = list(columnFnames)
    
    column_info = ""
    for column in columnFnames:
        column_info += f"{{NAME => '{column}', DATA_BLOCK_ENCODING => 'NONE', BLOOMFILTER => 'ROW', REPLICATION_SCOPE => '0', VERSIONS => '1', COMPRESSION => 'NONE', MIN_VERSIONS => '0', TTL => 'FOREVER', KEEP_DELETED_CELLS => 'FALSE', BLOCKSIZE => '65536', IN_MEMORY => 'false', BLOCKCACHE => 'true'}}\n"

    return (f"Table {TableName} is {status}\n{TableName}\nCOLUMN FAMILIES DESCRIPTION\n{column_info}", countRows, TableName)
    