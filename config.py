import os
dir_path = os.path.dirname(os.path.realpath(__file__))
class Config():
    # input url
    input_url = "https://www.google.com/maps/"
    # output path directory
    output_path = os.path.join(dir_path, "data")
    # google chrome web driver for linux
    chrome_driver_linux = os.path.join(dir_path, "driver/chromedriver")
    # google chrome web driver for windows
    chrome_driver_windows = os.path.join(dir_path, "driver/chromedriver.exe")
    # postal district csv path direcotry
    postal_district = os.path.join(dir_path, "db/postal_districts.csv")
    # gb postcode folder path
    gb_postcode =  os.path.join(dir_path,"db/gb-postcodes-v5")
    # gb folder list
    gb_postcode_folder = ["areas", "districts", "sectors", "units"]
    machine_os = "linux"

    