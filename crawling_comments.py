import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd

for i in range(1,11,5): ### test: 5page단위
    data = pd.read_excel("./crawling_data/" + str(i) +"_" + str(i+4) + ".xlsx")
