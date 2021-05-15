import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd

# sw교육 키워드로 검색한 네이버 뉴스의 content, date, title, path 수집 
# 여기서 수집한 path data는 crawling_comments.py에서 활용

# test: 10 page까지 돌려보기 

#for helper in range(1, 43): #100page 단위 -> 잘 끊김
#for helper in range(1, 85): #50page 단위로
for helper in range(1, 3):  ###test : 10page까지
    driver = webdriver.Chrome("./chromedriver")
    
    titles = []
    paths = []
    contents = []
    dates = []
    url = ""

    #i = (50 * (helper - 1)) + 1
    i = (5 * (helper - 1)) + 1
    for page in range(i, 5+i): ### test : 5page씩
    #for page in range(i, 1+i): ###test
        if page == 11: #page는  까지밖에 없음.
            break

        # keyword: sw교육 (query=sw교육)/ sort=0/ ds=시작날짜/ de=끝날짜/ start=10단위로 증가(한페이지 10개)
        start = (page - 1) * 10 + 1
        url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=sw교육&sort=0&ds=&de=&nso=so:r,p:all,a:all&start={}'.format(start)
        #https://search.naver.com/search.naver?where=news&sm=tab_pge&query=sw교육&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=128&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=11
        driver.get(url)
        print("current page : ", page)

        # driver.get(url)로 서버에게 get 요청을 보냈으니 response를 기다려야함. html을 받는데 걸리는 최소시간 -> 1.5s
        time.sleep(1.5)
        soup = bs(driver.page_source, 'html.parser') # 3초가 끝나면 새로운 page의 url로 접속하고 파서가 파싱한다.

        # 현 page에서 네이버뉴스 요소에 접근
        lists = soup.find("div", attrs={"class": "group_news"})
        a_lists = lists.find_all("a", attrs={"class": "info"})  # 현재 페이지의 뉴스 중 모든 네이버뉴스 a tag만 가져옴
        # -> 언론사 링크까지 포함되서 수집됨..(a.info.press라서)

        # path를 추가하기 전에 현재 paths 리스트에 몇개가 들어있는지 확인한다 => 2 page가 되면 paths 리스트의 7번 index부터 읽어야하기 때문
        path_len = len(paths)
        
        for a in a_lists: # 현재 page 내에서 각 네이버뉴스의 path를 파싱하여 paths 배열에 저장.
            if a.attrs["href"].startswith("https://news.naver.com"): # 네이버 뉴스 링크만 저장
                print(a.attrs["href"])
                paths.append(a.attrs["href"])  # 각 네이버뉴스의 path를 저장.

        new_paths = paths[path_len:] # page 별로 해당하는 path만 읽어야하므로 => 2 page가 되면 새로운 index부터 읽어야하기 때문
        print("new_paths : ", new_paths)
        for path in new_paths: # 현재 page의 모든 네이버뉴스의 해당 url에 접속하여 content를 파싱.
            url = path
            driver.get(url)
            soup = bs(driver.page_source, 'html.parser') # 각 url에 대하여 soup 객체를 새로 생성한다.

            # contents 추가하기.
            content = soup.find("div", attrs={"id":"articleBodyContents"})
            data = content.text.strip()
            data = data.replace("\n", "") # \n 문자도 제거
            data = data[61:] # 주석 제거: // flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}
            print('본문 내용 : ', data)

            # titles 추가학기.
            title = soup.find("h3", attrs={"id":"articleTitle"})
            title = title.text.strip()
            title = title.replace("\n", "")

            # date 추가하기.
            date = soup.find("span", attrs={"class": "t11"})
            date = date.text.strip()
            date = date.replace("\n", "")

            contents.append(data) # 공백 제거한 data를 리스트에 저장.
            titles.append(title)
            dates.append(date)
            
    driver.close()
    # 최종 값
    print("paths: ", paths)
    print("titles : ", titles)
    print("contents : ", contents)
    print("dates : ", dates)

    my_dictionary = {"paths": paths, "title": titles, "date": dates, "contents": contents}
    data = pd.DataFrame(my_dictionary)  # 전체 데이터를 긁은 list인 total을 dataframe으로 변환시켜주면서 각 column의 이름을 부여해줍니다.

    str_i = str(i)
    str_i2 = str(i+4)
    datatitle = str_i + '_' + str_i2
    # datatitle = input("Please set the title of this excel file : ")  # 긁어온 데이터를 저장할 xlsx 파일의 이름을 지정해줍니다.
    data.to_excel("crawling_data/" + datatitle + ".xlsx", engine="xlsxwriter")
    #xlsxwriter를 임포트시켜서 engine을 추가하지 않으면, data.to_excel에서 IllegalCharacterError 에러가 뜬다.