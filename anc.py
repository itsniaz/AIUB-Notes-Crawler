#Author : Niaz Ahmed
#Bug Reports : mr.niaz@live.com

import os
import sys


from  bs4 import BeautifulSoup as BS
from urllib.parse import unquote
import urllib.request
import requests as rs

base_url = "https://portal.aiub.edu"
course_url = base_url

username = input("Enter AIUB ID : ")
password = input("Enter AIUB Password : ")
TEMP_URL =  base_url
course_titles = []
course_links =[]

course_pages =[]

sem_url = []

count = 0
s = rs.session();
def download_page():
    try:
        homepage = s.post(base_url,data={'username':username,'password':password})
    except Exception:
        print("Unable to connect :( Check your netwrok connection.")
        sys.exit(0)
    homepage = homepage.content
    return homepage

def parse():
    soup = BS(download_page(),'html.parser')
    return soup

def get_reg_url():
    soup = parse()
    try:
        soup = soup.findAll('ul', attrs={'class': 'nav navbar-nav hidden-sm hidden-xs'})[0]
        soup = soup.findAll('a')[1]['href']
    except IndexError:
        print("Ooops ! Wrong ID/Pass or connectivity issue maybe.")
        sys.exit(0)
    global course_url
    course_url =  course_url+ str(soup)
    get_semesters(course_url)

def get_semesters(url):
    data = s.get(url).content
    newsoup = BS(data,"html.parser")
    newsoup = newsoup.find('select',attrs={'class' : 'btn btn-default form-control'})
    newsoup = newsoup.findAll('option')
    for each in newsoup:
        sem_url.append(TEMP_URL+each['value'])

    

def download_a_page(url):
    coursepage = s.get(url).content
    soup = BS(coursepage,"html.parser")
    return soup

def extract_course_page():
    sem_url.reverse()
    for each in sem_url:  
        soup = download_a_page(unquote(each))
        soup = soup.find('tbody')
        soup = soup.findAll('a')
        for s in soup:
            global courses
            global course_links
            global course_titles
            t = s.string.replace('/',',')
            t = t.split('-')[1]
            course_titles.append(t)
            course_links.append(base_url+s.get('href'))

def get_course_pages():
    global course_pages
    global course_links

    
    for link in course_links:
        resp = s.get(link).content
        soup = BS(resp,"html.parser")
        course_pages.append(soup)
     

def get_course_notes():
    i=0
    n = username
    makefolder(n)
    os.chdir(n)
    for page in course_pages:
        soup = page.findAll('div', attrs={'class': 'col-md-12'})[1]
        soup = soup.findAll('a')
    
        #Making Folder for course notes
        folder_name = course_titles[i]
        makefolder(folder_name)
        os.chdir(folder_name)
        #os.system('cls')
        print("Downloading Notes Of "+course_titles[i].split('[')[0])
        if len(soup)!=0:
            for s in soup:
                note_title = s.string
                link = base_url+unquote(s.get('href'))
                if note_title is not None and link is not None:
                    if not os.path.isfile(note_title):
                        dloader(note_title,link)
            print("Done")
        else:
            pass 
        os.chdir('..')  
        i+=1

    os.system('cls')
    print("Downloding Completed.....")
    print(str(count)+" new file/s added to the library")
    print("Check the directory where this programme is located..")

def makefolder(name):
    current_dir = os.getcwd()
    final_directory = os.path.join(current_dir,name)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

def dloader(file_name,url):
    global count
    count+=1
    req = s.get(url)
    file = open(file_name, 'wb')
    for chunk in req.iter_content(100000):
        file.write(chunk)
    file.close()


def main():
    global username
    global password
    
    os.system('cls')
    print("Please wait for a while....")
    get_reg_url()    
    extract_course_page()
    get_course_pages()
    get_course_notes()

main()
s.close()
input()



