import time

def put(command):
    start_time = time.time()
    put_ret = ""

    try:
        # conseguimos los atributos del commando
        command = command.split(" ", 1)
        
    
    except:
        return "Formato: put '<table name>', 'row id', '<colfamily:colname>','<value>' \n"

    try: 
        attributes = command[1].split(",")
        print(attributes)
        # Conseguimos cada uno de los atributos
        tableName = attributes[0].strip()
        print(tableName)
        rowID = attributes[1].strip()
        print(rowID)
        info = attributes[2].strip().strip("'")
        print(info)

        col = info.split(":")
        colFam = col[0]
        print(colFam)
        colName = col[1]
        print(colName)

        value = info[0]
        print(value)

    except:
        return "Sintáxis inválida: Argumentos faltantes \n"
    
    # TODO: real put
    
 
    end_time = time.time()
    put_ret += "0 filas en " + format(end_time - start_time, ".4f") + " segundos"
    return put_ret

def get():
    return ""

def scan():
    return ""

def delete():
    return ""

def deleteAll():
    return ""

def count():
    return ""

def count():
    return ""

def truncate():
    return ""