from logging_in import Logging
import data_scraping
import subprocess

for i in range(2017,2023):
    for j in range(1,7):
        data = Logging(str(i),str(j))
        data.soup()
        
    