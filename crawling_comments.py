import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd

# crawling.py에서 수집한 data에서 path 사용
# 기사 댓글(내용, 좋아요 수, 싫어요 수), 댓글 수 수집 및 반응(좋아요, 훈훈해요, 슬퍼요, 화나요, 후속기사원해요) 수집
# result format: columns - path/title/reaction/numberofcomments/comments

query = "소프트웨어교육"  # "SW교육", "AI교육", "ICT교육"
date = [
    # ...
    ("2015.01.01", "2015.01.31"), ("2015.02.01", "2015.02.28"), ("2015.03.01", "2015.03.31"), \
    ("2015.04.01", "2015.04.30"), ("2015.05.01", "2015.05.31"), ("2015.06.01", "2015.06.30"), \
    ("2015.07.01", "2015.07.31"), ("2015.08.01", "2015.08.31"), ("2015.09.01", "2015.09.30"), \
    ("2015.10.01", "2015.10.31"), ("2015.11.01", "2015.11.30"), ("2015.12.01", "2015.12.31"), \
    ("2016.01.01", "2016.01.31"), ("2016.02.01", "2016.02.28"), ("2016.03.01", "2016.03.31"), \
    ("2016.04.01", "2016.04.30"), ("2016.05.01", "2016.05.31"), ("2016.06.01", "2016.06.30"), \
    ("2016.07.01", "2016.07.31"), ("2016.08.01", "2016.08.31"), ("2016.09.01", "2016.09.30"), \
    ("2016.10.01", "2016.10.31"), ("2016.11.01", "2016.11.30"), ("2016.12.01", "2016.12.31"), \
    ("2017.01.01", "2017.01.31"), ("2017.02.01", "2017.02.28"), ("2017.03.01", "2017.03.31"), \
    ("2017.04.01", "2017.04.30"), ("2017.05.01", "2017.05.31"), ("2017.06.01", "2017.06.30"), \
    ("2017.07.01", "2017.07.31"), ("2017.08.01", "2017.08.31"), ("2017.09.01", "2017.09.30"), \
    ("2017.10.01", "2017.10.31"), ("2017.11.01", "2017.11.30"), ("2017.12.01", "2017.12.31"), \
    ("2018.01.01", "2018.01.31"), ("2018.02.01", "2018.02.28"), ("2018.03.01", "2018.03.31"), \
    ("2018.04.01", "2018.04.30"), ("2018.05.01", "2018.05.31"), ("2018.06.01", "2018.06.30"), \
    ("2018.07.01", "2018.07.31"), ("2018.08.01", "2018.08.31"), ("2018.09.01", "2018.09.30"), \
    ("2018.10.01", "2018.10.31"), ("2018.11.01", "2018.11.30"), ("2018.12.01", "2018.12.31"), \
    ("2019.01.01", "2019.01.31"), ("2019.02.01", "2019.02.28"), ("2019.03.01", "2019.03.31"), \
    ("2019.04.01", "2019.04.30"), ("2019.05.01", "2019.05.31"), ("2019.06.01", "2019.06.30"), \
    ("2019.07.01", "2019.07.31"), ("2019.08.01", "2019.08.31"), ("2019.09.01", "2019.09.30"), \
    ("2019.10.01", "2019.10.15"), ("2019.10.16", "2019.10.31"), ("2019.11.01", "2019.11.15"), \
    ("2019.11.16", "2019.11.30"), ("2019.12.01", "2019.12.15"), ("2019.12.16", "2019.12.31"),\
    ("2020.01.01", "2020.01.15"), ("2020.02.01", "2020.02.15"), ("2020.03.01", "2020.03.15"), \
    ("2020.04.01", "2020.04.15"), ("2020.05.01", "2020.05.15"), ("2020.06.01", "2020.06.15"), \
    ("2020.07.01", "2020.07.15"), ("2020.08.01", "2020.08.15"), ("2020.09.01", "2020.09.15"), \
    ("2020.10.01", "2020.10.15"), ("2020.11.01", "2020.11.15"), ("2020.12.01", "2020.12.15"), \
    ("2020.01.16", "2020.01.31"), ("2020.02.16", "2020.02.29"), ("2020.03.16", "2020.03.31"), \
    ("2020.04.16", "2020.04.30"), ("2020.05.16", "2020.05.31"), ("2020.06.16", "2020.06.30"), \
    ("2020.07.16", "2020.07.31"), ("2020.08.16", "2020.08.31"), ("2020.09.16", "2020.09.30"), \
    ("2020.10.16", "2020.10.31"), ("2020.11.16", "2020.11.30"), ("2020.12.16", "2020.12.31"), \
    ("2021.01.01", "2021.01.15"), ("2021.02.01", "2021.02.15"), ("2021.03.01", "2021.03.15"), \
    ("2021.04.01", "2021.04.15"), ("2021.05.01", "2021.05.15"), ("2021.06.01", "2021.06.15"), \
    ("2021.07.01", "2021.07.09"), \
    ("2021.01.16", "2021.01.31"), ("2021.02.16", "2021.02.29"), ("2021.03.16", "2021.03.31"), \
    ("2021.04.16", "2021.04.30"), ("2021.05.16", "2021.05.31"), ("2021.06.16", "2021.06.30"), \
    ("2021.07.01", "2021.07.15"), ("2021.07.16", "2021.07.31"), ("2021.08.01", "2021.08.15"),\
    ("2021.08.16", "2021.08.31"), ("2021.09.01", "2021.09.15"), ("2021.09.16", "2021.09.30"),\
    ("2021.10.01", "2021.10.15"), ("2021.10.16", "2021.10.28")
]

