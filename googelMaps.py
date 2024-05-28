# Standortbestimmung der Wohnungen:
'''
Die Standorte der Wohnungen wurden durch ihre durch Adressen identifiziert. Diese Informationen wurden bereits im ursprünglichen Datensatz vorhanden.
Unter Verwendung der Google Maps API wurde der Abstand zwischen jedem Wohnort und dem nächstgelegenen Ocean Beach ermittelt.
Dieser Abstand wurde in Kilometern gemessen.
Da einige der Orte lokale Namen haben, die Google Maps nicht bekannt sind, werden die Entfernungen vom Ozean manuell hinzugefügt. 
'''



import googlemaps
from math import radians, cos, sin, sqrt, atan2
import csv

# Replace 'YOUR_API_KEY' with your actual API key
api_key = 'AIzaSyDv0XqIcZOyH6FUCn3ZQxEWudyS-YyEgX4'
gmaps = googlemaps.Client(key=api_key)

coastal_points = [
    'Consolação, Peniche, Leiria, Portugal',
    'Monserrate, Viana do Castelo, Portugal',
    'Foz do Douro, Porto, Portugal',
    'Praia da Rocha, Portimão, Faro, Portugal',
    'Cascais e Estoril, Lisboa, Portugal',
    'Costa da Caparica, Almada, Setúbal, Portugal',
    'Espinho, Aveiro, Portugal',
    'Fão, Esposende, Braga, Portugal',
    'Buarcos, Figueira da Foz, Coimbra, Portugal',
    'Vila Nova de Milfontes, Odemira, Beja, Portugal',
    'Azenhas do Mar, Sintra, Lisboa, Portugal',
    'Paço de Arcos, Oeiras, Lisboa, Portugal'
]


# Function to calculate the Haversine distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return int(R * c) 



coastal_coords = []
for coastal_point in coastal_points:
    geocode_result = gmaps.geocode(coastal_point)
    if geocode_result:
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        coastal_coords.append((lat, lng))
    else:
        print(f"No results found for {coastal_point}")

# Read locations from the CSV file
results = []

with open('list_for_googleMap.csv', mode='r', newline='', encoding='ISO-8859-1') as file:
    # Read the file here

    reader = csv.DictReader(file, delimiter=';')  # Assuming tab-delimited format
    for row in reader:
        location = row['Location']
        min_distance = float('inf')
        if location == location in ['Marco, Porto', 'Campo dos Leões, Santarém','Praça de Touros, Santarém'] :
            min_distance = 60
            results.append([location, min_distance])
        elif location in ['Guarda, Guarda','Centro de Saúde, Castelo Branco']:
            min_distance = 160
            results.append([location, min_distance])
        elif location in ['St.º António da Caparica, Almada', 'Marisol, Almada', 'Previdência, Porto' ]:
            min_distance = 0
            results.append([location, min_distance])
        else:
            geocode_result = gmaps.geocode(location)
            if geocode_result:
                loc_lat = geocode_result[0]['geometry']['location']['lat']
                loc_lng = geocode_result[0]['geometry']['location']['lng']
            
                nearest_coastal_point = None
                for coastal_lat, coastal_lng in coastal_coords:
                    distance = haversine(loc_lat, loc_lng, coastal_lat, coastal_lng)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_coastal_point = (coastal_lat, coastal_lng)
                results.append([location, min_distance])
            else:
                print(f"No results found for {location}")
                results.append([location, 'not found'])
# Write the results to a CSV file
with open('location_distances-3.csv', mode='w', newline='', encoding='ISO-8859-1') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Location', 'Distance to Nearest Coastal Point (km)'])
    writer.writerows(results)

print("Data saved to location_distances.csv")


