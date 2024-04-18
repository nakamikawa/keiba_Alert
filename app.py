from flask import Flask, render_template, request
import pandas as pd
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

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
        print(f"エラーが発生しました: {e}")
        return pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def get_schedule():
    url = request.form.get('url')
    df = scrape_schedule(url)
    if not df.empty:
        html_table = df.to_html(index=False, classes='table table-striped')
    else:
        html_table = '<p>スケジュールが取得できませんでした。</p>'
    return render_template('schedule.html', table=html_table)

if __name__ == '__main__':
    app.run(debug=True)
