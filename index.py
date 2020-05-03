# encoding=utf-8
from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import os
import string
import time

def getTime():
  return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

def log(info):
  with open('log.log', 'a') as myfile:
    myfile.write(f'[{getTime()}]:{info}\n')

def errlog(err):
  with open('err.log', 'a') as myfile:
    myfile.write(f'[{getTime()}]:{err}\n')

def getDetailPages(page):
  listUrl = f'http://www.yomoer.cn/catalog/templateList?catalogCode=PPTmoban&orderBy=4&catalogId=144&pager.offset={12 * page}'
  log(listUrl)
  detailRes = urlopen(listUrl)
  detailSoup = BeautifulSoup(detailRes.read(), "html.parser", from_encoding="utf-8")
  tags = detailSoup.select('[data-preview]')
  if len(tags) == 0 or page > 2:
    return
  for tag in tags:
    detailId = tag['data-preview']
    nextUrl = f'http://www.yomoer.cn/template/detail/{detailId}.html'
    downloadPPTfromDetailPage(nextUrl)
  getDetailPages(page + 1)


def downloadPPTfromDetailPage(url):
  log(url)
  detailRes = urlopen(url)
  detailSoup = BeautifulSoup(detailRes.read(), "html.parser", from_encoding="utf-8")
  imgTag = detailSoup.find(class_="oldImg")
  imgDataDsrc = imgTag['data-dsrc']
  try:
    dateFd = re.findall(r"/cover/(\d+)/cover", imgDataDsrc)[0]
    idStr = re.findall(r"\d+/cover(.+)/", imgDataDsrc)[0]
    fileName = imgTag['alt']
    durl = f"http://www.yomoer.cn/storeData/ppt/{dateFd}/ppt{idStr}/{fileName}.pptx"
    durl = quote(durl, safe = string.printable)
    dDir = os.path.abspath(os.path.join(os.getcwd(), f'./download/ppt/{dateFd}/'))
    dist = os.path.abspath(os.path.join(dDir, f'{fileName}.pptx'))
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
  except HTTPError as e:
    errlog(f'error:{e.code}, {url}')

getDetailPages(3)
