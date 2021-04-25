
from selenium import webdriver
from bs4 import BeautifulSoup
import boto3
import time
import csv
import re

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=options)

# current hack to get draft ids list - use JS in console:
# let ids = []
# let info = document.querySelectorAll('.info')
# info.forEach(i => ids.push(i.children[0].getAttribute('href').slice(11)))

# To delete items - 
# dynamo = boto3.resource('dynamodb', region_name='us-west-2')
# table = dynamo.Table('nfl-mock-drafts-2021')
# scan = table.scan()
# with table.batch_writer() as batch:
#     for each in scan['Items']:
#         batch.delete_item(
#             Key={
#                 'position': each['position'],
#                 'draft_id': each['draft_id']
#             }
#         )


draft_ids = ["DzDCTM8IcM", "B9NVqlIJVy", "KiDJ0ZSr5j", "NGwIOEACJV", "iRkJV9ThCD", "rESVBpd6Zm", "5vCVD5WIkb", "cYQYExLEvg", "LtusOHSgu1", "LyFCdgPAl0", "mPbak6GCwR", "17HAGeVPGF", "GysD2s6pa2", "OE4A9dEPcz", "qis7dag77A", "mkKWuJy94R", "ES0htZoXMc", "XGTSnvgY6q", "CSHKXIvH2N", "qYmCdLJwjC", "8JvNEn6VeZ", "q75yk4RxFc", "RLCmp6NMi5", "YJ4Ve5obzN", "vJdErP5JVn", "efpk6OdeIr", "maGQICUbVf", "LbxjwEUcy7", "Iedh7tIGfI", "u6DKZbvWOC", "NCcIjmNAAg", "YEiNTbLzO9", "0Av0Fj89B2", "H7hnzoX1BA", "v2yQLO3iAX", "eRlQocFGrM", "xLTGBlSvL3", "P3E6PPaIsI", "Qixo0Le1rf", "CZHOMLDz0T", "IKW6IiuBMu", "lqimwPFr7T", "JlwewfjeWF", "ocH7lirAAE", "0EZzyBfApD", "KAxHhL39DU", "kMhqkOVpsm", "sATyK1CrTE", "cEgx27MtCm", "FD1UwkHidZ", "ZvZOzjKvf7", "CQDfEoQPmp", "mLk1vfJPSn", "NHsS4wRmoU", "njrMFmMjpE", "bnpnXMUcBC", "FaZl609LlZ", "Jlb6HucvAe", "vd82CJeqh2", "XpAd3diz9D", "sCbwDqCA97", "F79x0EUy7w", "tiHlft6GjJ", "cW6Sh0cYn5", "SO75RgF6k2", "6rc9Aulg29", "Nil98PIiyq", "DrXEE7oBz3", "zSyafriXPB", "Vgr5JC65tu", "eLb38jh0yN", "wc3dyubmYv", "dwhwI0KA1H", "sKgYJdftSF", "1EYWeHDkpn", "MyGo2hvD0I", "e2K2c1i7t8", "2BWxkfyAej", "HGH8lTBRje", "MPltahciEW", "J9DxRO30pW", "0XPo93z7Pu", "LIbBSeYfyj", "TVaDwNJ7xX", "cHouIXDHVX", "2oJr0VgpeH", "2CEwPinRzm", "P7GpVNrMtR", "XwBI0dRQ6G", "262vRxXgX7", "D3BsHLZ0QR", "uAXhNYUmJ8", "VyOMBX8roU", "QpdHTrkY19", "0ZCD1qdEAF", "LmnaDLgAjw", "SZY3nABkow", "NZ3Q2MjONm", "aS47YJd3nd", "EFlXiOiEqm"]

for idx, draft_id in enumerate(draft_ids, start=1):

    driver.get(f"https://thedraftnetwork.com/mockDraft/{draft_id}")
    li_list = driver.find_elements_by_class_name("picks-paginate-links--round")

    ads = driver.find_elements_by_class_name("popup-banner")

    mock_draft = list()
    pattern = re.compile('[\W_]+')

    for x in range(len(li_list)):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pick_numbers = soup.find_all('h6', {"class": "pick-number"})
        team_names = soup.find_all('div', {"class": "team-name"})
        player_names = soup.find_all('div', {"class": "player-name"})
        player_positions = soup.find_all('span', {"class": "player-info"})
        player_schools = soup.find_all('span', {"class": "player-school"})
    
        # print(player_names)
        for pick_idx in range(len(pick_numbers)):
            pick = list()
            pick.append(pick_numbers[pick_idx].string[:-1])
            pick.append(team_names[pick_idx].string)
            pick.append(player_names[pick_idx].string)
            pick.append(pattern.sub('', player_positions[pick_idx].contents[0]))
            pick.append(player_schools[pick_idx].string)
            mock_draft.append(pick)
            print(pick)
        
        time.sleep(1)
        # print(pick_info)            
        if x < len(li_list) - 1:
            print(li_list[x+1].text)
            driver.execute_script("arguments[0].click();", li_list[x + 1])

    # print('MOCK DRAFT')
    print(mock_draft)
    s3_client = boto3.client('s3')

    with open('/tmp/test.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Position', 'Team', 'Player_Name', 'Player_Position', "Player_Team"
        ])
        writer.writerows(mock_draft)
        s3_client.upload_file(
            Filename='/tmp/test.csv', 
            Bucket='nfl-mock-drafts-2021', 
            Key=f'mock_draft_{idx}.csv')


    dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')

    for pick in mock_draft:
        dynamodb_client.put_item(
            TableName='nfl-mock-drafts-2021',
            Item={
                'draft_id': {'S': str(idx)},
                'position': {'S': pick[0]},
                'team': {'S': pick[1]},
                'player_name': {'S': pick[2]},
                'player_position': {'S': pick[3]},
                'player_team': {'S': pick[4]}
            }
        )

