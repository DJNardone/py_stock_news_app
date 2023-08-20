import requests
from twilio.rest import Client
import os

account_sid = 'AC09c30700ea699e92c03658dc4aba3894'
auth_token = os.environ.get("AUTH_TOKEN")
to_number = os.environ.get("TO_NUMBER")
from_number = os.environ.get("FROM_NUMBER")

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_api_key = os.environ.get("STOCK_API_KEY")
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key
}

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_api_key = os.environ.get("NEWS_API_KEY")
news_parameters = {
    "q": "TSLA",
    "sortBy": "relevancy",
    "searchIn": "title,description",
    "pageSize": 3,
    "apiKey": news_api_key
}

stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()['Time Series (Daily)']
stock_data_list = [value for (key, value) in stock_data.items()]

recent_close_price = float(stock_data_list[0]['4. close'])
prior_close_price = float(stock_data_list[1]['4. close'])
price_diff = (recent_close_price - prior_close_price)
up_down = None
if price_diff > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"
percent_diff = round(abs(price_diff / recent_close_price) * 100)

if abs(percent_diff) >= 0:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()['articles']
    news_titles = [news_data[i]["title"] for i in range(0, 3)]

    format_message = f"{COMPANY_NAME} {up_down} {percent_diff}% Today\n" \
                     f"Headlines:\n🔸 {news_titles[0]}\n🔸 {news_titles[1]}\n🔸 {news_titles[2]}"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_=from_number,
        body=format_message,
        to=to_number
    )

    print(message.status)


