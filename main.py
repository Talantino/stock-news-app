import requests
from twilio.rest import Client

NEWS_API_KEY = "YOUR KEY"
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "YOUR KEY"

account_sid = "YOUR ACCOUNT SID"
auth_token = os.environ.get("AUTH_TOKEN")

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()

daily = data["Time Series (Daily)"]
data_list = [value for (key, value) in daily.items()]
yesterday_data = data_list[0]["4. close"]
two_days_ago = data_list[1]["4. close"]

difference = abs(float(yesterday_data) - float(two_days_ago))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
diff_percentage = (difference / float(yesterday_data)) * 100
print(diff_percentage)

if abs(diff_percentage) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percentage}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)
    client = Client(account_sid, auth_token)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="VIRTUAL_TWILIO_NUMBER",
            to="VERIFIED_NUMBER"
        )
