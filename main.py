import requests
# import newsapi
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_PRICE_ACCESS_KEY = "6CY7YMHPCKO3JU5S"
NEWS_ACCESS_KEY = "72fcc49d530c457f8ea18b2851affe05"

stock_price_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_PRICE_ACCESS_KEY,
}

news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_ACCESS_KEY,
}

account_sid = "AC7673838147a32dec9453c2b1ad8c3779"
auth_token = "b50da18f8e5b58abc3c3a27ec5216c8b"

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
response = requests.get(url="https://www.alphavantage.co/query", params=stock_price_parameters)
data = response.json()["Time Series (Daily)"]
# print(data)
close_values = [values["4. close"] for key, values in data.items()]
check = close_values[:2]
diff = float(check[0]) - float(check[1])
percent = (diff / float(check[0])) * 100
if abs(percent) > 0:
    # STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    response = requests.get(url="https://newsapi.org/v2/top-headlines", params=news_parameters)
    data = response.json()["articles"][:3]
    top_news = {news["title"]: news["description"] for news in data}

    # STEP 3: Use https://www.twilio.com
    # Send a separate message with the percentage change and each article's title and description to your phone number.
    client = Client(account_sid, auth_token)
    if diff < 0:
        symbol = "🔻"
    else:
        symbol = "🔺"

    for title, description in top_news.items():
        message = client.messages.create(
            body=f"{STOCK}: {symbol}{round(percent)}%\n"
                 f"Headline: {title}\n"
                 f"Brief: {description}",
            from_="+19094871753",
            to='+919066569822'
        )

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.
"""
