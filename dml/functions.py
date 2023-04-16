import time
import json

def put(command, data):

    try:
        # conseguimos los atributos del commando
        command = command.split(" ", 1)
        command[1]
    
    except:
        return (True, "put '<table name>', 'row id', '<colfamily:colname>','<value>' \n")

    try: 
        arguments = command[1].split(",")

        # Conseguimos cada uno de los atributos
        tableName = arguments[0].strip().strip("'")
        rowID = arguments[1].strip().strip("'")
        info = arguments[2].strip().strip("'")

        col = info.split(":")
        colFam = col[0].strip().strip("'")
        colName = col[1].strip().strip("'")

        value = arguments[3].strip().strip("'")

    except:
        return True, "Sintaxis inválida: Argumentos faltantes \n"
    
    # conseguir region
    region = ""

    for x in data:
        for y in data[x]:
            if y == tableName:
                region = x 


    # Verificar existencia de tabla
    if region == "":
        return True, "La tabla no existe\n"

    # verificar disponilbilidad
    if data[region][tableName]["enabled"] != "True":
        return True, "La tabla no está disponible\t"
    
    # verificar si existe rowID
    try:
        data[region][tableName]["rows"][rowID]

        # verificar si existe la column family
        try: 
            data[region][tableName]["rows"][rowID][colFam]

            data[region][tableName]["rows"][rowID][colFam][colName] = {
                "Timestamp": time.time(),
                "value": value
            }
        
        except:
            # no existe
            data[region][tableName]["rows"][rowID][colFam] = {
                colName: {
                    "Timestamp": time.time() * 1000,
                    "value": value
                }
            }

    except:
        # no existe rowID
        data[region][tableName]["rows"][rowID] = {
            colFam: {
                colName: {
                    "Timestamp": time.time() * 1000,
                    "value": value
                }
            }
        }

    # modificar timestamp de la tabla
    data[region][tableName]["timestamp"] = time.time() * 1000

    data_string = json.dumps(data)
    return (data_string, "")

def get(command, data):
    start_time = time.time()
    ret = ""
    cantFilas = 0

    try:
        # conseguimos los atributos del commando
        command = command.split(" ", 1)
        command[1]
    
    except:
        return "get '<table name>', 'row id' \n"

    try:
        arguments = command[1].strip().split(",")

        tableName = arguments[0].strip().strip("'")

        rowID = arguments[1].strip().strip("'")

    except:
        return "Sintaxis inválida: Argumentos faltantes \n"
    

    # conseguir region
    region = ""

    for x in data:
        for y in data[x]:
            if y == tableName:
                region = x 


    # Verificar existencia de tabla
    if region == "":
        return "La tabla no existe\n"

    # verificar disponilbilidad
    if data[region][tableName]["enabled"] != "True":
        return "La tabla no está disponible\t"
    
    # verificar existencia del row
    try:
        data[region][tableName]["rows"][rowID]
    except:
        return "La row ID ingresada no existe \n"
    
    ret += "COLUMN\t\t\tCELL\n"
    
    for columnFamily in data[region][tableName]["rows"][rowID]:
        for columnName in data[region][tableName]["rows"][rowID][columnFamily]:
            cantFilas += 1
            ret += columnFamily + ":" + columnName +\
            "\ttimestamp=" + str(data[region][tableName]["rows"][rowID][columnFamily][columnName]["Timestamp"]) +\
            ", value=" + data[region][tableName]["rows"][rowID][columnFamily][columnName]["value"] +\
            "\n"

    end_time = time.time()
    ret+= "\n"
    ret += str(cantFilas) + " fila(s) en " + format(end_time - start_time, ".4f") + " segundos \n"
    return ret

def scan(command, data):
    start_time = time.time()
    ret = ""
    cantFilas = 0

    try:
        command = command.split(" ")
        tableName = command[1].strip().strip("'")

    except:
        return "scan '<table name>\n"

    ret += "ROW\t\tCOLUMN+CELL\n"

    # conseguir region
    region = ""

    for x in data:
        for y in data[x]:
            if y == tableName:
                region = x 


    # Verificar existencia de tabla
    if region == "":
        return "La tabla no existe\n"

    # verificar disponilbilidad
    if data[region][tableName]["enabled"] != "True":
        return "La tabla no está disponible\t"
    
    rows = "rows"

    for fila in data[region][tableName][rows]:
        for columnFamily in data[region][tableName][rows][fila]:
            for columnName in data[region][tableName][rows][fila][columnFamily]:
                retorno = "" + \
                str(fila) + \
                "\t\tColumn=" + \
                columnFamily + ":" +columnName +\
                ", timestamp=" + str(data[region][tableName][rows][fila][columnFamily][columnName]["Timestamp"]) +\
                ", value=" + data[region][tableName][rows][fila][columnFamily][columnName]["value"] +\
                "\n"

                ret += retorno



    end_time = time.time()
    ret+= "\n"
    ret += str(cantFilas) + " fila(s) en " + format(end_time - start_time, ".4f") + " segundos \n"
    return ret

