from selenium import webdriver
import time

BASE_URL = "https://finance.naver.com/sise/sise_index.nhn?code=KPI200"
driver = webdriver.Chrome("../Downloads/chromedriver 2")
driver.get(BASE_URL)
time.sleep(3)

# 당일 코스피지수 스크래핑
# tbody 태그 검색 후  kospi_200_juyo_sise에 집어넣음 print(type(kospi_200_juyo_sise))로 타입을 출력해보면, 검색된 web element(태그)로 리턴되는 것을 알 수 있음.
kospi_200_juyo_sise = driver.find_element_by_tag_name("tbody")
# kospi_200_juyo_sise에서 하위에 있는 모든 tr 태그들을 검색해서 리스트로 반환시킴
tr = kospi_200_juyo_sise.find_elements_by_tag_name("tr")


# 찾은 모든 tr 태그들을 enumerate를 사용해서 index하고 같이 뽑아냄
for idx, tr_child in enumerate(tr):
    #tr_child (태그)에서 뽑아낸 텍스트 데이터 길이가 0이면 유효하지 않은 데이터이므로, 조건문으로 검사
    if len(tr_child.text) > 0:
        # tr_child에서 뽑아낸 텍스트 데이터를 공백을 기준으로 split()하여, 리스트로 만듦
        p_list = tr_child.text.split()
        # 웹 사이트에서 tr 태그들의 생김새를 보면, 0, 2, 4번째 tr 태그에서 각각 코스피200 / 전일대비 / 등락률 데이터의 상승 / 하락을 색깔로 표시하고 있음
        
        # 0번째 tr 태그는 코스피 200 지수 표시
        if idx == 0:
            # tr 태그 하위에 td 태그의 id가 now_value인 태그 > strong 태그를 찾고, 해당 strong 태그의 class 이름을 가져옴.
            # 만약 클래스이름에 nv01이 포함되어있다면 하락, red01이 포함되어있다면 상승
            if "nv01" in tr_child.find_element_by_xpath("//td[@id='now_value']/strong").get_attribute("class"):
                print(f"{p_list[0]}: {p_list[1]}(하락), {p_list[2]}: {p_list[3]}")
            elif "red01" in tr_child.find_element_by_xpath("//td[@id='now_value']/strong").get_attribute("class"):
                print(f"{p_list[0]}: {p_list[1]}(상승), {p_list[2]}: {p_list[3]}")
            else:
                print(f"{p_list[0]}: {p_list[1]}, {p_list[2]}: {p_list[3]}")
        # 2번째 태그는 전일대비 표시
        elif idx == 2:
            # tr 태그 하위에 td 태그의 id가 change_value인 태그 > span 태그를 찾고, 해당 span 태그의 class 이름을 가져옴
            # 만약 클래스이름에 nv01이 포함되어있다면 하락, red02가 포함되어있다면 상승
            if "nv01" in tr_child.find_element_by_xpath("//td[@id='change_value']/span").get_attribute("class"):
                print(f"{p_list[0]}: {p_list[1]}(하락), {p_list[2]}: {p_list[3]}")
            elif "red02" in tr_child.find_element_by_xpath("//td[@id='change_value']/span").get_attribute("class"):
                print(f"{p_list[0]}: {p_list[1]}(상승), {p_list[2]}: {p_list[3]}")
            else:
                print(f"{p_list[0]}: {p_list[1]}, {p_list[2]}: {p_list[3]}")
        # 4번째 태그는 등락률 표시
        elif idx == 4:
            # tr 태그 하위에 td 태그의 id가 change_rate인 태그 > strong 태그를 찾고, 해당 strong 태그의 class 이름을 가져옴
            # 만약 클래스 이름에 tah nv01이 포함되어있다면 하락, tah red01이 포함되어있다면 상승
            if "tah nv01" in tr_child.find_element_by_xpath("//td[@id='change_rate']/strong").get_attribute("class"):
                print(f"{p_list[0]}: {p_list[1]}(하락), {p_list[2]}: {p_list[3]}")
            elif "tah red01" in tr_child.find_element_by_xpath("//td[@id='change_rate']/strong").get_attribute("class"):
                print(f"{p_list[0]}: {p_list[1]}(상승), {p_list[2]}: {p_list[3]}")
            else:
                print(f"{p_list[0]}: {p_list[1]}, {p_list[2]}: {p_list[3]}")
        # 그 외 다른 태그는 상승 / 하락 표시가 없으므로 그냥 출력
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

