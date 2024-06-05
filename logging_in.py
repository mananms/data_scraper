#the neccessary imports
import time
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import re
import pandas as pd
from bs4 import BeautifulSoup

service=Service(executable_path="chromedriver.exe")
driver=webdriver.Chrome(service=service)

class Logging:
    def __init__(self,year,round):
        self.round = round
        self.year = year

    def soup(self):
        soup=BeautifulSoup(self.call(), 'lxml')

        #create lists to store the values
        round_no=[]
        year=[]
        institutes=[]
        branches=[]
        genders=[]
        quotas=[]
        categories=[]
        opening_ranks=[]
        closing_ranks=[]

        #find the table element containing all the values
        table=soup.find('div',class_='table-responsive')
        table_row=table.find_all_next('tr')

        #append the values to their respective lists
        for tr in table_row:
            info=tr.find_all_next('td')
            institutes.append(info[0].text)
            branches.append(info[1].text)
            quotas.append(info[2].text)
            categories.append(info[3].text)
            genders.append(info[4].text)
            opening_ranks.append(info[5].text)
            closing_ranks.append(info[6].text)

        #for explicitly adding round and year to the data frame
        for i in range(len(institutes)):
            round_no.append(self.round)
            year.append(self.year)

        #create a dataframe with the lists(of extracted data ) as columns
        df=pd.DataFrame(list(zip(year,round_no,institutes,branches,quotas,categories, genders, opening_ranks,closing_ranks)),
                columns=['Year','Round','Institutes','Academic Program','Quota','Seat Type','Gender', 'Opening Rank','Closing Rank'])



        # saving the data to csv file
        df.to_csv(path_or_buf=self.year+'-'+self.round+'.csv')

    def call(self):
        print("Fetching the data for you")

        #navigating to the JOSAA website
        # this link is only for the data of 2016-2022 
        # for data of 2023 use 'https://josaa.admissions.nic.in/applicant/SeatAllotmentResult/CurrentORCR.aspx'
        driver.get('https://josaa.admissions.nic.in/applicant/seatmatrix/OpeningClosingRankArchieve.aspx')

        # make the  dropdown visible first then select

        #select the year
        driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_ddlYear').style.display = 'block';")
        year_no=driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ddlYear')
        select_year_no=Select(year_no)
        select_year_no.select_by_visible_text(self.year)

        #select the round no
        driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_ddlroundno').style.display = 'block';")
        round_no=driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ddlroundno')
        select_round_no=Select(round_no)
        select_round_no.select_by_visible_text(self.round)



        # select the institute type
        driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_ddlInstype').style.display = 'block';")
        institute_type=driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ddlInstype')
        select_institute_type=Select(institute_type)
        select_institute_type.select_by_visible_text('ALL')



        #select the institute name
        driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_ddlInstitute').style.display = 'block';")
        institute_name=driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ddlInstitute')
        select_institute_name=Select(institute_name)
        select_institute_name.select_by_visible_text('ALL')



        #select the academic program
        driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_ddlBranch').style.display = 'block';")
        branch_name=driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ddlBranch')
        select_branch_name=Select(branch_name)
        select_branch_name.select_by_visible_text('ALL')



        #select the seat type/category
        driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_ddlSeatType').style.display = 'block';")
        seat_type=driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ddlSeatType')
        select_seat_type=Select(seat_type)
        select_seat_type.select_by_visible_text('ALL')



        #click the submit button
        driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_btnSubmit').click()

        # transfer the page source to another variable for further use
        mp = driver.page_source

        time.sleep(3)
        return mp
# set up the web driver


# take the input from the user
# here we consider user wants to see al the institutes of a given type for specified year and round
# if you want to search for a specific institute,branch or seat type just change 'ALL' to whatever you want
# institute_type_entered=input('Enter the type of institute')

