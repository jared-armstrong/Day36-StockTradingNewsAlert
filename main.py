import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from newsapi import NewsApiClient


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = "882V5R7OS54F6BOP"
NEWS_API_KEY = "9d1ebc6c65994aa4b9c1facc9124d462"

STOCK_ENDPOINT = f"https://www.alphavantage.co/query?"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

TWILIO_SID = "AC750ca865640cda114b14b9466fa25b13"
TWILIO_AUTH_TOKEN = "8b8796715168de5164fc7b677798150a"
TWILIO_NUMBER = "+18889038705"

# Get yesterday's stock price

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

stock_response = requests.get(STOCK_ENDPOINT, stock_params)
stock_data = stock_response.json()['Time Series (Daily)']

data_list = [value for (key, value) in stock_data.items()]
print(data_list)

yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data['4. close'])
print(yesterday_closing_price)

# Get the day before yesterday's closing price

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']
print(day_before_yesterday_closing_price)

# Find positive difference between the prices

price_difference = yesterday_closing_price - day_before_yesterday_closing_price

# # Find percentage difference between closing price yesterday and closing price day before yesterday

diff_percent = round((price_difference / yesterday_closing_price) * 100)

# If percentage greater than 5, print news

if abs(diff_percent) > 3:
    newsApi = NewsApiClient(api_key=NEWS_API_KEY)
    all_articles = newsApi.get_everything(q='Tesla',
                                          from_param='2024-02-01',
                                          to='2024-02-06',
                                          sort_by='relevancy',
                                          language='en')
    articles = all_articles["articles"]

    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [f"{STOCK_NAME}: {diff_percent}\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=TWILIO_NUMBER,
            to="+12192997485"
        )
        print(message.body)

    print("Messages sent!")

