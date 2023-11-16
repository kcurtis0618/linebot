from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 設定 Channel Access Token 與 Channel Secret
line_bot_api = LineBotApi('MqnoFY4froFhOhpFxgpsL3YQTdqzrsd+glI6X6xIxfBk2rm1wGcFWDZR0srzIWZEzIe1AS21ZPzF4hNdJlFeSjkJkbuiUkdNnI/ojglmKVcSXPU1S8KAwvYdVdUjT10dJ/MHADeSqayJe8s83N1vXQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d6fff126b59d024cfd2daf367fc6db6f')

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 LINE 請求頭的資料
    signature = request.headers['X-Line-Signature']

    # 取得請求的內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        # 驗證簽章
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 收到文字訊息時的處理邏輯
    user_message = event.message.text
    reply_message = f'你說了：{user_message}'
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

if __name__ == "__main__":
    app.run(port=5000)
