import logging
import time
import feedparser
import telebot
from Crypto.Hash import SHA256

chat_id = "#insert your chat id "
bot_token = "insert your bot token "
# Telegram botunu başlat
bot = telebot.TeleBot(bot_token)

# Takip etmek istediğiniz RSS beslemesinin URL'si
rss_feed_url = ['#insert your rss feeds']

# Tekrarlayan URL'leri kaldırmak için bir küme kullanın
unique_rss_feeds = set(rss_feed_url)

# Loglama konfigürasyonu
logging.basicConfig(
    filename='all.log',  # Tüm logları tek bir dosyada tutalım
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('rss_bot_logs')

info_handler = logging.FileHandler('info.log')
info_handler.setLevel(logging.INFO)
logger.addHandler(info_handler)

def my_function():
    logger.info('Fonksiyon çalışıyor...')


sent_news = set()

# Haberleri çekip gönderen fonksiyon


def get_and_send_news(chat_id):
    for url in unique_rss_feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.title
                link = entry.link

                # Haber kimliği oluşturma (örneğin, yayın tarihi ve başlık hash'i)
                # Hash the news item every time it's processed
                hashObject = SHA256.new()
                hashObject.update(f"{title}{link}".encode('utf-8'))  # Combine title and link for a more robust hash
                news_id = hashObject.hexdigest()

                if news_id not in sent_news:
                    sent_news.add(news_id)
                    # Haber gönderme işlemi
                    message = f"**{title}**\n\n{link}"
                    bot.send_message(chat_id, message, parse_mode='Markdown')
                    logger.info(f"Haber gönderildi: {title}")
                    time.sleep(60)  # Wait 60 seconds between messages (adjust as needed)
                else:
                    logger.info(f"Haber zaten gönderilmiş: {title}")

        except Exception as e:

            logger.error(f"RSS beslemesinde hata: {e}")
            # Hata durumunda bildirim gönderebilirsiniz


# Haberleri düzenli olarak kontrol etme
while True:
    try:
        get_and_send_news(chat_id)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
    time.sleep(1)  # 1 dakikada bir uykuya alır .

# Botu başlat
telebot.polling()


