
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from config import Config as cfg
# working direcotry
dir_path = os.path.dirname(os.path.realpath(__file__))
# defining year for url generation
years = [
    "2008", "2009", "2010", "2011","2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"
    ]

def get_driver(chrome_driver_path, input_url):
    # ++++++++++++++  drive initialization ++++++++++++++++++++
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(chrome_driver_path, chrome_options=chrome_options)

    driver.get(input_url)
    driver.implicitly_wait(1)
    return driver

def take_fullpage_screenshot(driver, file_name="data/unknown.png"):
    """ taken screenshoot
    """
    driver.set_window_size(1920, 1800)
    time.sleep(1)
    driver.save_screenshot(file_name)

def get_360_degree_img(driver, file_path_dir, cnt, postal_district, year=None):
    """
    operation for 360 degree image
    """
    for i in range(4):
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#compass > div > button.sO0oCd.QNxVQc"))).click()
        take_fullpage_screenshot(driver,  file_name = file_path_dir[:-4]+"_"+str(i)+".png")
        time.sleep(2)
        cnt+=1
    return cnt

def get_text_element(driver):
    """
    street view image text
    """
    text_element = driver.find_element(By.CSS_SELECTOR, "#titlecard > div.C5SiJf.V2ucA > \
    div.gzhbId > div.b4tYeb > div.PP8x0b > div").get_attribute("textContent")
    fomated_text = text_element.split(" ")[-1]
    print(fomated_text)
    return fomated_text

def street_view_image_process(
    driver:object, 
    latitude_and_longitude:str = '', 
    cnt:int=0, postal_district:list=[], 
    output_path:str="data"
    )-> dict:
    """
    Get url from google street view of 2008 to 2022 years
    """
    file_name = latitude_and_longitude.replace(" ", "_")
    file_path_dir = os.path.join(output_path, file_name)
    os.makedirs(output_path, exist_ok= True)
    print('Filling search input')
    driver.find_element(By.ID, "searchboxinput").send_keys(latitude_and_longitude)
    print("Click search ")
    driver.find_element(By.ID, 'searchbox-searchbutton').click()
    time.sleep(2)
    # click side bar image
    driver.set_window_size(1920, 1800)
    try:
        driver.find_element(By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > \
        div.e07Vkf.kA9KIf > div > div > div.ZKCDEc > div.RZ66Rb.FgCUCc > button').click()
    except:
        driver.find_element(By.CSS_SELECTOR, "#runway-expand-button > div > div > button.GFgdCf > div.L6Bbsd > div").click()
        wait = WebDriverWait(driver, 10)
        main_canvas = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[name()='canvas']")))
        size = main_canvas.size
        w, h = size['width'], size['height']
        new_w = w/2
        new_h = h/2
        ActionChains(driver).move_by_offset(new_h, new_h).pause(5).perform()
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[name()='canvas']"))).click()

    time.sleep(2)
    # minimize the left search region
    print("Minimize the search region")
    # #QA0Szd > div > div > div.gYkzb > button
    driver.find_element(By.CSS_SELECTOR, '#QA0Szd > div > div > div.gYkzb > button').click()
    time.sleep(2)
    print("click historical region")
    driver.find_element(By.CSS_SELECTOR, "#titlecard > div.C5SiJf.V2ucA > div.gzhbId > div.b4tYeb > div.PP8x0b").click()
    print("year 2022 select")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#timemachine > div > div > div > div.kopeNe.Hk4XGb > div:nth-child(3) > span").click()
    time.sleep(2)
    search_years = "2022"
    search_urls_list = []
    try:
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "timemachine")))
        # print(driver.current_url)
        street_view_url = driver.current_url
        if search_years in street_view_url:
            for y in years:
                n_url = street_view_url.replace(search_years, y)
                search_urls_list.append(n_url)
    except Exception as e:
        print(e)
    return cnt, search_urls_list

def get_screenshot_from_url(
    search_urls_list, geo_locaiton, postal_district, output_path, cnt
    ):
    """
    Generated url to google street view image crawling
    """
    text_list = []
    generated_output_path = os.path.join(output_path, postal_district)
    os.makedirs(generated_output_path, exist_ok=True)
    for i in search_urls_list:
        print(f"file url : {i}")
        driver = get_driver(cfg.chrome_driver_linux, i)
        wait = WebDriverWait(driver, 10)
        print("Minimize the search region")
        time.sleep(2)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#QA0Szd > div > div > div.gYkzb > button'))).click()
        # driver.find_element(By.CSS_SELECTOR, '#QA0Szd > div > div > div.gYkzb > button').click()
        time.sleep(2)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#timemachine > div > div > div > div.C2uExc > img.WUYGjd"))).click()
        # driver.find_element(By.CSS_SELECTOR, "#timemachine > div > div > div > div.C2uExc > img.WUYGjd").click()
        time.sleep(2)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#timemachine > div > div > div > div.PP8x0b.BLDmvf.Hk4XGb > div"))).click()
        # driver.find_element(By.CSS_SELECTOR, "#timemachine > div > div > div > div.PP8x0b.BLDmvf.Hk4XGb > div").click()
        time.sleep(2)
        text = get_text_element(driver)
        print(f"Extracted Year : {text}")
        if text not in text_list:
            text_list.append(text)
        else:
            print("Already Taken this year")
            continue
        time.sleep(2)
        file_name = f"extracted_img_{geo_locaiton}_{postal_district}_{text}_{cnt}.png"
        n_output_path = os.path.join(generated_output_path, file_name)
        get_360_degree_img(
            driver, n_output_path, cnt, postal_district, year=text
            )
        driver.quit()
        cnt+=1
    return cnt
    

def google_street_view_image_capture(
    driver:object = None,
    geo_locaiton:str ="" , 
    cnt = 0, 
    postal_district:list = [], 
    output_path:str="data"
    ) -> int:
    if driver == None:
        return None
    try:
        cnt, search_urls_list = street_view_image_process(
            driver, 
            latitude_and_longitude = geo_locaiton,
            cnt = cnt, 
            postal_district = postal_district
            )
        driver.quit()
        print("Generated URL List : ", search_urls_list)
        if search_urls_list:
            print("process running ")
            cnt = get_screenshot_from_url(
                search_urls_list,
                geo_locaiton,
                postal_district,
                output_path,
                cnt
            )
    except Exception as e:
        print(e)  
    return cnt


if __name__ == "__main__":
    # 51.587525, -0.133864
    output_path = "data"
    latitude_and_longitude = [["57.129048, -2.126709"]]
    postal_district = "n12"
    driver = get_driver(cfg.chrome_driver_linux, cfg.input_url)
    cnt = 0
    url_list = []
    for i in latitude_and_longitude:
        cnt = google_street_view_image_capture(
            driver = driver, 
            geo_locaiton = i[0], 
            cnt = cnt , 
            postal_district = postal_district,
            output_path = output_path
            )
        # url_list.extend(search_urls_list)
        cnt+=1
    driver.quit()