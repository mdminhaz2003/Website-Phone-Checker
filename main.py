from bs4 import BeautifulSoup
import requests as req
import pandas as pd
import re

regex_href = re.compile(r'tel:[\d\+\ \_\(\)\.\{\}\%\$\@\#\~-]+')
regex_phone = r"([\d\+\ \_\(\)\.\{\}-]+)"
filename = input('Enter your excel file name with extensions : ')
data = pd.read_excel(filename).fillna('').to_numpy()
for website in data:
    if re.search(r"^https://www\.", website[0]):
        pass
    elif re.search(r"^www\.", website[0]):
        website[0] = f'https://{website[0]}'
    elif re.search(r"^http://www\.", website[0]):
        pass
    elif re.search(r"^http://", website[0]):
        pass
    elif re.search(r"^https://", website[0]):
        pass
    else:
        website[0] = f'https://www.{website[0]}'
rows_number = 2
for row in data:
    try:
        print(f'Currently checking this row[{rows_number}]: {row[0]}')
        res = req.get(row[0])
        content = res.content
        soup = BeautifulSoup(content, 'html.parser')
        tag_a = soup.find_all('a')
        for a in tag_a:
            if re.findall(regex_href, a['href']):
                print(a['href'])
                result = a['href']
                row[1] = f'{row[1]} | {result}'
        if row[1] != '':
            row[2] = 'Yes'
            row[3] = 'Yes'
        else:
            try:
                tag_header = soup.find_all('header')
                for phone in tag_header:
                    for match_header in re.findall(regex_phone, phone.text):
                        if len(match_header) > 8:
                            result = match_header.strip()
                            print(result)
                            row[1] = f'{row[1]} | {result}'
                if row[1] != '':
                    row[2] = 'Yes'
                    row[3] = 'Yes'
                else:
                    tag_span = soup.find_all('span')
                    for span in tag_span:
                        for match_span in re.findall(regex_phone, span.text):
                            if len(match_span) > 8:
                                result = match_span.strip()
                                print(result)
                                row[1] = f'{row[1]} | {result}'
                    if row[1] != '':
                        row[2] = 'Yes'
                        row[3] = 'Yes'
                    else:
                        row[2] = 'No'
                        row[3] = 'Yes'
            except AttributeError as e:
                print(e)
        rows_number += 1
    except Exception as e:
        print(e)
        rows_number += 1
df = pd.DataFrame(data, columns=['Websites', 'Phone', 'Suitable', 'Tool'])
df.to_excel('result.xlsx', index=False)
print(df.info())
print('\n')
print('If you can got any error or You want to update it then you can contact with Md. Minhaz by this PPH profile link.')
print('peopleperhour profile : https://pph.me/mdminhaz2003/')
print('Github Repository : https://github.com/mdminhaz2003/Website-Phone-Checker/')
print('Gmail : mdm047767@gmail.com')
print('Program Finished. You can check result.xlsx file for get result.')