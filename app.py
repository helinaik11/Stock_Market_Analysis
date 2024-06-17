from flask import Flask, request, render_template, jsonify
import yfinance as yf
from datetime import timedelta, date
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    company = request.form['company']
    days = int(request.form['days'])

    present_day = date.today()
    final_date = present_day.strftime("%Y-%m-%d")
    day2 = present_day - timedelta(days=days)
    begin_date = day2.strftime("%Y-%m-%d")

    data = yf.download(company, start=begin_date, end=final_date, progress=False)
    data["Date"] = data.index

    fig = go.Figure(data=go.Candlestick(x=data["Date"], open=data["Open"], close=data["Close"], high=data["High"], low=data["Low"]))
    fig.update_layout(title="STOCK ANALYSIS")
    candlestick_html = fig.to_html(full_html=False)

    return jsonify(plots=[candlestick_html])

if __name__ == '__main__':
    app.run(debug=True)
