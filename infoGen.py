"""
Estructura de los HFiles:

    {
        "Region":{
            "TablaName":{
                "enabled": "True",
                "timestamp": 1111111111.9383,
                "rows": {
                    "row key":{
                        "Column Family":{
                            "Column qualifier": {
                                "timestamp": 1111111111.9383,
                                "value": "..."
                            }
                        }
                    }
                }
            }
        }
    }

"""
# Tabla Estudiante
    # carnet_Estudiante
        # Informacion_Personal
            # nombres
            # apellidos
            # cumpleaños
        # Información_Contacto
            # correo
            # teléfono
            # telefono_hogar 
        # Información_académica
            # Año
            # promedio
            # skill

# Tabla Company
    # company_id
        # General
            # nombre
            # market_value
            # url
        # Locacion
            # Pais
            # Direccion
        # Jerarquia
            # CEO 
            # Founder 


import json
from dml.functions import *

def fill_Hfiles(filepath, fp):

    with open(fp) as f:
        data = json.load(f)

    with open(filepath) as file:
        Mockdata = json.load(file)

    # put 'TableName', 'RowKey, 'ColumnFamily:ColumnName', value
    for obj in Mockdata:
        # nombre
        cmd = f"put Estudiante, '{obj['idEstudiante']}', 'Informacion_personal:Nombre', {obj['Nombre']}"
        newData, ret = put(cmd, data)
        if type(newData) != str:
            print(ret)
        else:
            data = json.loads(newData)

        # apellido
        cmd = f"put Estudiante, '{obj['idEstudiante']}', 'Informacion_personal:Apellido', {obj['Apellido']}"
        newData, ret = put(cmd, data)
        if type(newData) != str:
            print(ret)
        else:
            data = json.loads(newData)
            
        # birthday
        cmd = f"put Estudiante, '{obj['idEstudiante']}', 'Informacion_personal:Birthday', {obj['birthday']}"
        newData, ret = put(cmd, data)
        if type(newData) != str:
            print(ret)
        else:
            data = json.loads(newData)

        # correo
        if obj['correo'] != None:
            cmd = f"put Estudiante, '{obj['idEstudiante']}', 'Informacion_de_contacto:Correo', {obj['correo']}"
            newData, ret = put(cmd, data)
            if type(newData) != str:
                print(ret)
            else:
                data = json.loads(newData)

        # celular
        cmd = f"put Estudiante, '{obj['idEstudiante']}', 'Informacion_de_contacto:Celular', {obj['celular']}"
        newData, ret = put(cmd, data)
        if type(newData) != str:
            print(ret)
        else:
            data = json.loads(newData)

        if obj['telefono_casa'] != None:
            # telefono
            cmd = f"put Estudiante, '{obj['idEstudiante']}', 'Informacion_de_contacto:Telefono', {obj['telefono_casa']}"
            newData, ret = put(cmd, data)
            if type(newData) != str:
                print(ret)
            else:
                data = json.loads(newData)

        # year
        cmd = f"put Estudiante, '{obj['idEstudiante']}', 'Informacion_academica:Year', {obj['year']}"
        newData, ret = put(cmd, data)
        if type(newData) != str:
            print(ret)
        else:
            data = json.loads(newData)

        # promedio
        cmd = f"put Estudiante, '{obj['idEstudiante']}', 'Informacion_academica:Promedio', {obj['promedio']}"
        newData, ret = put(cmd, data)
        if type(newData) != str:
            print(ret)
        else:
            data = json.loads(newData)

        # skill
        cmd = f"put Estudiante, '{obj['idEstudiante']}', 'Informacion_academica:LinkedIn_Skill', {obj['skill']}"
        newData, ret = put(cmd, data)
        if type(newData) != str:
            print(ret)
        else:
            data = json.loads(newData)

    with open(fp, 'w') as f:
        json.dump(data, f, indent= 4)


def fill_Hfiles_company(filepath, fp):
    
    with open(fp) as f:
        data = json.load(f)

    with open(filepath) as file:
        MockdataB = json.load(file)

    for obj in MockdataB:
        # nombre
        cmd = f"put Company, '{obj['Codigo']}', 'General:Nombre', {obj['Nombre']}"
        newData, ret = put(cmd, data)
        if type(newData) != str:
            print(ret)
        else:
            data = json.loads(newData)

        # Value
        cmd = f"put Company, '{obj['Codigo']}', 'General:Value', {obj['market_value']}"
        newData, ret = put(cmd, data)
        if type(newData) != str:
            print(ret)
        else:
            data = json.loads(newData)

        # web page
        if obj['web_page'] != None:
            cmd = f"put Company, '{obj['Codigo']}', 'General:url', {obj['web_page']}"
            newData, ret = put(cmd, data)
            if type(newData) != str:
                print(ret)
            else:
                data = json.loads(newData)
            
        # pais
        cmd = f"put Company, '{obj['Codigo']}', 'Locacion:Pais', {obj['Pais']}"
        newData, ret = put(cmd, data)
        if type(newData) != str:
            print(ret)
        else:
            data = json.loads(newData)

        # direccion
        cmd = f"put Company, '{obj['Codigo']}', 'Locacion:Direccion', {obj['direccion']}"
        newData, ret = put(cmd, data)
        if type(newData) != str:
            print(ret)
        else:
            data = json.loads(newData)

        # CEO
        cmd = f"put Company, '{obj['Codigo']}', 'Jerarquia:CEO', {obj['CEO']}"
        newData, ret = put(cmd, data)
        if type(newData) != str:
            print(ret)
        else:
            data = json.loads(newData)

        # Fundador
        cmd = f"put Company, '{obj['Codigo']}', 'Jerarquia:Founder', {obj['Founder']}"
        newData, ret = put(cmd, data)
        if type(newData) != str:
            print(ret)
        else:
            data = json.loads(newData)

    with open(fp, 'w') as f:
        json.dump(data, f, indent= 4)

# fill_Hfiles('./data/MOCK_DATA_estudiantes.json', './data/Hfile.json')
fill_Hfiles_company('./data/MOCK_DATA_company.json', './data/Hfile.json')