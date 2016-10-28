import mechanize
import webbrowser
from bs4 import BeautifulSoup
import time
import csv


fbids=[]
with open('friendlist.csv', 'rb') as f:
    reader = csv.reader(f)
        
    for row in reader:
        url = "http://findmyfbid.com/"
        br = mechanize.Browser()
        br.set_handle_robots(False) # ignore robots
        br.open(url)
        br.select_form(nr=0)
        br["url"] = row[2]
        res = br.submit()
        content = res.read()
        
        soup = BeautifulSoup(content)
        for item in soup.find_all("div", attrs={"class":"container"}):
            if item.find_all("h1", attrs={"class":"text-danger"}):
                print("error")
                fbids.append("error") 
            else:
                for code in item.find_all("code"):
                    print (code.contents)
                    fbids.append(code.contents)

with open('ids.csv', 'wb') as w:
    csvwriter= csv.writer(w, delimiter=' ', quotechar ='|')
    for element in fbids:
        csvwriter.writerow(element)
     
    

