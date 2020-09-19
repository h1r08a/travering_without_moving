# j-wave travelling without movingでかけられた曲をスプレッドシートに保存
## (DataFrameは使用しない)

```
pip install requests
pip install beautifulsoup4
pip install gspread
```

1. [GCP](https://console.developers.google.com/)でプロジェクト作成
2. GoogleDriveAPIを有効にする
3. GoogleSheetsAPIを有効にする
4. 認証情報を設定する（サービスアカウントキー）
5. JSONをスクリプトと同じディレクトリに保存
6. 書き込むスプレッドシートに`client_email`を共有する
7. スクリプトのJSONファイル名とスプレッドシートキーを変更
8. スクリプト実行
