# Google street view data scraping
Google street view data scraping using geolocation. This script will take 360 degree screenshot within 4 images and also it can take all of years screenshot of the current geolocation.



# Environment

```
conda create -n ds_3.8 python=3.8
conda activate ds_3.8
```
# Requirements,

```
pip install selenium==4.4.0
pip install pandas==1.3.5 

```

# Configuration

Download gb-postcodes-v5 from:
https://postcodes-mapit-static.s3.eu-west-2.amazonaws.com/data/gb-postcodes-v5.tar.bz2

```
make sure db folder:
db:
    - gb-postcodes-v5
        - areas
        - districts
        - sectors
        - units
    - postal_districts.csv

For windows
self.chrome_driver_linux = chrome_driver_windows
Linux:

self.chrome_driver_linux = cfg.chrome_driver_linux

```

# Run for taking screenshot

```
python main.py
```




