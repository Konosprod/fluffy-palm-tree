import sys
import json
from bs4 import BeautifulSoup
import urllib3.request
import certifi
import hashlib
# progressbar is provided by progressbar2 on PYPI.
from progressbar import DataTransferBar
from requests_download import download, HashTracker, ProgressTracker



user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where(), headers=user_agent)

hasher = HashTracker(hashlib.sha256())
progress = ProgressTracker(DataTransferBar())

def downloadEp(ep):
    src = BeautifulSoup(http.request("GET", "http://anime.megamanonline.org" + ep.p.a["href"]).data, "html.parser")
    vimeourl = src.find("iframe")["src"]

    index = vimeourl.rindex("/")+1
    idvid = vimeourl[index:index+8]
    vimeourl = "https://player.vimeo.com/video/"+idvid

    res = ""
    try:
        res = json.loads(http.request("POST", vimeourl+"/check-password?referrer=http://www.google.com", fields={"password": "bWVnYW1hbg==&Watch Video="}).data.decode("utf-8"))
    except:
        print("Unable to download : " + ep.p.text.strip())
        sys.stdout.flush()
        return
    
    print("Downloading : " + ep.p.text.strip())
    sys.stdout.flush()
    download(res["request"]["files"]["progressive"][0]["url"], res["video"]["title"]+".mp4", trackers=(hasher, progress))

    return

if __name__ == "__main__":

    source = BeautifulSoup(http.request("GET", sys.argv[1]).data, "html.parser")

    eps = source.find_all("td", {"class":"list-title"})

    for ep in eps:
        downloadEp(ep)
