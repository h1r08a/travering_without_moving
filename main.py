import requests
from bs4 import BeautifulSoup
import gspread
import json

#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = ''

#共有設定したスプレッドシートのシート1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

page_url = "https://www.j-wave.co.jp/original/travelling/backnumber/"
res = requests.get(page_url)
soup = BeautifulSoup(res.content, features="html.parser")

links = soup.find_all('a')
no_use = ('index.html', "message/", "getop", "ps://www.j-wave.co.jp/")
ln = []
for link in links:
    tmp = link.get('href')[3:]
    if tmp in no_use:
        continue
    ln.append("https://www.j-wave.co.jp/original/travelling/{}".format(tmp))

count = 0
song_list = []
artist_list = []
for l in ln:
    res = requests.get(l)
    soup = BeautifulSoup(res.content, features="html.parser")
    elms = soup.find_all("h3", {'class': "ms_song"})
    for elm in elms:
            song = elm.string.split(' / ')
            if len(song) == 2:
                artist_list.append(song[1])
                song_list.append(song[0])
                count = count + 1

# song
# 編集する範囲を指定、A1セルから、リストの要素数をカウントしたものを指定する
cell_list = worksheet.range('A2:A'+str(len(artist_list)+1))

#cell_listにtest_listの値を流し込む
for i,cell in enumerate(cell_list):
    cell.value = song_list[i]

#最後にupdate_cellsで流し込む
worksheet.update_cells(cell_list)

# artist
# 編集する範囲を指定、A1セルから、リストの要素数をカウントしたものを指定する
cell_list = worksheet.range('B2:B'+str(len(artist_list)+1))

#cell_listにtest_listの値を流し込む
for i,cell in enumerate(cell_list):
    cell.value = artist_list[i]

#最後にupdate_cellsで流し込む
worksheet.update_cells(cell_list)

print("合計{}件 保存完了".format(len(artist_list)))