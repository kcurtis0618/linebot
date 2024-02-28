from flask import Flask, request, abort
import json
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage
import openai

app = Flask(__name__)

# 環境變量中獲取 API 密鑰和 LINE 機器人的設定
API_KEY = os.getenv("OPENAI_API_KEY")
LINE_BOT_KEY = os.getenv("CHANNEL_TOKEN")
LINE_SECRET_KEY = os.getenv("CHANNEL_SECRET")

# 初始化 LINE Bot API 和 Handler
line_bot_api = LineBotApi(LINE_BOT_KEY)
handler = WebhookHandler(LINE_SECRET_KEY)

def GPT_response(text):
    client = openai.OpenAI()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
    )

    # 提取生成的文章標題和標籤
    generated_text = response.choices[0].message.content
    return generated_text

@app.route("/", methods=['POST'])
def linebot():
    # 獲取請求體和簽名
    body = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']
    # json_data = json.loads(body)
    # print(json_data)
    try:
        # 處理請求體
        events = handler.parser.parse(body, signature)

        for event in events:
            # 處理消息事件
            if event.type == 'message' and event.message.type == 'text':
                user_id = event.source.user_id
                received_msg = event.message.text
                # msg = json_data['events'][0]['message']['text'] + '.'
                # user = json_data["events"][0]["source"]["userId"]
                # 模擬的處理邏輯，這裡需要根據實際需求來填寫
                reply_msg = f"i got your msg：{received_msg}"
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_msg))
                print(f'{user_id}: {received_msg}')

    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        print(f"Exception: {e}")
        abort(500)

    return 'OK'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run()

