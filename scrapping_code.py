from selenium import webdriver
import time

BASE_URL = "https://finance.naver.com/sise/sise_index.nhn?code=KPI200"
driver = webdriver.Chrome("../Downloads/chromedriver 2")
driver.get(BASE_URL)
time.sleep(3)

# 당일 코스피지수 스크래핑
kospi_200_juyo_sise = driver.find_element_by_tag_name("tbody")
tr = kospi_200_juyo_sise.find_elements_by_tag_name("tr")

for idx, tr_child in enumerate(tr):
    if len(tr_child.text) > 0:
        p_list = tr_child.text.split()
        if idx == 0:
            if "nv01" in tr[0].find_element_by_xpath("//td[@id='now_value']/strong").get_attribute("class"):
                print(f"{p_list[0]}: {p_list[1]}(하락), {p_list[2]}: {p_list[3]}")
            elif "red02" in tr[0].find_element_by_xpath("//td[@id='now_value']/strong").get_attribute("class"):
                print(f"{p_list[0]}: {p_list[1]}(상승), {p_list[2]}: {p_list[3]}")
            else:
                print(f"{p_list[0]}: {p_list[1]}, {p_list[2]}: {p_list[3]}")
        elif idx == 2:
            if "nv01" in tr[0].find_element_by_xpath("//td[@id='change_value']/span").get_attribute("class"):
                print(f"{p_list[0]}: {p_list[1]}(하락), {p_list[2]}: {p_list[3]}")
            elif "red02" in tr[0].find_element_by_xpath("//td[@id='change_value']/span").get_attribute("class"):
                print(f"{p_list[0]}: {p_list[1]}(상승), {p_list[2]}: {p_list[3]}")
            else:
                print(f"{p_list[0]}: {p_list[1]}, {p_list[2]}: {p_list[3]}")
        elif idx == 4:
            if "tah nv01" in tr[0].find_element_by_xpath("//td[@id='change_rate']/strong").get_attribute("class"):
                print(f"{p_list[0]}: {p_list[1]}(하락), {p_list[2]}: {p_list[3]}")
            elif "tah red02" in tr[0].find_element_by_xpath("//td[@id='change_rate']/strong").get_attribute("class"):
                print(f"{p_list[0]}: {p_list[1]}(상승), {p_list[2]}: {p_list[3]}")
            else:
                print(f"{p_list[0]}: {p_list[1]}, {p_list[2]}: {p_list[3]}")
        else:
            print(f"{p_list[0]}: {p_list[1]}, {p_list[2]}: {p_list[3]}")

# 시간별시세 영역                                                                        
time_iframe = driver.find_element_by_xpath("//iframe[@title='시간별시세 영역']")
driver.switch_to_frame(time_iframe)

iframe = driver.find_element_by_class_name("Nnavi")
맨뒤 = iframe.find_element_by_class_name("pgRR").find_element_by_tag_name("a").get_attribute("href").split("=")
맨뒤index = int(맨뒤[-1])

for p in range(1, 맨뒤index+1):
    url = "https://finance.naver.com/sise/sise_index_time.naver?code=KPI200&thistime=20211230185900&page=" + str(p)
    driver.get(url)
    time.sleep(5)

    time_sise = driver.find_element_by_class_name("type_1")
    for idx, tr_child in enumerate(time_sise.find_elements_by_tag_name("tr")):
        if idx == 2 or idx == 3 or idx == 4 or idx == 9 or idx == 10 or idx == 11:
            info = tr_child.find_elements_by_tag_name("td")
            for d_idx, data in enumerate(info):
                if d_idx == 0 and data.text != " ":
                    print("체결시각: " + data.text)
                elif d_idx == 1 and data.text != " ":
                    print("체결가: " + data.text)
                elif d_idx == 2 and data.text != " ":
                    if data.find_element_by_tag_name("span").get_attribute("class") == "tah p11 nv01":
                        print("전일비(하락): " + data.text)
                    elif data.find_element_by_tag_name("span").get_attribute("class") == "tah p11 red02":
                        print("전일비(상승): " + data.text)
                    elif data.find_element_by_tag_name("span").get_attribute("class") == "tah p11 gray01":
                        print("전일비(동일): " + data.text)
                elif d_idx == 3 and data.text != " ":
                    print("변동량(천주): " + data.text)
                elif d_idx == 4 and data.text != " ":
                    print("거래량(천주): " + data.text)
                elif d_idx == 5 and data.text != " ":
                    print("거래대금(백만): " + data.text)

driver.switch_to_default_content
driver.get(BASE_URL)

