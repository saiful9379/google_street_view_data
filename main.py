import os
import json
from config import Config as cfg
from geo_location import geo_location_coordinate
# from google_map_screenshot import get_driver, street_view_image_process
from google_map_screenshot_v2 import get_driver, google_street_view_image_capture

class street_view_data_scraping:
    def __init__(self):
        self.input_url = cfg.input_url
        self.output_path = cfg.output_path
        self.chrome_driver_linux = cfg.chrome_driver_linux

    def get_screenshot(self, g_location_lan_lati, postal_district):
        cnt = 0
        for lan_lati in g_location_lan_lati:
            st_lan_lati = f'{lan_lati[::-1][0]} {lan_lati[::-1][1]}'
            try:
                driver = get_driver(self.chrome_driver_linux, self.input_url)
                google_street_view_image_capture(
                    driver = driver, 
                    geo_locaiton = st_lan_lati, 
                    cnt = cnt, 
                    postal_district = postal_district,
                    output_path =self.output_path
                    )
                driver.quit()
            except Exception as e:
                print(f"{e}")
            cnt+=1

    def street_view_data_crowling(self):
        """
        this is the main funtion for data scriping
        """
        geo_object = geo_location_coordinate()
        geo_location_info = geo_object.postal_district2geo_location()
        geo_db_files, db_files_name, postal_district_data = geo_location_info["geo_db_files"], \
            geo_location_info["db_files_name"], geo_location_info["postal_district_data"]

        for postal_district in postal_district_data:
            queries_files = [(s, idx) for idx, s in enumerate(db_files_name) if s.startswith(postal_district)]
            if len(queries_files)==0: print(f"empty location : {postal_district}")
            else:
                queries_files_idx = [idx[1] for idx in queries_files]
                res_list = list(map(geo_db_files.__getitem__, queries_files_idx))
                for r_list in res_list:
                    g_location_lan_lati = geo_object.read_geo_location_json(r_list)
                    self.get_screenshot(g_location_lan_lati, postal_district)
                    # print(g_location_lan_lati)

                        
if __name__ == "__main__":
    s_obj = street_view_data_scraping()
    s_obj.street_view_data_crowling()