import xml.etree.ElementTree as ET
import xmltodict
import csv
import requests
import datetime
import os


def xml_to_dict(xml_str):
    data_dict = xmltodict.parse(xml_str)
    return data_dict


def dict_to_csv(data_dict, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        # Crée un objet writer CSV et l'en-tête
        csv_writer = csv.writer(csvfile)

        header = ["validFrom", "validTo", "placeOfOriginId", "historyMunicipalityId", "placeOfOriginName",
                  "cantonAbbreviation", "successorId"]
        csv_writer.writerow(header)

        # Inscrit les données dans le csv
        place_of_origins = data_dict["placeOfOriginNomenclature"]["placeOfOrigins"]["placeOfOrigin"]

        for place_of_origin in place_of_origins:
            row = [
                place_of_origin.get("validFrom", ""),
                place_of_origin.get("validTo", ""),
                place_of_origin.get("placeOfOriginId", ""),
                place_of_origin.get("historyMunicipalityId", ""),
                place_of_origin.get("placeOfOriginName", ""),
                place_of_origin.get("cantonAbbreviation", ""),
                place_of_origin.get("successorId", ""),
            ]
            csv_writer.writerow(row)


def get_last_modified_date(response):
    last_modified_str = response.headers.get("Last-Modified", None)
    if last_modified_str:
        last_modified_date = datetime.datetime.strptime(last_modified_str, "%a, %d %b %Y %H:%M:%S %Z")
        return last_modified_date
    return None


def save_last_modified_date(last_modified_date, file_path):
    with open(file_path, "w") as file:
        file.write(last_modified_date.strftime("%Y-%m-%d %H:%M:%S"))


def load_last_modified_date(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            date_str = file.readline().strip()
            return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return None


xml_url = "https://www.e-service.admin.ch/competency-app-download/eCH-0135.xml"
csv_file_path = "/home/ezra/PycharmProjects/scrapNorme_eCH-0135/data.csv"
last_modified_file = "/home/ezra/PycharmProjects/scrapNorme_eCH-0135/last_modified.txt"

# Récupérer le fichier XML depuis l'URL
response = requests.get(xml_url)

if response.status_code == 200:
    xml_str = response.text
    last_modified_date = get_last_modified_date(response)
    previous_last_modified_date = load_last_modified_date(last_modified_file)

    if previous_last_modified_date is None or last_modified_date > previous_last_modified_date:
        # Convertir les données XML en dictionnaire
        data_dict = xml_to_dict(xml_str)

        # Convertir les données du dictionnaire en format CSV et écrire dans un fichier
        dict_to_csv(data_dict, csv_file_path)

        # Sauvegarder la date de dernière modification
        save_last_modified_date(last_modified_date, last_modified_file)
    else:
        print("Pas de mise à jour depuis la dernière vérification.")
else:
    print("Erreur lors de la récupération du fichier XML.")
