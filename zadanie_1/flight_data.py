import matplotlib.pyplot as plt
import requests
import database
import pandas as pd


# Funkcja do pozyskania danych z OpenSky Network API
def fetch_flight_data(databasefile="flights.db"):
    # AREA EXTENT COORDINATE WGS4 (for Atlanta Airport - ATL ± 100 km)
    lon_min, lat_min = -85.4277, 32.6407
    lon_max, lat_max = -83.4277, 34.6407

    # credintals foor OpenSky API
    user_name, password = ("Kmita", "CNqH@pSdmmQpjH7C")

    url_data = (
            'https://' + user_name + ':' + password +
            '@opensky-network.org/api/states/all?' +
            'lamin=' + str(lat_min) + '&lomin=' + str(lon_min) +
            '&lamax=' + str(lat_max) + '&lomax=' + str(lon_max)
    )

    # Fetching data from the API
    response = requests.get(url_data).json()
    # print(response)

    if 'states' in response and response['states']:
        col_name = [
            'icao24', 'callsign', 'origin_country', 'time_position', 'last_contact',
            'long', 'lat', 'baro_altitude', 'on_ground', 'velocity',
            'true_track', 'vertical_rate', 'sensors', 'geo_altitude',
            'squawk', 'spi', 'position_source'
        ]
        flight_df = pd.DataFrame(response['states'], columns=col_name)
        # flight_df.fillna('No data', inplace=True)
        database.save_to_db(flight_df, databasefile)
    else:
        print("No flight data available.")


# Odczyt danych i wygenerowanie wykresu z danych lotniczych
def plot_flight_data(databasefile="flights.db", show_plot=True):
    # Wczytaj dane lotnicze z bazy danych
    flight_df = database.load_flight_data(databasefile)

    # caly kod tutaj (filtracja, konwersja jednostek, sortowanie i wybieranie jednego, rysowanie wykresu)

    # Remove entries with missing values in velocity and geo_altitude
    flight_df = flight_df.dropna(subset=['velocity', 'geo_altitude'])
    flight_df['velocity'] = pd.to_numeric(flight_df['velocity'], errors='coerce')
    flight_df['geo_altitude'] = pd.to_numeric(flight_df['geo_altitude'], errors='coerce')

    # Convert units
    flight_df['velocity_kmh'] = flight_df['velocity'] * 3.6
    flight_df['geo_altitude_km'] = flight_df['geo_altitude'] / 1000

    # Remove duplicate flights, keeping the one with the highest velocity
    flight_df = flight_df.sort_values(by='velocity_kmh', ascending=False).drop_duplicates(subset='icao24', keep='first')

    plt.figure(figsize=(8,6))
    plt.scatter(flight_df['velocity_kmh'], flight_df['geo_altitude_km'], alpha=0.6)
    plt.xlabel('Velocity (km/h)')
    plt.ylabel('Geometric Altitude (km)')
    plt.title('Aircraft Velocity vs Geometric Altitude')
    plt.xlim(0, 1200)
    plt.ylim(0, 14)
    plt.grid(True)
    plt.tight_layout()

    if show_plot:
        plt.show()
