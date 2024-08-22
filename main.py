import time

import feedparser
import telebot


chat_id = "#insert your chat id "
bot_token = "#insert your bot token "




# Takip etmek istediğiniz RSS beslemesinin URL'si
rss_feed_url = ['#insert your rss or atom feeds']
                


# Tekrarlayan URL'leri kaldırmak için bir küme kullanın
unique_rss_feeds = set(rss_feed_url)

# Telegram botunu başlat 
bot = telebot.TeleBot(bot_token)

#istek sınırlaması için


# Haberleri çekip gönderen fonksiyon
def get_and_send_news(chat_id):
    for url in unique_rss_feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.title
                link = entry.link


                message = f"**{title}**\n\n{link}"
                bot.send_message(chat_id, message, parse_mode='Markdown')
                time.sleep(2)  # Wait 2 seconds between messages (adjust as needed)
        except Exception as e:
            print(f"Error parsing {url}: {e}")



# Haberleri düzenli olarak kontrol etme
while True:
    get_and_send_news(chat_id)
    time.sleep(30)  # 30 dakikada bir uykuya alır .

# Botu başlat
telebot.polling()

