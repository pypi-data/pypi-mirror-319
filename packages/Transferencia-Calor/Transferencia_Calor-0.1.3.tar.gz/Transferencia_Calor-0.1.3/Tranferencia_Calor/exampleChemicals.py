from chemicals.elements import periodic_table
import pandas as pd

def tablaPeriodica():
    tabla_periodoca = []
    for elemento in periodic_table:
        tabla_periodoca.append(
            {
                "elemento": elemento.name,
                "simbolo": elemento.symbol,
                "Peso Molecular": elemento.MW
            }
        )
    df=pd.DataFrame(tabla_periodoca)
    print(df)

tablaPeriodica()