def delete(command, data):
    
    try:
        # conseguimos los atributos del commando
        command = command.split(" ", 1)
        command[1]
    
    except:
        return True, "delete '<table name>', 'row id', '<colfamily:colname>' \n"

    try: 
        arguments = command[1].split(",")

        # Conseguimos cada uno de los atributos
        tableName = arguments[0].strip().strip("'")
        rowID = arguments[1].strip().strip("'")
        info = arguments[2].strip().strip("'")

        col = info.split(":")
        colFam = col[0].strip().strip("'")
        colName = col[1].strip().strip("'")


    except:
        return True, "Sintaxis inválida: Argumentos faltantes \n"
    
    # conseguir region
    region = ""

    for x in data:
        for y in data[x]:
            if y == tableName:
                region = x 


    # Verificar existencia de tabla
    if region == "":
        return True, "La tabla no existe\n"

    # verificar disponilbilidad
    if data[region][tableName]["enabled"] != "True":
        return True, "La tabla no está disponible\t"
    
    # verificar si existe rowID
    try:
        data[region][tableName]["rows"][rowID]

        # verificar si existe la column family
        try: 
            data[region][tableName]["rows"][rowID][colFam]

            try:
                del data[region][tableName]["rows"][rowID][colFam][colName]

            except:
                return True, f"ERROR: Column name desconocido {colFam} en tabla {tableName}"
        
        except:
            # no existe column family
            return True, f"ERROR: Column family desconocida {colFam} en tabla {tableName}"

    except:
        # no existe rowID
        return True, f"ERROR: Row ID desconocido {rowID} en tabla {tableName}"

    # modificar timestamp de la tabla
    data[region][tableName]["timestamp"] = time.time() * 1000

    data_string = json.dumps(data)

    return (data_string, "")

def deleteAll(command, data):

    try:
        # conseguimos los atributos del commando
        command = command.split(" ", 1)
        command[1]
    
    except:
        return True, "deleteall '<table name>', '<row>' \n"

    try: 
        arguments = command[1].strip().split(",")

        tableName = arguments[0].strip().strip("'")

        rowID = arguments[1].strip().strip("'")

    except:
        return True, "Sintaxis inválida: Argumentos faltantes \n"
    
# conseguir region
    region = ""

    for x in data:
        for y in data[x]:
            if y == tableName:
                region = x 

    # Verificar existencia de tabla
    if region == "":
        return True, "La tabla no existe\n"

    # verificar disponilbilidad
    if data[region][tableName]["enabled"] != "True":
        return True, "La tabla no está disponible\t"
    
    # verificar si existe rowID
    try:
        data[region][tableName]["rows"][rowID]

        del data[region][tableName]["rows"][rowID]

    except:
        # no existe rowID
        return True, f"ERROR: Row ID desconocido {rowID} en tabla {tableName}"

    # modificar timestamp de la tabla
    data[region][tableName]["timestamp"] = time.time() * 1000

    data_string = json.dumps(data)

    return (data_string, "")

def countF(command, data):
    start_time = time.time()
    ret = ""

    try:
        command = command.split(" ")
        tableName = command[1].strip().strip("'")

    except:
        return "count '<table name>'\n"
    
    # conseguir region
    region = ""

    for x in data:
        for y in data[x]:
            if y == tableName:
                region = x 


    # Verificar existencia de tabla
    if region == "":
        return "La tabla no existe\n"

    # verificar disponilbilidad
    if data[region][tableName]["enabled"] != "True":
        return "La tabla no está disponible\t"
    
    cantData = 0
    for row in data[region][tableName]["rows"]:
        for columnFamily in data[region][tableName]["rows"][row]:
            for columnName in data[region][tableName]["rows"][row][columnFamily]:
                for value in data[region][tableName]["rows"][row][columnFamily][columnName]:
                    cantData += 1

    ret += "\n" + str(cantData) + "\n"


    end_time = time.time()
    ret+= "\n"
    ret += "1 fila(s) en " + format(end_time - start_time, ".4f") + " segundos \n"
    return ret

def truncate(command, data):
    
    try:
        command = command.split(" ")
        tableName = command[1].strip().strip("'")

    except:
        return True, "truncate '<table name>'\n"
    
    # conseguir region
    region = ""

    for x in data:
        for y in data[x]:
            if y == tableName:
                region = x 


    # Verificar existencia de tabla
    if region == "":
        return True, "La tabla no existe\n"

    # verificar disponilbilidad
    if data[region][tableName]["enabled"] != "True":
        return True, "La tabla no está disponible\t"
    
    # Eliminar info de la tabla
    del data[region][tableName]

    data_string = json.dumps(data)

    return (data_string, "")