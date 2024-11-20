# 📊 Stockify Bot
<p align="center">
  <img src="https://github.com/user-attachments/assets/b5a4e306-16af-4caa-b504-a95f47bd1d74" alt="Stockify Bot Logo" width="100%">
</p>

**Stockify Bot** is a simple, powerful, and interactive Discord bot designed to help users stay updated with stock market trends and insights. It offers real-time stock prices, financial news, company information, and custom alerts. Built with Python, Stockify Bot integrates with multiple financial APIs to deliver accurate and timely data.

---

## 📜 Table of Contents

- Features
- Tech Stack
- Command List
- Setup and Usage
- Acknowledgments

---

## ✨ Features

- **Real-Time Stock Prices**: Fetch the latest stock prices using ticker symbols.
- **Financial News**: Retrieve the most recent news articles related to a company or stock.
- **Company Information**: Get details such as CEO, sector, industry, and description.
- **Top Performers**: View the top gainers and losers in the stock market.
- **Stock Price Alerts**: Set up price alerts and receive notifications directly on Discord.
- **Historical Data**: Access past stock prices for a specified period.
- **Stock Recommendations**: Get curated stock suggestions based on different sectors.
- **Currency Conversion**: Perform real-time currency exchange rate calculations.

---

## 🛠️ Tech Stack

- **Python**: The core programming language used to build the bot.
- **Discord.py**: Library for interacting with the Discord API.
- **Requests**: For making API calls to fetch stock, news, and financial data.
- **APIs Used**:
  - **Alpha Vantage**: Provides stock prices, historical data, and other financial metrics.
  - **NewsAPI**: Delivers financial news articles.
  - **IEX Cloud**: Supplies data for top gainers/losers.
  - **Finnhub**: Retrieves company information.
  - **Polygon.io**: Enhances company profile data.
  - **Exchange Rates API**: Performs live currency conversions.

---

## 🔧 Command List

| Command                          | Description                                                   |
|----------------------------------|---------------------------------------------------------------|
| `!help`                          | Displays the list of available commands.                     |
| `!getticker [COMPANY NAME]`      | Retrieves the ticker symbol for a given company.             |
| `!stock [TICKER]`                | Fetches the current stock price.                             |
| `!stocknews [TICKER]`            | Provides recent news articles for a stock.                   |
| `!companyinfo [TICKER]`          | Displays company information.                                |
| `!topgainers`                    | Shows the top-performing stocks.                             |
| `!toplosers`                     | Shows the worst-performing stocks.                           |
| `!volumetracker [TICKER]`        | Tracks the trading volume of a stock over a specified period.|
| `!stocksearch [QUERY]`           | Searches for stocks matching a query.                        |
| `!setalert [TICKER] [PRICE]`     | Sets a stock price alert.                                     |
| `!history [TICKER] [PERIOD]`     | Displays historical price data for a stock.                  |
| `!earnings [TICKER]`             | Fetches earnings report for a stock.                         |
| `!compare [TICKERS]`             | Compares the prices of multiple stocks.                      |
| `!recommend [CATEGORY]`          | Provides stock recommendations by sector.                    |
| `!exchange [FROM] [TO]`          | Converts currencies using live exchange rates.               |

---

## 🚀 Setup and Usage

1. **Clone the Repository**: Download the code to your local machine.
   ```bash
   git clone https://github.com/pranavkhot/Stockify.git
   
2. Install Dependencies:
   ```bash
   pip install discord requests
   
3. Configure API Keys:
- Replace placeholders like TOKEN, ALPHA_VANTAGE_API_KEY, NEWSAPI_KEY, etc., with your API keys in the script.
4. Run the Bot: Save the file as stockify_bot.py and execute it

    ```bash
     python stockify_bot.py
     
5. Invite the Bot to Your Server:
- Go to the Discord Developer Portal.
- Generate an OAuth2 URL under the "OAuth2" section with the bot scope and necessary permissions.
- Use the generated URL to invite the bot to your Discord server.

6. Test the Commands:
- Use !help in your server to view the list of available commands and test them.
---

## 🙏 Acknowledgments

- Discord.py Community: For comprehensive documentation and examples.
- Financial Data Providers: Alpha Vantage, NewsAPI, IEX Cloud, Finnhub, Polygon.io, and Exchange Rates API for their robust APIs.
- Open-Source Libraries: Python libraries like requests and discord.py made development seamless.
---

### Thank you for using Stockify Bot! 🎉
