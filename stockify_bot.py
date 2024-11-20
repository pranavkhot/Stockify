import discord
from discord import Embed
from discord.ext import commands, tasks
import requests
import matplotlib.pyplot as plt
from io import BytesIO

TOKEN = 'KEY'
ALPHA_VANTAGE_API_KEY = 'KEY'
ALPHA_VANTAGE_ENDPOINT = "https://www.alphavantage.co/query"
NEWSAPI_ENDPOINT = "https://newsapi.org/v2/everything"
NEWSAPI_KEY = "KEY"
IEX_ENDPOINT = "https://cloud.iexapis.com/stable/stock/market"
IEX_TOKEN = "KEY"
FINNHUB_ENDPOINT = "https://finnhub.io/api/v1/stock/profile2"
FINNHUB_API_KEY = "KEY"
POLYGON_ENDPOINT = "https://api.polygon.io/v1/meta"
POLYGON_API_KEY = "KEY"
EXCHANGE_RATES_API_KEY = 'KEY'
EXCHANGE_RATES_API_ENDPOINT = "https://open.er-api.com/v6/latest"


intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Command List
@bot.command(name="help", aliases=["commands"])
async def _help(ctx):
    embed = Embed(title="Stock Bot Commands", description="Here are the available commands:", color=0x3498db)
    
    # Add commands to the embed
    command_list = [
        ("🔍 !getticker [COMPANY NAME]", "Retrieve the ticker for a given company name."),
        ("💹 !stock [TICKER]", "Get the current stock price."),
        ("📰 !stocknews [TICKER]", "Retrieve recent news articles for a stock."),
        ("🏢 !companyinfo [TICKER]", "Get information about a company."),
        ("📈 !topgainers", "See the top gaining stocks."),
        ("📉 !toplosers", "See the top losing stocks."),
        ("🔊 !volumetracker [TICKER]", "Track the volume of a stock."),
        ("🔍 !stocksearch [QUERY]", "Search for a stock."),
        ("🚨 !setalert [TICKER] [PRICE] [DIRECTION]", "Set a price alert for a stock."),
        ("📅 !history [TICKER] [PERIOD]", "Retrieve historical data for a stock."),
        ("💰 !earnings [TICKER]", "Get earnings report for a stock."),
        ("🔗 !compare [TICKERS]", "Compare multiple stocks."),
        ("🌟 !recommend [CATEGORY]", "Get stock recommendations for a category."),
        ("💱 !exchange [FROM_CURRENCY] [TO_CURRENCY]", "Get currency exchange rate.")
    ]
    
    for command, description in command_list:
        embed.add_field(name=command, value=description, inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
async def stock(ctx, ticker: str):
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": ticker,
        "interval": "1min",
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    response = requests.get(ALPHA_VANTAGE_ENDPOINT, params=params).json()

    # Check if the expected key exists in the response
    if 'Time Series (1min)' in response:
        latest_time = list(response['Time Series (1min)'].keys())[0]
        price = response['Time Series (1min)'][latest_time]['1. open']
        await ctx.send(f"💰 Current price of {ticker.upper()} is ${price}")
    else:
        # If the key is not present, check for an error message in the response
        error_msg = response.get('Note') or response.get('Error Message') or "⚠️ Error fetching data for the stock. Please try again later."
        await ctx.send(error_msg)

    
@bot.command()
async def getticker(ctx, query: str):
    ALPHA_VANTAGE_SEARCH_ENDPOINT = "https://www.alphavantage.co/query"
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": query,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    response = requests.get(ALPHA_VANTAGE_SEARCH_ENDPOINT, params=params).json()

    if 'bestMatches' in response and len(response['bestMatches']) > 0:
        matches = response['bestMatches']
        message = "🔍 **Found Stocks**:\n"
        for match in matches:
            symbol = match['1. symbol']
            name = match['2. name']
            message += f"- {name} ({symbol})\n"
        await ctx.send(message)
    else:
        await ctx.send(f"❌ No stocks found matching '{query}'.")


@bot.command()
async def stocknews(ctx, ticker: str, number_of_articles: int = 3):
    params = {
        "q": ticker,
        "apiKey": NEWSAPI_KEY,
        "pageSize": number_of_articles,
        "language": "en"
    }

    response = requests.get(NEWSAPI_ENDPOINT, params=params).json()

    if response['status'] == "ok" and response['totalResults'] > 0:
        for article in response['articles']:
            title = article['title']
            url = article['url']
            description = article['description']
            await ctx.send(f"📰 **{title}**\n{description}\n[Read more]({url})")
    else:
        await ctx.send(f"❌ No recent news articles found for {ticker.upper()}.")

@bot.command()
async def companyinfo(ctx, ticker: str):
    url = f"{POLYGON_ENDPOINT}/symbols/{ticker}/company?apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        await ctx.send(f"❌ Error fetching data for {ticker}. Please try again later.")
        return

    data = response.json()
    company_name = data['name']
    ceo = data['ceo']
    sector = data['sector']
    industry = data['industry']
    website = data['url']
    description = data['description']

    message = f"🏢 **Company Information for {ticker.upper()} - {company_name}**\n"
    message += f"👤 CEO: {ceo}\n"
    message += f"📊 Sector: {sector}\n"
    message += f"🏭 Industry: {industry}\n"
    message += f"🌐 Website: {website}\n"
    message += f"📝 Description: {description}"

    await ctx.send(message)

@bot.command()
async def topgainers(ctx, number_of_stocks: int = 5):
    url = f"{IEX_ENDPOINT}/list/gainers?token={IEX_TOKEN}&listLimit={number_of_stocks}"
    response = requests.get(url).json()

    if response:
        message = "📈 **Top Gainers**:\n"
        for stock in response:
            symbol = stock['symbol']
            change = stock['changePercent']
            message += f"{symbol}: +{change*100:.2f}%\n"
        await ctx.send(message)
    else:
        await ctx.send("❌ Unable to fetch top gainers at the moment.")

@bot.command()
async def toplosers(ctx, number_of_stocks: int = 5):
    url = f"{IEX_ENDPOINT}/list/losers?token={IEX_TOKEN}&listLimit={number_of_stocks}"
    response = requests.get(url).json()

    if response:
        message = "📉 **Top Losers**:\n"
        for stock in response:
            symbol = stock['symbol']
            change = stock['changePercent']
            message += f"{symbol}: {change*100:.2f}%\n"
        await ctx.send(message)
    else:
        await ctx.send("❌ Unable to fetch top losers at the moment.")

        
@bot.command()
async def volumetracker(ctx, ticker: str, days: int = 10):
    # Ensure days is between 1 and 100 (Alpha Vantage limitation for daily data)
    days = min(max(days, 1), 100)
    
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    response = requests.get(ALPHA_VANTAGE_ENDPOINT, params=params).json()

    # Extract daily data
    daily_data = response.get("Time Series (Daily)", {})

    # If we don't have sufficient data, notify the user
    if len(daily_data) < days:
        await ctx.send(f"Not enough data for {ticker.upper()}. Try reducing the number of days or choose another stock.")
        return

    # Extract volumes for the given period
    volumes = [int(data["5. volume"]) for _, data in list(daily_data.items())[:days]]

    # Calculate average volume
    average_volume = sum(volumes) / days
    current_volume = volumes[0]

    # Compare current volume to average volume
    if current_volume > average_volume:
        comparison = f"The current volume of {ticker.upper()} is 📈 **higher** than its {days}-day average."
    else:
        comparison = f"The current volume of {ticker.upper()} is 📉 **lower** than its {days}-day average."

    await ctx.send(comparison + f"\n🔊 Current Volume: **{current_volume:,}**\n📅 {days}-Day Average Volume: **{average_volume:,.0f}**")


@bot.command()
async def stocksearch(ctx, query: str):
    ALPHA_VANTAGE_SEARCH_ENDPOINT = "https://www.alphavantage.co/query"
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": query,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    response = requests.get(ALPHA_VANTAGE_SEARCH_ENDPOINT, params=params).json()

    if 'bestMatches' in response and len(response['bestMatches']) > 0:
        matches = response['bestMatches']
        message = "🔍 **Stock Search Results**:\n"
        for match in matches:
            symbol = match['1. symbol']
            name = match['2. name']
            message += f"- {symbol}: {name}\n"
        await ctx.send(message)
    else:
        await ctx.send(f"❌ No stocks found matching '{query}'.")


# In-memory storage for alerts
alerts = []

@bot.event
async def on_ready():
    print(f'🟢 We have logged in as {bot.user}')
    check_stock_prices.start()


@bot.command()
async def setalert(ctx, ticker: str, target_price: float, direction: str):
    if direction not in ["above", "below"]:
        await ctx.send("Direction should be either 'above' or 'below'")
        return
    
    alert = {
        "user_id": ctx.author.id,
        "ticker": ticker.upper(),
        "target_price": target_price,
        "direction": direction
    }
    alerts.append(alert)
    await ctx.send(f"⏰ Alert set for {ticker.upper()} {direction} ${target_price}")

@tasks.loop(minutes=10)
async def check_stock_prices():
    for alert in alerts.copy():
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": alert['ticker'],
            "interval": "1min",
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        response = requests.get(ALPHA_VANTAGE_ENDPOINT, params=params).json()
        latest_time = list(response['Time Series (1min)'].keys())[0]
        current_price = float(response['Time Series (1min)'][latest_time]['1. open'])
        
        user = bot.get_user(alert['user_id'])

        if alert['direction'] == "above" and current_price >= alert['target_price']:
            await user.send(f"📈 {alert['ticker']} has reached ${current_price}, above your target of ${alert['target_price']}!")
            alerts.remove(alert)
        elif alert['direction'] == "below" and current_price <= alert['target_price']:
            await user.send(f"📉 {alert['ticker']} has dropped to ${current_price}, below your target of ${alert['target_price']}!")
            alerts.remove(alert)


@bot.command()
async def history(ctx, ticker: str, period: str):
    # Define the number of data points (days) based on the period
    if period == "1month":
        data_points = 30
    elif period == "6months":
        data_points = 180
    elif period == "1year":
        data_points = 365
    else:
        await ctx.send("🚫 Invalid period. Please use 1month, 6months, or 1year.")
        return

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY,
        "outputsize": "full"  # Retrieve full-length daily historical data
    }

    response = requests.get(ALPHA_VANTAGE_ENDPOINT, params=params).json()
    
    if "Time Series (Daily)" in response:
        data = list(response["Time Series (Daily)"].items())[:data_points]
        dates = [entry[0] for entry in data]
        prices = [float(entry[1]['4. close']) for entry in data]
        message = f"📅 **Historical Data for {ticker.upper()} over {period}**:\n"
        for date, price in zip(dates, prices):
            message += f"{date}: ${price}\n"
        await ctx.send(message)
    else:
        await ctx.send(f"❌ Error fetching historical data for {ticker}. Please try again later.")


