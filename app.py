from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # スクレイピングして取得したテキストを抽出
        text = soup.get_text()
        return text
    except Exception as e:
        return f"エラーが発生しました: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_text', methods=['POST'])
def get_text():
    url = request.form.get('url')
    scraped_text = scrape_text(url)
    return render_template('result.html', text=scraped_text)

if __name__ == '__main__':
    app.run(debug=True)
