import xml.etree.ElementTree as ET
import xmltodict
import csv
import requests


def xml_to_dict(xml_str):
    data_dict = xmltodict.parse(xml_str)
    return data_dict


def dict_to_csv(data_dict, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        # Créez un objet writer CSV et écrivez l'en-tête
        csv_writer = csv.writer(csvfile)

        header = ["validFrom", "validTo", "placeOfOriginId", "historyMunicipalityId", "placeOfOriginName",
                  "cantonAbbreviation", "successorId"]
        csv_writer.writerow(header)

        # Écrivez les lignes de données
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


def fetch_xml_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


# Main script
xml_url = "https://www.e-service.admin.ch/competency-app-download/eCH-0135.xml"
csv_file_path = "/home/ezra/PycharmProjects/scrapNorme_eCH-0135/data.csv"

# Récupérer le fichier XML depuis l'URL
xml_str = fetch_xml_from_url(xml_url)

if xml_str:
    # Convertir les données XML en dictionnaire
    data_dict = xml_to_dict(xml_str)

    # Convertir les données du dictionnaire en format CSV et écrire dans un fichier
    dict_to_csv(data_dict, csv_file_path)
else:
    print("Erreur lors de la récupération du fichier XML.")
