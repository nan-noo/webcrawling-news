import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd

# crawling.py에서 수집한 data에서 path 사용
# 기사 댓글(내용, 좋아요 수, 싫어요 수) 수집 및 반응(좋아요, 훈훈해요, 슬퍼요, 화나요, 후속기사원해요) 수집
# result format: columns - path/title/reaction/comments

for i in range(1,10,5): ### test: 5page단위
#for i in range(1,400,50): ### 50page단위, 400page까지 있음
    driver = webdriver.Chrome("./chromedriver")

    data = pd.read_excel("./crawling_data/" + str(i) +"_" + str(i+4) + ".xlsx") ## test
    #data = pd.read_excel("./crawling_data/" + str(i) +"_" + str(i+49) + ".xlsx")
    paths = data["path"]
    titles = data["title"]

    reactions = []
    comments = []
    #print("current file: " + str(i) +"_" + str(i+49))
    print("current file: " + str(i) +"_" + str(i+4)) ## test

    for path in paths:
        driver.get(path)
        # 서버에게 get 요청을 보냈으니 response를 기다려야함. html을 받는데 걸리는 최소시간 -> 1.5s
        time.sleep(1.5)
        soup = bs(driver.page_source, 'html.parser') # 3초가 끝나면 새로운 page의 url로 접속하고 파서가 파싱한다.

        # 반응 수집
        u_likeit = soup.find("ul", attrs={"class":"u_likeit_layer"})
        u_likeit_counts = u_likeit.find_all("span", attrs={"class":"u_likeit_list_count"}) #좋아요, 훈훈해요, 슬퍼요, 화나요, 후속기사원해요
        reaction = [int(count.text.strip()) for count in u_likeit_counts] # [0,0,0,0,0]
        
        # 댓글 수집 -> 댓글 더보기 페이지로 이동
        total_num_repl = int(soup.find("span", attrs={"class": "u_cbox_count"}).text.strip())
        num_repl = int(soup.find("span", attrs={"class": "u_cbox_info_txt"}).text.strip()) # 삭제 댓글 수 제외 
        if total_num_repl == 0 or num_repl == 0: # 현재 댓글이 없음
            comment = []
        else: # 댓글 더보기로 이동
            driver.find_element_by_css_selector('a.u_cbox_btn_view_comment').click()
            time.sleep(1)

            if total_num_repl > 20:
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
            recomm = [int(count.text.strip()) for count in cbox_recomms]
            unrecomm = [int(count.text.strip()) for count in cbox_unrecomms]

            # zip()을 이용하여 content, recomm, unrecomm 합치기
            comment = [com for com in zip(content, recomm, unrecomm)] # [(c,r,u), ... ]

        # reactions, comments에 append
        reactions.append(reaction)
        comments.append(comment)
    
    driver.close()
    # 최종 값
    print("paths: ", paths)
    print("titles : ", titles)
    print("reactions : ", reactions)
    print("comments : ", comments)

    my_dictionary = {"path": paths, "title": titles, "reaction": reactions, "comments": comments}
    data = pd.DataFrame(my_dictionary)  # 전체 데이터를 긁은 list인 total을 dataframe으로 변환시켜주면서 각 column의 이름을 부여해줍니다.

    str_i = str(i)
    # str_i2 = str(i+49)
    str_i2 = str(i+4) ### test
    datatitle = str_i + '_' + str_i2
    # datatitle = input("Please set the title of this excel file : ")  # 긁어온 데이터를 저장할 xlsx 파일의 이름을 지정해줍니다.
    data.to_excel("crawling_data/comments" + datatitle + ".xlsx", engine="xlsxwriter")
    #xlsxwriter를 임포트시켜서 engine을 추가하지 않으면, data.to_excel에서 IllegalCharacterError 에러가 뜬다.





