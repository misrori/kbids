import requests
import pandas as pd
import datetime
import pickle
import os

cookies = {
    '_ga': 'GA1.1.772192671.1734972176',
    '_ga_NRGJ8GQQR3': 'GS1.1.1734972176.1.1.1734972732.0.0.0',
    'dtCookie7gis1lmx': 'v_4_srv_1_sn_AE89CE2F93D027DD30EB8B8E36D3EE35_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
    'rxVisitor7gis1lmx': '1736264799725IOJ7IRJ673H93E13OE60HNG48JGMHARO',
    'XSRF-TOKEN': '827fb012-52f8-4e89-9b84-02e900f6fc06',
    'ekr_language': 'hu',
    'dtSa7gis1lmx': '-',
    'rxvt7gis1lmx': '1736285532461|1736283517929',
    'dtPC7gis1lmx': '1$483633819_1h20vCAJCRPPRIBWINDMPNQJABMRPURFIUCON-0e0',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'Cookie': '_ga=GA1.1.772192671.1734972176; _ga_NRGJ8GQQR3=GS1.1.1734972176.1.1.1734972732.0.0.0; dtCookie7gis1lmx=v_4_srv_1_sn_AE89CE2F93D027DD30EB8B8E36D3EE35_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1; rxVisitor7gis1lmx=1736264799725IOJ7IRJ673H93E13OE60HNG48JGMHARO; XSRF-TOKEN=827fb012-52f8-4e89-9b84-02e900f6fc06; ekr_language=hu; dtSa7gis1lmx=-; rxvt7gis1lmx=1736285532461|1736283517929; dtPC7gis1lmx=1$483633819_1h20vCAJCRPPRIBWINDMPNQJABMRPURFIUCON-0e0',
    'Referer': 'https://ekr.gov.hu/ekr-szerzodestar/hu/szerzodesLista',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'x-dtpc': '1$483633819_1h20vCAJCRPPRIBWINDMPNQJABMRPURFIUCON-0e0',
}

params = {
    'offset': '0',
    'limit': '120',
    'apikey': 'PSZT',
}

response = requests.get(
    'https://ekr.gov.hu/ekr-szerzodestar/rest/szerzodesapi/1.0/szerzodesek',
    params=params,
    cookies=cookies,
    headers=headers,
    verify=False,
)


t = response.json()

osszes = t['totalRecords']
# round up to 10000
max_page = round(osszes / 10000) * 10000 + 10000

all_data = []
ofsetek = list(range(0, max_page, 10000))

for offset in ofsetek:
    print(offset)
    params = {
        'offset': str(offset),
        'limit': '10000',
        'apikey': 'PSZT',
    }
    response = requests.get(
        'https://ekr.gov.hu/ekr-szerzodestar/rest/szerzodesapi/1.0/szerzodesek',
        params=params,
        cookies=cookies,
        headers=headers,
        verify=False,
    )
    t = response.json()
    all_data.extend(t['szerzodesAlapadat'])


data = pd.DataFrame(all_data)


today = datetime.date.today()
today_str = today.strftime("%Y_%m_%d")

id_folder = 'kbids'
if not os.path.exists(id_folder):
    os.makedirs(id_folder)

new_filepath = f'{id_folder}/data_{today_str}.piclke'

with open(new_filepath, 'wb') as f:
    pickle.dump(new_data, f)