@bot.command()
async def earnings(ctx, ticker: str):
    params = {
        "function": "EARNINGS",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    response = requests.get(ALPHA_VANTAGE_ENDPOINT, params=params).json()

    if "annualEarnings" in response:
        # For simplicity, we'll just fetch the most recent annual earnings
        recent_earnings = response["annualEarnings"][0]
        fiscal_date_ending = recent_earnings['fiscalDateEnding']
        reported_EPS = recent_earnings['reportedEPS']

        message = f"💰 **Earnings Report for {ticker.upper()}**:\n"
        message += f"Fiscal Date Ending: {fiscal_date_ending}\n"
        message += f"Reported EPS: ${reported_EPS}\n"
        await ctx.send(message)
    else:
        await ctx.send(f"❌ Error fetching earnings report for {ticker}. Please try again later.")


@bot.command()
async def compare(ctx, *tickers: str):
    if not tickers or len(tickers) < 2:
        await ctx.send("❗ Please provide at least two stock tickers for comparison.")
        return

    prices = {}
    for ticker in tickers:
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": ticker,
            "interval": "1min",
            "apikey": ALPHA_VANTAGE_API_KEY
        }

        response = requests.get(ALPHA_VANTAGE_ENDPOINT, params=params).json()
        if "Time Series (1min)" in response:
            latest_time = list(response['Time Series (1min)'].keys())[0]
            price = response['Time Series (1min)'][latest_time]['1. open']
            prices[ticker] = price
        else:
            await ctx.send(f"❌ Error fetching data for {ticker}. Please try again later.")
            return

    # Once we have all prices, format and send the message
    message = "📊 **Stock Price Comparison**:\n"
    for ticker, price in prices.items():
        message += f"{ticker.upper()}: ${price}\n"
    
    await ctx.send(message)

