import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

api_key_stock = "RZE20PDKW1MGPQAZ"
api_key_news = "7a46e6c854f740d2a095a712442711a5"

account_sid = 'ACcb0b5f19a28185b73ebc4bcff45d4212'
auth_token = 'd080d2dfb66f6cb8c02f44fcf36c2c5b'

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": api_key_stock,
}

response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]
yesterday_closing = stock_data_list[0]['4. close']

day_before_yesterday_closing = stock_data_list[1]['4. close']
closing_positive_difference = float(yesterday_closing) - float(day_before_yesterday_closing)

up_down = None
if closing_positive_difference > 5:
    up_down = "🔼"
else:
    up_down = "🔽"

percent_diff = (abs(closing_positive_difference) / float(yesterday_closing)) * 100

if abs(percent_diff) > .3:
    news_parameters = {
        "q": COMPANY_NAME,
        "apiKey": api_key_news,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()['articles']
    news_data_list = news_data[:3]
    for each_news in news_data_list:
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"\n\n{COMPANY_NAME}: {up_down}{round(percent_diff, 2)}% \n\nHeadline:{each_news['title']} ({COMPANY_NAME})?.\n\n Brief: {each_news['description']}",
            from_='+17163255844',
            to='7033509383'
        )