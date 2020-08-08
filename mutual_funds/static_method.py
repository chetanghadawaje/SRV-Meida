from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests


def get_data(date=None):
    if not date:
        date = datetime.today() - timedelta(days=1)
        date = date.strftime('%d-%b-%Y')
    url = "http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?mf=53&tp=1&frmdt=" + date + "&todt=" + date
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    mf_dict = {}
    for line in soup.get_text().split("\n"):
        if line[:6].isdigit():
            temp_data = line.split(";")
            mf_dict[temp_data[1]] = temp_data[4]
    return mf_dict
