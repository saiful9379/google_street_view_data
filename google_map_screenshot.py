
import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from config import Config as cfg
# working direcotry
dir_path = os.path.dirname(os.path.realpath(__file__))

def get_driver(chrome_driver_path, input_url):
    # ++++++++++++++  drive initialization ++++++++++++++++++++
    driver = webdriver.Chrome(chrome_driver_path)
    driver.get(input_url)
    driver.implicitly_wait(3)
    return driver

def take_fullpage_screenshot(driver, file_name="data/unknown.png"):
    driver.set_window_size(1920, 1800)
    time.sleep(1)
    driver.save_screenshot(file_name)
    # driver.quit()

def get_360_degree_img(driver, file_path_dir, cnt, postal_district, year=None):
    for i in range(4):
        driver.find_element(By.CSS_SELECTOR, "#compass > div > button.sO0oCd.QNxVQc").click()
        take_fullpage_screenshot(driver,  file_name = f"{file_path_dir}_{postal_district}_{year}_{cnt}_{i}.png")
        time.sleep(3)
        cnt+=1
    return cnt
def get_text_element(driver):
    text_element = driver.find_element(By.CSS_SELECTOR, "#titlecard > div.C5SiJf.V2ucA > div.gzhbId > div.b4tYeb > div.PP8x0b > div").get_attribute("textContent")
    fomated_text = text_element.split(" ")[-1]
    print(fomated_text)
    return fomated_text


def street_view_image_process(driver, latitude_and_longitude, cnt, postal_district, output_path="data"):
    # insert latitude and langu
    file_name = latitude_and_longitude.replace(" ", "_")
    file_path_dir = os.path.join(output_path, file_name)
    os.makedirs(output_path, exist_ok= True)
    print('Filling search input')
    driver.find_element(By.ID, "searchboxinput").send_keys(latitude_and_longitude)
    print("Click search ")
    driver.find_element(By.ID, 'searchbox-searchbutton').click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.ZKCDEc > div.RZ66Rb.FgCUCc > button').click()
    time.sleep(1)
    # minimize the left search region
    print("Minimize the search region")
    driver.find_element(By.CSS_SELECTOR, '#QA0Szd > div > div > div.gYkzb > button').click()
    time.sleep(1)
    cnt = get_360_degree_img(driver, file_path_dir, cnt, postal_district, year = get_text_element(driver))
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "#titlecard > div.C5SiJf.V2ucA > div.gzhbId > div.b4tYeb > div.PP8x0b > button").click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#timemachine > div > div > div > div.C2uExc > img.WUYGjd").click()
    ########## close ###########################
    driver.find_element(By.CSS_SELECTOR, "#timemachine > div > div > div > div.HsalXc > button").click()
    time.sleep(2)
    cnt = get_360_degree_img(driver, file_path_dir, cnt, postal_district, year = get_text_element(driver))
    return cnt
    

if __name__ == "__main__":
    latitude_and_longitude = [["57.129048, -2.126709"]]
    postal_district = "n12"
    driver = get_driver(cfg.chrome_driver_linux, cfg.input_url)
    cnt = 0
    for i in latitude_and_longitude:
        cnt = street_view_image_process(driver, i[0], cnt, postal_district)
        cnt+=1
    driver.quit()