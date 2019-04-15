import csv
from ingenieria.models import *


def importar():
    with open("F:/recurrentes.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            # _, created = Recurrente.objects.get_or_create(
            #     id=row[0],
            #     activo=row[1],
            #     creado=row[2],
            #     modificado=row[3],
            #     nombre=row[4],
            #     apellido=row[5],
            #     email=row[6],
            #     telefono=row[7],
            #     ruc=row[8],
            #     rmc=row[9],
            # )
