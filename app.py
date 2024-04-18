from flask import Flask, render_template, request
import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging

app = Flask(__name__)

# ログの設定
logging.basicConfig(filename='error.log', level=logging.ERROR)

def scrape_schedule(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', class_='hr-tableSchedule')
        rows = table.find_all('tr')

        schedule_data = []
        for row in rows[1:]:
            cells = row.find_all('td')
            if cells:
                time_text_elem = cells[0].find('p')
                if time_text_elem:
                    time_text = time_text_elem.text.strip()
                    r_text = cells[0].contents[0].strip()  # <p>要素以外のテキストを取得
                else:
                    time_text = None
                    r_text = cells[0].text.strip()

                race_name_elem = cells[1].find('span', class_='hr-tableSchedule__title')
                race_name = race_name_elem.text.strip() if race_name_elem else None

                content_elem = cells[1].find('span', class_='hr-tableSchedule__statusText')
                content = content_elem.text.strip() if content_elem else None

                if time_text and race_name and content:
                    schedule_data.append({'R': r_text, '発走時刻': time_text, 'レース名': race_name, '内容': content})

        return pd.DataFrame(schedule_data)

    except Exception as e:
        # エラーメッセージをログに出力
        logging.error(f"スクレイピング中にエラーが発生しました: {e}")
        # エラーメッセージを明示的に送出
        raise ValueError(f"スクレイピング中にエラーが発生しました: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])  # フォームの送信先を / に変更
def get_schedule():
    try:
        url = request.form.get('url')
        df = scrape_schedule(url)
        if not df.empty and 'エラー' not in df.columns:
            html_table = df.to_html(index=False, classes='table table-striped')
        else:
            error_message = df.iloc[0]['エラー'] if 'エラー' in df.columns else 'スケジュールが取得できませんでした。'
            html_table = f'<p>{error_message}</p>'
        return render_template('index.html', table=html_table)  # index.htmlにテーブルを表示
    except ValueError as ve:
        # ログに出力されたエラーメッセージを読み込み
        with open('error.log', 'r') as f:
            error_log = f.read()
        return render_template('index.html', error=str(ve), error_log=error_log)  # エラーメッセージとログを表示

if __name__ == '__main__':
    app.run(debug=True)
