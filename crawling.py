import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd

# sw교육 키워드로 검색한 네이버 뉴스의 path(링크), title, date, content, press(언론사) 수집
# 여기서 수집한 path data는 crawling_comments.py에서 활용
# 네이버 검색은 최상의 검색결과 품질을 위해 뉴스 검색결과를 4,000건까지 제공합니다. -> 400page까지 제공됨
# -> 월 단위로 수집

# test: 10 page까지 돌려보기

# https://search.naver.com/search.naver?where=news&query=인공지능교육&sm=tab_opt&sort=1&photo=0&field=0&pd=3&ds=2021.07.06&de=2018.01.01&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Afrom20180101to20210706&is_sug_officeid=0

query = "SW교육" # "SW교육", "AI교육", "ICT교육"
sort = "2" # 오래된 순
date = [
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
             ("2019.10.01", "2019.10.31"), ("2019.11.01", "2019.11.30"), ("2019.12.01", "2019.12.31"), \
    ("2020.01.01", "2020.01.31"), ("2020.02.01", "2020.02.29"), ("2020.03.01", "2020.03.31"), \
     ("2020.04.01", "2020.04.30"), ("2020.05.01", "2020.05.31"), ("2020.06.01", "2020.06.30"), \
         ("2020.07.01", "2020.07.31"), ("2020.08.01", "2020.08.31"), ("2020.09.01", "2020.09.30"), \
             ("2020.10.01", "2020.10.31"), ("2020.11.01", "2020.11.30"), ("2020.12.01", "2020.12.31"), \
    ("2021.01.01", "2021.01.31"), ("2021.02.01", "2021.02.28"), ("2021.03.01", "2021.03.31"), \
     ("2021.04.01", "2021.04.30"), ("2021.05.01", "2021.05.31"), ("2021.06.01", "2021.06.30"), \
         ("2021.07.01", "2021.07.09")]#, ("2021.08.01", "2021.08.31"), ("2021.09.01", "2021.09.30"), \
             #("2021.10.01", "2021.10.31"), ("2021.11.01", "2021.11.30"), ("2021.12.01", "2021.12.31")]
# dateStart = "2018.01.01"
# dateEnd = "2018.01.31" 

for dateStart, dateEnd in date:
    #for helper in range(1, 3):  ###test : 10page까지
    for helper in range(1, 5):
        driver = webdriver.Chrome("./chromedriver")
        
        titles = []
        paths = []
        contents = []
        dates = []
        press = []
        url = ""

        #i = (5 * (helper - 1)) + 1 ### test
        i = (100 * (helper - 1)) + 1
        #for page in range(i, 5+i): ### test : 5page씩
        for page in range(i, 100+i): # 50page 단위로 수집
            # if page == 231: #page는 최대 400page 까지밖에 없음.
            #     break

            # keyword: sw교육 (query=sw교육)/ sort=1(최신순)/ ds=시작날짜/ de=끝날짜/ start=10단위로 증가(한페이지 10개)
            start = (page - 1) * 10 + 1
            url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=' + query +'&sort=' + sort + '&ds=' + dateStart + '&de=' + dateEnd + '&nso=so%3Add%2Cp%3Afrom' + dateStart.replace('.', '') + 'to' + dateEnd.replace('.', '') + '&start={}'.format(start)

            driver.get(url)

            # driver.get(url)로 서버에게 get 요청을 보냈으니 response를 기다려야함. html을 받는데 걸리는 최소시간 -> 1.5s
            time.sleep(1.5)
            soup = bs(driver.page_source, 'html.parser') # 3초가 끝나면 새로운 page의 url로 접속하고 파서가 파싱한다.
            
            # page not found면 break
            if soup.find("div", attrs={"class": "not_found02"}) is not None:
                print("not found")
                break

            print("current page : ", page)

            # 현 page에서 네이버뉴스 요소에 접근
            lists = soup.find("div", attrs={"class": "group_news"})
            a_lists = lists.find_all("a", attrs={"class": "info"})  # 현재 페이지의 뉴스 중 모든 네이버뉴스 a tag만 가져옴
            # -> 언론사 링크까지 포함되서 수집됨..(a.info.press라서)

            # path를 추가하기 전에 현재 paths 리스트에 몇개가 들어있는지 확인한다 => 2 page가 되면 paths 리스트의 7번 index부터 읽어야하기 때문
            path_len = len(paths)

            # 현재 page 내에서 각 네이버뉴스의 path를 파싱하여 paths 배열에 저장.
            for a in a_lists: 
                if a.attrs["href"].startswith("https://news.naver.com"): # 네이버 뉴스 링크만 저장
                    paths.append(a.attrs["href"])  # 각 네이버뉴스의 path를 저장.

            new_paths = paths[path_len:] # page 별로 해당하는 path만 읽어야하므로 => 2 page가 되면 새로운 index부터 읽어야하기 때문
            #print("new_paths : ", new_paths)
            
            # 현재 page의 모든 네이버뉴스의 해당 url에 접속하여 content를 파싱.
            for path in new_paths: 
                print("current path: ", path)
                driver.get(path)
                soup = bs(driver.page_source, 'html.parser') # 각 url에 대하여 soup 객체를 새로 생성한다.

                # contents 추가하기.
                content = soup.find("div", attrs={"id":"articleBodyContents"})

                if content is None: 
                    paths.remove(path)
                    path_len -= 1
                    continue

                data = content.text.strip().replace("\n", "") # \n 문자도 제거
                data = data[61:] # 주석 제거: // flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}
                #print('본문 내용 : ', data)

                # titles 추가학기.
                title = soup.find("h3", attrs={"id":"articleTitle"})
                title = title.text.strip().replace("\n", "")

                # date 추가하기.
                date = soup.find("span", attrs={"class": "t11"})
                date = date.text.strip().replace("\n", "")

                # press 추가하기
                print(soup.find("a", attrs={"class": "nclicks(atp_press)"}).find("img").get("title").strip())
                press.append(soup.find("a", attrs={"class": "nclicks(atp_press)"}).find("img").get("title").strip())

                contents.append(data) # 공백 제거한 data를 리스트에 저장.
                titles.append(title)
                dates.append(date)
                
        driver.close()
        # 최종 값
        print("paths: ", len(paths))
        print("titles : ", len(titles))
        print("contents : ", len(contents))
        print("dates : ", len(dates))
        print("press: ", len(press))

        my_dictionary = {"path": paths, "title": titles, "date": dates, "press": press, "content": contents}
        data = pd.DataFrame(my_dictionary)  # 전체 데이터를 긁은 list인 total을 dataframe으로 변환시켜주면서 각 column의 이름을 부여

        str_i = str(i)
        # str_i2 = str(i+4) ### test
        str_i2 = str(i+99)
        datatitle = dateStart + "-" + dateEnd + "+" + str_i + '_' + str_i2

        #xlsxwriter를 임포트시켜서 engine을 추가하지 않으면, data.to_excel에서 IllegalCharacterError 에러가 뜬다.
        data.to_excel("crawling_data/" + query + "/" + datatitle + ".xlsx", engine="xlsxwriter")
        