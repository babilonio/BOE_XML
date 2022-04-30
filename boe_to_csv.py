from xml.etree import ElementTree
import csv


tree = ElementTree.parse("boe.xml")
root = tree.getroot()

keys = [
    "Marca",
    "Modelo-Tipo",
    "Inicio",
    "Fin",
    "C.C.",
    "N.º de cilind.",
    "G/D",
    "P kW",
    "cvf",
    "cv",
    "2022 Valor euros"
]

tables = root.findall("./table")
print(len(tables))

with open('boe.csv', 'w', encoding='UTF-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=keys + ["Fecha"])
    writer.writeheader()

    for table in tables:
        marca = table.findall("thead/tr/th")[0].text.replace("Marca: ", "")
        
        for modelo in table.findall("tbody/tr"):
            values = [td.text for td in modelo.findall("td")]
            row = dict(zip(keys, [marca] + values))
            
            try:
                inicio = int(row["Inicio"].replace("-", ""))
                try:
                    fin = int(row["Fin"])
                except ValueError:
                    fin = 2022

                for i in range(fin-inicio + 1):
                    row.update({"Fecha": inicio + i})
                    writer.writerow(row)
            except:
                row.update({"Fecha": ""})
                writer.writerow(row)