def get_recommendations(category):
    # Expanded mock data for demonstration purposes
    recommendations = {
        "tech": [
            {"symbol": "AAPL", "rationale": "Strong performance in wearables."},
            {"symbol": "MSFT", "rationale": "Cloud segment growth."},
            {"symbol": "GOOGL", "rationale": "Continued dominance in search."},
            {"symbol": "AMZN", "rationale": "E-commerce leadership."},
            {"symbol": "FB", "rationale": "Growth in ad revenue."}
        ],
        "health": [
            {"symbol": "JNJ", "rationale": "New drug pipeline."},
            {"symbol": "PFE", "rationale": "Success of vaccine distribution."},
            {"symbol": "MRK", "rationale": "Diverse drug portfolio."},
            {"symbol": "ABT", "rationale": "Innovative medical devices."},
            {"symbol": "GILD", "rationale": "Strong antiviral segment."}
        ],
        "finance": [
            {"symbol": "JPM", "rationale": "Stable financial performance."},
            {"symbol": "BAC", "rationale": "Expanding digital services."},
            {"symbol": "WFC", "rationale": "Recovery post-controversies."},
            {"symbol": "C", "rationale": "International banking growth."},
            {"symbol": "GS", "rationale": "Strong investment banking segment."}
        ]
    }
    
    return recommendations.get(category, [])

@bot.command()
async def recommend(ctx, category: str):
    stocks = get_recommendations(category)
    if stocks:
        message = f"🌟 **Recommended stocks for {category.capitalize()} sector**:\n\n"
        for stock in stocks:
            message += f"**{stock['symbol']}**: {stock['rationale']}\n\n"
        await ctx.send(message)
    else:
        await ctx.send(f"❌ No recommendations available for {category}.")


@bot.command()
async def exchange(ctx, from_currency: str, to_currency: str):
    url = f"{EXCHANGE_RATES_API_ENDPOINT}/{from_currency}"
    response = requests.get(url)

    if response.status_code != 200:
        await ctx.send("❌ Error fetching exchange rate. Please try again later.")
        return

    data = response.json()
    if to_currency not in data['rates']:
        await ctx.send(f"🚫 Currency {to_currency} not supported or incorrect.")
        return

    exchange_rate = data['rates'][to_currency]
    await ctx.send(f"💱 1 {from_currency.upper()} is equal to {exchange_rate} {to_currency.upper()}.")


bot.run(TOKEN)
