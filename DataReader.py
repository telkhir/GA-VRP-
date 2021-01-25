import pandas as pd
import numpy as np


class DataReader:

    def __init__(self, excel_file_path):
        self.excel_file_path = excel_file_path

    def read_data(self):
        param_data = pd.read_excel(self.excel_file_path, "Param", skiprows=0)
        trips_df = pd.read_excel(self.excel_file_path, "Trips", skiprows=0)
        trips_df = trips_df[trips_df["NbEmployees"] != 0]
        distances_df = pd.read_excel(self.excel_file_path, "Distance", skiprows=0)
        nb_vehicles = param_data.loc[param_data["Param"] == "NbVehicles"][["Value1", "Value2", "Value3"]].sum(axis=1).values[0]
        nb_home = param_data.loc[param_data["Param"] == "NbHome"]["Value1"].values[0]
        nb_work = param_data.loc[param_data["Param"] == "NbWork"]["Value1"].values[0]
        time_per_station = param_data.loc[param_data["Param"] == "TimePerStation (min)"]["Value1"].values[0]
        speed = param_data.loc[param_data["Param"] == "Speed (min/km)"]["Value1"].values[0]
        trips = [tuple(x) for x in trips_df[["Departure", "Arrival"]].dropna().to_numpy()]
        all_stations = np.concatenate((trips_df["Departure"].dropna().unique(), trips_df["Arrival"].dropna().unique()))
        distances = dict()
        for station_i in all_stations:
            for station_j in all_stations:
                if station_i != station_j:
                    row = distances_df[(distances_df["Departure"] == station_i) & (distances_df["Arrival"] == station_j)]
                    if len(row) != 0:
                        distances[station_i, station_j] = row["Distance"].values[0]
                        distances[station_j, station_i] = row["Distance"].values[0]

        return {"all_stations": all_stations, "distances": distances, "nb_vehicles": nb_vehicles,
                "nb_home": nb_home, "nb_work": nb_work, "time_per_station": time_per_station,
                "speed": speed, "trips": trips}
