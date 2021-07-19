import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd

query = "소프트웨어교육"
dataTitle = "2018.01.01-2018.01.31+1_100"
file = "./crawling_data/" + query + "/" + dataTitle + ".xlsx"

path = "https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=001&aid=0009795098"

driver = webdriver.Chrome("./chromedriver")
cleanbotOn = True

print("current path: ", path)
driver.get(path)
# 서버에게 get 요청을 보냈으니 response를 기다려야함. html을 받는데 걸리는 최소시간 -> 1.5s
time.sleep(1)
soup = bs(driver.page_source, 'html.parser') # 3초가 끝나면 새로운 page의 url로 접속하고 파서가 파싱한다.

# 반응 수집
u_likeit = soup.find("ul", attrs={"class":"u_likeit_layer"})

if u_likeit is None: reaction = "None"
else: 
    u_likeit_counts = u_likeit.find_all("span", attrs={"class":"u_likeit_list_count"}) #좋아요, 훈훈해요, 슬퍼요, 화나요, 후속기사원해요

    reaction = [int(count.text.strip().replace(',', '')) for count in u_likeit_counts] # [0,0,0,0,0]

# 댓글 수집 -> 댓글 더보기 페이지로 이동
total_num_repl = soup.find("span", attrs={"class": "u_cbox_count"})

if total_num_repl is None: 
    comment = "None"
else: 
    total_num_repl = int(total_num_repl.text.strip().replace(',', ''))

    if total_num_repl == 0: # 현재 댓글이 없음
        comment = []
    else: # 댓글 더보기로 이동

        if cleanbotOn:
            # 클린봇 옵션 해제 후 추출
            cleanbot = driver.find_element_by_css_selector('a.u_cbox_cleanbot_setbutton')
            cleanbot.click()
            time.sleep(1)
            cleanbot_disable = driver.find_element_by_xpath("//input[@id='cleanbot_dialog_checkbox_cbox_module']")
            cleanbot_disable.click()
            time.sleep(1)
            cleanbot_confirm = driver.find_element_by_css_selector('button.u_cbox_layer_cleanbot2_extrabtn')
            cleanbot_confirm.click()
            time.sleep(1)
            cleanbotOn = False

        # 댓글 더보기
        driver.find_element_by_css_selector('a.u_cbox_btn_view_comment').click()
        time.sleep(1)

        # 더보기 계속 클릭
        while True:
            try:
                driver.find_element_by_css_selector('a.u_cbox_btn_more').click()
                time.sleep(1)
            except:
                break;

        cbox_contents = driver.find_elements_by_css_selector("span.u_cbox_contents") # 댓글 내용
        cbox_recomms = driver.find_elements_by_css_selector("em.u_cbox_cnt_recomm") # 댓글의 좋아요 수
        cbox_unrecomms = driver.find_elements_by_css_selector("em.u_cbox_cnt_unrecomm") # 댓글 싫어요 수

        content = [content.text.strip().replace("\n", "") for content in cbox_contents]
        for i, count in enumerate(cbox_recomms):
            print(str(i) + "th: " + count.text.strip().replace(',','')) # -> 자동접힘 댓글이면 ''으로 읽어옴..
        unrecomm = [int(count.text.strip().replace(',', '')) for count in cbox_unrecomms] # 자동접힘 댓글이 있을 시 에러남

driver.close()