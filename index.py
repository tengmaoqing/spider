# encoding=utf-8
from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import os
import string
import time
import socket

socket.setdefaulttimeout(120) 

def getTime():
  return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

def log(info):
  with open('log.log', 'a', encoding="utf-8") as myfile:
    myfile.write(f'[{getTime()}]:{info}\n')
    myfile.close()

def errlog(err):
  with open('err.log', 'a', encoding="utf-8") as myfile:
    myfile.write(f'[{getTime()}]:{err}\n')
    myfile.close()

def getDetailPages(page):
  listUrl = f'http://www.yomoer.cn/catalog/templateList?catalogCode=PPTmoban&orderBy=4&catalogId=144&pager.offset={12 * page}'
  log(listUrl)
  detailRes = urlopen(listUrl)
  detailSoup = BeautifulSoup(detailRes.read(), "html.parser", from_encoding="utf-8")
  tags = detailSoup.select('[data-preview]')
  if len(tags) == 0 or page > 250:
    return
  for tag in tags:
    detailId = tag['data-preview']
    nextUrl = f'http://www.yomoer.cn/template/detail/{detailId}.html'
    downloadPPTfromDetailPage(nextUrl)
  getDetailPages(page + 1)


def downloadPPTfromDetailPage(url):
  log(url)
  try:
    detailRes = urlopen(url)
    detailSoup = BeautifulSoup(detailRes.read(), "html.parser", from_encoding="utf-8")
  except Exception:
    errlog(f'err, {url}')
    return
  imgTag = detailSoup.find(class_="oldImg")
  tags = detailSoup.select('.catalog-detailmore .tips span')
  imgDataDsrc = imgTag['data-dsrc']
  try:
    tagStr = ','.join(map(lambda tag: tag.contents[0], tags))
    dateFd = re.findall(r"/cover/(\d+)/cover", imgDataDsrc)[0]
    idStr = re.findall(r"\d+/cover(.+)/", imgDataDsrc)[0]
    fileName = imgTag['alt']
    durl = f"http://www.yomoer.cn/storeData/ppt/{dateFd}/ppt{idStr}/{quote(fileName)}.pptx"
    # durl = quote(durl)
    dDir = os.path.abspath(os.path.join(os.getcwd(), f'./download/ppt/{dateFd}/'))
    dist = os.path.abspath(os.path.join(dDir, f'{tagStr}&&{fileName}.pptx'))
  except IndexError as err:
    errlog(f'indexError: {url}')
    return
  # return
  try:
    f = urlopen(durl)
    data = f.read()
    if not os.path.exists(dDir):
      os.makedirs(dDir)
    with open(dist, 'wb') as outfile:
      outfile.write(data)
      outfile.close()
    log(f'{fileName} over')
  except HTTPError as e:
    errlog(f'error:{e.code}, {durl}')
  except Exception:
    errlog(f'download error: {durl}')

getDetailPages(116)
# downloadPPTfromDetailPage('http://www.yomoer.cn/template/detail/5244.html')