import time

def put(command, data):
    start_time = time.time()
    ret = ""

    try:
        # conseguimos los atributos del commando
        command = command.split(" ", 1)
        print(command[1])
    
    except:
        return "put '<table name>', 'row id', '<colfamily:colname>','<value>' \n"

    try: 
        arguments = command[1].split(",")

        # Conseguimos cada uno de los atributos
        tableName = arguments[0].strip()
        print(tableName)
        rowID = arguments[1].strip()
        print(rowID)
        info = arguments[2].strip().strip("'")
        print(info)

        col = info.split(":")
        colFam = col[0]
        print(colFam)
        colName = col[1]
        print(colName)

        value = info[0]
        print(value)

    except:
        return "Sintaxis inválida: Argumentos faltantes \n"
    
    # TODO: real put

    # if enabled
    # else: return "Tabla no está hablitada"
    
 
    end_time = time.time()
    ret+= "\n"
    ret += "0 fila(s) en " + format(end_time - start_time, ".4f") + " segundos \n"
    return ret

def get(command, data):
    start_time = time.time()
    ret = ""
    cantFilas = 0

    try:
        # conseguimos los atributos del commando
        command = command.split(" ", 1)
        print(command[1])
    
    except:
        return "get '<table name>', 'row id' \n"

    try:
        arguments = command[1].strip().split(",")

        tableName = arguments[0].strip().strip("'")
        print(tableName)

        rowID = arguments[1].strip().strip("'")
        print(rowID)

    except:
        return "Sintaxis inválida: Argumentos faltantes \n"
    

    # conseguir region
    region = ""

    for x in data:
        for y in data[x]:
            if y == tableName:
                region = x 

    print("region: " + region)

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
            "\ttimestamp=" + data[region][tableName]["rows"][rowID][columnFamily][columnName]["Timestamp"] +\
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
        print(tableName)

    except:
        return "scan '<table name>\n"

    ret += "ROW\t\tCOLUMN+CELL\n"

    # conseguir region
    region = ""

    for x in data:
        for y in data[x]:
            if y == tableName:
                region = x 

    print("region: " + region)

    # Verificar existencia de tabla
    if region == "":
        return "La tabla no existe\n"

    # verificar disponilbilidad
    if data[region][tableName]["enabled"] != "True":
        return "La tabla no está disponible\t"

    for row in data[region][tableName]["rows"]:
        for columnFamily in data[region][tableName]["rows"][row]:
            for columnName in data[region][tableName]["rows"][row][columnFamily]:    
                ret +=row + "\t\t" + "Column="+\
                columnFamily+":"+columnName+\
                ", timestamp="+data[region][tableName]["rows"][row][columnFamily][columnName]["Timestamp"]+\
                ", value="+data[region][tableName]["rows"][row][columnFamily][columnName]["value"]+\
                "\n"

    end_time = time.time()
    ret+= "\n"
    ret += str(cantFilas) + " fila(s) en " + format(end_time - start_time, ".4f") + " segundos \n"
    return ret

def delete(command, data):
    start_time = time.time()
    ret = ""
    cantFilas = 0

    try:
        # conseguimos los atributos del commando
        command = command.split(" ", 1)
        print(command[1])
    
    except:
        return "delete '<table name>', '<row>', '<column name >', '<time stamp>' \n"

    try: 
        arguments = command[1].split(",")
        print(arguments)

        tableName = arguments[0].strip("'")
        print(tableName)

        row = arguments[1].strip("'")
        print(row)

        columnName = arguments[2].strip("'")
        print(columnName)

        timeStamp = arguments[3].strip("'") 
        print(timeStamp)

    except:
        return "Sintaxis inválida: Argumentos faltantes \n"
    
    # TODO: real put

    # if enabled
    # else: return "Tabla no está hablitada"
    

    end_time = time.time()
    ret+= "\n"
    ret += str(cantFilas) + " fila(s) en " + format(end_time - start_time, ".4f") + " segundos \n"
    return ret

def deleteAll(command, data):
    start_time = time.time()
    ret = ""
    cantFilas = 0

    try:
        # conseguimos los atributos del commando
        command = command.split(" ", 1)
        print(command[1])
    
    except:
        return "deleteall '<table name>', '<row>' \n"

    try: 
        arguments = command[1].split(",")
        print(arguments)

        tableName = arguments[0].strip("'")
        print(tableName)

        row = arguments[1].strip("'")
        print(row)

    except:
        return "Sintaxis inválida: Argumentos faltantes \n"
    

    # TODO

    # if enabled
    # else: return "Tabla no está hablitada"

    end_time = time.time()
    ret+= "\n"
    ret += str(cantFilas) + " fila(s) en " + format(end_time - start_time, ".4f") + " segundos\n"
    return ret

def countF(command, data):
    start_time = time.time()
    ret = ""

    try:
        command = command.split(" ")
        tableName = command[1]
        print(tableName)

    except:
        return "count '<table name>'\n"
    
    # TODO: real count

    # if enabled
    # else: return "Tabla no está hablitada"


    end_time = time.time()
    ret+= "\n"
    ret += "1 fila(s) en " + format(end_time - start_time, ".4f") + " segundos \n"
    return ret

def truncate(command, data):
    start_time = time.time()
    ret = ""

    try:
        command = command.split(" ")
        tableName = command[1]
        print(tableName)

    except:
        return "truncate '<table name>'\n"
    
    # TODO: real put

    # if enabled
    # else: return "Tabla no está hablitada"


    end_time = time.time()
    ret+= "\n"
    ret += "0 fila(s) en " + format(end_time - start_time, ".4f") + " segundos \n"
    return ret