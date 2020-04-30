import re

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
mainURL = "https://www.indeed.fr"
URL = "https://www.indeed.fr/emplois?q=intelligence%20artificielle&l=France"

number_result = 50


def remove_html_tags(text):
    # Remove html tags from a string
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

columns = ["Job Title", "Job URL", "Job Description"]

sample_df = pd.DataFrame(columns=columns)

for start in range(0, number_result, 10):
    page = requests.get(URL + "&start=" + str(start))
    time.sleep(1)  # ensuring at least 1 second between page grabs
    soupMain = BeautifulSoup(page.text, "lxml")
    for div in soupMain.find_all(name="div", attrs={"class": "row"}):
        # specifying row num for index of job posting in dataframe
        num = (len(sample_df) + 1)
        # creating an empty list to hold the data for each posting
        job_post = []
        # grabbing the job title, the job URL and the job summary
        for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
            job_post.append(a["title"])
            job_url = mainURL + a["href"]
            job_post.append(job_url)
            job_soup = BeautifulSoup(requests.get(job_url).text, 'lxml')
            for summ in job_soup.find_all(name="div", attrs={"id": "jobDescriptionText"}):
                text = remove_html_tags(str(summ))
                job_post.append(text)
        sample_df.loc[num] = job_post


sample_df.to_csv("result.csv", encoding="utf-8")