for dateStart, dateEnd in date:
    # for i in range(1,10,5): ### test: 5page단위
    for i in range(1, 400, 100):  # 100page단위, 400page까지 있음
        driver = webdriver.Chrome("./chromedriver")

        # data = pd.read_excel("./crawling_data/" + str(i) +"_" + str(i+4) + ".xlsx") ## test
        dataTitle = dateStart + "-" + dateEnd + "+" + str(i) + "_" + str(i+99)
        data = pd.read_excel("./crawling_data/" + query +
                             "/" + dataTitle + ".xlsx")
        paths = data["path"]
        titles = data["title"]

        reactions = []
        comments = []
        numComments = []
        print("current file: " + dataTitle)
        # print("current file: " + str(i) +"_" + str(i+4)) ## test

        cleanbotOn = True

        for path in paths:
            print("current path: ", path)
            driver.get(path)
            # 서버에게 get 요청을 보냈으니 response를 기다려야함. html을 받는데 걸리는 최소시간 -> 1.5s
            time.sleep(1)
            # 3초가 끝나면 새로운 page의 url로 접속하고 파서가 파싱한다.
            soup = bs(driver.page_source, 'html.parser')

            # 반응 수집
            u_likeit = soup.find("ul", attrs={"class": "u_likeit_layer"})

            if u_likeit is None:
                reaction = "None"
            else:
                u_likeit_counts = u_likeit.find_all(
                    "span", attrs={"class": "u_likeit_list_count"})  # 좋아요, 훈훈해요, 슬퍼요, 화나요, 후속기사원해요

                reaction = [int(count.text.strip().replace(',', ''))
                            for count in u_likeit_counts]  # [0,0,0,0,0]

            # 댓글 수집 -> 댓글 더보기 페이지로 이동
            total_num_repl = soup.find("span", attrs={"class": "u_cbox_count"})

            if total_num_repl is None:
                comment = "None"
            else:
                total_num_repl = int(
                    total_num_repl.text.strip().replace(',', ''))

                if total_num_repl == 0:  # 현재 댓글이 없음
                    comment = []
                else:  # 댓글 더보기로 이동

                    if cleanbotOn:
                        # 클린봇 옵션 해제 후 추출
                        cleanbot = driver.find_element_by_css_selector(
                            'a.u_cbox_cleanbot_setbutton')
                        cleanbot.click()
                        time.sleep(1)
                        cleanbot_disable = driver.find_element_by_xpath(
                            "//input[@id='cleanbot_dialog_checkbox_cbox_module']")
                        cleanbot_disable.click()
                        time.sleep(1)
                        cleanbot_confirm = driver.find_element_by_css_selector(
                            'button.u_cbox_layer_cleanbot2_extrabtn')
                        cleanbot_confirm.click()
                        time.sleep(1)
                        cleanbotOn = False

                    # 댓글 더보기
                    driver.find_element_by_css_selector(
                        'a.u_cbox_btn_view_comment').click()
                    time.sleep(1)

                    # 더보기 계속 클릭
                    while True:
                        try:
                            driver.find_element_by_css_selector(
                                'a.u_cbox_btn_more').click()
                            time.sleep(1)
                        except:
                            break

                    cbox_contents = driver.find_elements_by_css_selector(
                        "span.u_cbox_contents")  # 댓글 내용
                    cbox_recomms = driver.find_elements_by_css_selector(
                        "em.u_cbox_cnt_recomm")  # 댓글의 좋아요 수
                    cbox_unrecomms = driver.find_elements_by_css_selector(
                        "em.u_cbox_cnt_unrecomm")  # 댓글 싫어요 수

                    content = [content.text.strip().replace("\n", "")
                               for content in cbox_contents]
                    # 자동접힘 댓글은 못 읽어옴, ''으로 읽어와서 int()시 에러남
                    recomm = [count.text.strip().replace(',', '')
                              for count in cbox_recomms]
                    unrecomm = [count.text.strip().replace(',', '')
                                for count in cbox_unrecomms]  # 자동접힘 댓글은 못 읽어옴

                    # zip()을 이용하여 content, recomm, unrecomm 합치기
                    # [(c,r,u), ... ]
                    comment = list(zip(content, recomm, unrecomm))

            # reactions, comments에 append
            reactions.append(reaction)
            comments.append(comment)
            numComments.append(len(comment))

        driver.close()
        # 최종 값
        print("paths: ", len(paths))
        print("titles : ", len(titles))
        print("reactions : ", len(reactions))
        print("comments : ", len(comments))
        print("number of comments: ", numComments)

        my_dictionary = {"path": paths, "title": titles, "reaction": reactions,
                         "numberOfComments": numComments, "comments": comments}
        # 전체 데이터를 긁은 list인 total을 dataframe으로 변환시켜주면서 각 column의 이름을 부여해줍니다.
        data = pd.DataFrame(my_dictionary)

        # datatitle = input("Please set the title of this excel file : ")  # 긁어온 데이터를 저장할 xlsx 파일의 이름을 지정해줍니다.
        data.to_excel("crawling_data/" + query + "/" +
                      "comments+" + dataTitle + ".xlsx", engine="xlsxwriter")
        # xlsxwriter를 임포트시켜서 engine을 추가하지 않으면, data.to_excel에서 IllegalCharacterError 에러가 뜬다.
