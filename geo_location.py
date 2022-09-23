import os
import csv
import json
import pandas as pd
from config import Config as cfg

# import glob

# working direcotry
dir_path = os.path.dirname(os.path.realpath(__file__))

class geo_location_coordinate:
    def __init__(self):
        self.postal_district = cfg.postal_district
        self.gb_postcode =  cfg.gb_postcode
        self.gb_postcode_folder = cfg. gb_postcode_folder

    def json_file_db(self):
        # print(f'db path directory :{self.gb_postcode}')
        geo_db_files, db_files_name = [], []
        for dirpath, dnames, fnames in os.walk(self.gb_postcode):
            for f in fnames:
                file_path = os.path.join(dirpath, f)
                geo_db_files.append(file_path), db_files_name.append(f)   
        assert geo_db_files != db_files_name, "file path and file not match"
        return geo_db_files, db_files_name
    def get_csv_data(self):
        df = pd.read_csv(cfg.postal_district)
        postal_district_data = df.postal_district.tolist()
        # print(postal_district_data)
        return postal_district_data

    def postal_district2geo_location(self):
        print("DB Geo Location loading      : ", end = '', flush= True)
        geo_db_files, db_files_name = self.json_file_db()
        print("Done")
        print("Postal District data loading : ", end = '', flush= True)
        postal_district_data = self.get_csv_data()
        print("Done")
        geo_location_info = {
            "geo_db_files"  : geo_db_files,
            "db_files_name" : db_files_name,
            "postal_district_data" : postal_district_data
        }
        return geo_location_info

    def read_geo_location_json(self, json_file):
        coor_list = []
        data = json.load(open(json_file))
        for feature in data["features"]:
            coordinates = feature["geometry"]["coordinates"]
            for coors in coordinates:
                if len(coors) > 1:
                    for i in coors:

                        if len(i) == 2:
                            coor_list.append(i)
                        else:
                            for j in i:
                                assert len(j) == 2 , "need to nested loops"
                                coor_list.append(j)
                else:
                    if len(coors) == 1:
                        n_cor = coors[0]
                        for c_n in n_cor:
                            coor_list.append(c_n)
                    else:
                        print("this operation not implement yet")
        return coor_list

if __name__ =="__main__":
    obj = geo_location_coordinate()
    obj.postal_district2geo_location()
    # obj.json_file_db()
    # obj.get_csv_data()
    # postal_district = cfg.
    # # gb_postcode_folder = ["areas", "districts", "sectors", "units"]
    # # gb_postcode_path = "gb-postcodes-v5"

