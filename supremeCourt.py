#!/usr/bin/env python
# -*- coding: utf-16 -*-

# ------------------------------------------------------------
import multiprocessing
import os
import logging
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import pandas as pd


def loggerInit(logFileName):
    try:
        os.makedirs("logs")
    except:
        pass
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
    file_handler = logging.FileHandler(f'logs/{logFileName}')
    # file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    # stream_handler.setLevel(logging.ERROR)
    logger.addHandler(stream_handler)
    return logger


logger = loggerInit(logFileName="supremeCourt.bot.log")

import requests

def searchModule(PublishFrom, PublishTo, translationPublishFrom, translationPublishTo):

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'opEueMonUID=u_j24ztno1jrlla0smx8w; ASP.NET_SessionId=bfcoba1m4lqal4tne15eta0n; TS0164e775=01ea5d8107b53639b5a9a09bf130af9a7bd80552b76a5cf84907e8c586df623a71276ab54ab7afbc156ca16860a93f1cca802123b6b295985ddeacb7faa0ec6ae9bf60b410',
        'DNT': '1',
        'Origin': 'https://supremedecisions.court.gov.il',
        'Referer': 'https://supremedecisions.court.gov.il/Verdicts/Search/1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    json_data = {
        'document': {
            'Year': None,
            'Counsel': [
                {
                    'Text': '',
                    'textOperator': 2,
                    'option': '2',
                    'Inverted': False,
                    'Synonym': False,
                    'NearDistance': 3,
                    'MatchOrder': False,
                },
            ],
            'CaseNum': None,
            'Technical': None,
            'fromPages': '2',
            'toPages': None,
            'dateType': 1,
            # 'PublishFrom': '2022-10-02T18:30:00.000Z',
            'PublishFrom': PublishFrom,
            # 'PublishTo': '2022-11-02T18:30:00.000Z',
            'PublishTo': PublishTo,
            'publishDate': 8,
            'translationDateType': 1,
            # 'translationPublishFrom': '2022-10-11T07:12:11.231Z',
            'translationPublishFrom': translationPublishFrom,
            # 'translationPublishTo': '2022-11-11T07:12:11.231Z',
            'translationPublishTo': translationPublishTo,
            'translationPublishDate': 8,
            'SearchText': [
                {
                    'Text': '',
                    'textOperator': 1,
                    'option': '2',
                    'Inverted': False,
                    'Synonym': False,
                    'NearDistance': 3,
                    'MatchOrder': False,
                },
            ],
            'Judges': None,
            'Parties': [
                {
                    'Text': '',
                    'textOperator': 2,
                    'option': '2',
                    'Inverted': False,
                    'Synonym': False,
                    'NearDistance': 3,
                    'MatchOrder': False,
                },
            ],
            'Mador': None,
            'CodeMador': [],
            'TypeCourts': None,
            'TypeCourts1': None,
            'TerrestrialCourts': None,
            'LastInyan': None,
            'LastCourtsYear': None,
            'LastCourtsMonth': None,
            'LastCourtCaseNum': None,
            'Old': False,
            'JudgesOperator': 2,
            'Judgment': None,
            'Type': None,
            'CodeTypes': [],
            'CodeJudges': [],
            'Inyan': None,
            'CodeInyan': [],
            'AllSubjects': [
                {
                    'Subject': None,
                    'SubSubject': None,
                    'SubSubSubject': None,
                },
            ],
            'CodeSub2': [],
            'Category1': None,
            'Category3': None,
            'CodeCategory3': [],
            'Volume': None,
            'Subjects': None,
            'SubSubjects': None,
            'SubSubSubjects': None,
        },
        'lan': '1',
    }

    response = requests.post('https://supremedecisions.court.gov.il/Home/SearchVerdicts',
                             headers=headers, json=json_data)
    rawDataDump = response.json()
    return rawDataDump


def parseDataset(rawDataDump):
    return [f"https://supremedecisions.court.gov.il/Home/Download?path={x['Path']}&fileName={x['FileName']}&type=2"
     for x in rawDataDump['data']]


def downloadFile(filePath):
    fileName = re.findall("fileName=([^&]+)&", filePath)[0] + ".html"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    response = requests.get(filePath, headers=headers)
    aa = response.text

    open("Downloaded HTML/"+fileName,"w", encoding='UTF-16').write(response.text)
    logger.debug("Downloaded " + fileName)


def core(StartDate, StopDate):
    '''
    StartDate = ("2022-10-03")
    StopDate = ("2022-11-03")
    '''
    try: os.makedirs("Downloaded HTML")
    except: pass

    StartDate = datetime.strptime(StartDate, '%Y-%m-%d')
    StopDate = datetime.strptime(StopDate, '%Y-%m-%d')

    StartDate = (StartDate - timedelta(days=1)).strftime('%Y-%m-%d')
    StopDate = (StopDate - timedelta(days=1)).strftime('%Y-%m-%d')

    PublishFrom = StartDate+'T18:30:00.000Z'
    PublishTo = StopDate+'T18:30:00.000Z'

    translationPublishFrom = (datetime.today() - timedelta(weeks=4)).strftime('%Y-%m-%d')
    translationPublishTo = datetime.today().strftime('%Y-%m-%d')

    translationPublishFrom = translationPublishFrom+'T07:12:11.231Z'
    translationPublishTo = translationPublishTo+'T07:12:11.231Z'

    rawDataDump = searchModule(PublishFrom, PublishTo, translationPublishFrom, translationPublishTo)
    pd.DataFrame.from_dict(rawDataDump['data']).to_csv("Downloaded HTML/refrenceTable.csv")
    listOfFiles = parseDataset(rawDataDump)

    with ThreadPoolExecutor(max_workers=(multiprocessing.cpu_count() * 10)) as executor:
        results = []
        for filePath in listOfFiles:
            executor.submit(downloadFile, filePath)
        executor.shutdown(wait=True)
