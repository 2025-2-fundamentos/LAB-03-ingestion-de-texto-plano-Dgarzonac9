"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requerimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """

    import pandas as pd
    import re

    with open('files/input/clusters_report.txt', 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    lineas = lineas[4:]  # Saltar cabecera

    patron = re.compile(r'^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)$')

    datos = []
    cluster_actual = None
    cantidad_actual = None
    porcentaje_actual = None
    palabras_clave_actuales = []

    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue

        coincidencia = patron.match(linea)
        if coincidencia:
            # Guardar cluster anterior
            if cluster_actual is not None:
                palabras = " ".join(palabras_clave_actuales)
                palabras = re.sub(r'\s+', ' ', palabras)
                palabras = ", ".join([x.strip() for x in palabras.split(",")])
                palabras = palabras.rstrip(".")
                datos.append([cluster_actual, cantidad_actual, porcentaje_actual, palabras])

            # Empezar nuevo cluster
            cluster_actual = int(coincidencia.group(1))
            cantidad_actual = int(coincidencia.group(2))
            porcentaje_actual = float(coincidencia.group(3).replace(",", "."))
            tail = coincidencia.group(4).strip()
            palabras_clave_actuales = [tail] if tail else []

        else:
            if linea:
                palabras_clave_actuales.append(linea)

    # Guardar último cluster
    if cluster_actual is not None:
        palabras = " ".join(palabras_clave_actuales)
        palabras = re.sub(r'\s+', ' ', palabras)
        palabras = ", ".join([x.strip() for x in palabras.split(",")])
        palabras = palabras.rstrip(".")
        datos.append([cluster_actual, cantidad_actual, porcentaje_actual, palabras])

    df = pd.DataFrame(
        datos,
        columns=[
            "cluster",
            "cantidad_de_palabras_clave",
            "porcentaje_de_palabras_clave",
            "principales_palabras_clave",
        ],
    )

    return df
