
#載入LineBot所需要的套件
from flask import Flask, request, abort
import re
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
#引用其他檔案
# import ai_reply
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('MqnoFY4froFhOhpFxgpsL3YQTdqzrsd+glI6X6xIxfBk2rm1wGcFWDZR0srzIWZEzIe1AS21ZPzF4hNdJlFeSjkJkbuiUkdNnI/ojglmKVcSXPU1S8KAwvYdVdUjT10dJ/MHADeSqayJe8s83N1vXQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('d6fff126b59d024cfd2daf367fc6db6f')

#主動推播
line_bot_api.push_message('Udd9d677bacb9d89bb80323b5c1c9a46a', TextMessage(text='你可以開始了'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

 
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('嗨',message):
        # 發送按鈕訊息寫在TemplateSendMessage()
        buttom_template_message = TemplateSendMessage(
            alt_text = 'Start talk flow, multiselection buttom',# 註記這個按鈕的功能簡介
            template = ButtonsTemplate(
                title = '青少年就學就業職訓機器人',# 按鈕上方大標題
                text = '請點選下方功能', # 下方些微內文
                actions = [
                    # 回傳用按鈕，可以在action的地方加入自己需要用的參數
                    PostbackAction(
                        label = '填寫會員資料',
                        display_text = '確認按鈕',
                        data = 'action=感謝你的填寫'
                    ),
                    # 回覆文字
                    MessageAction(
                        label = '最新消息',
                        text = '多按鈕選擇樣板'
                    ),
                    # 連結
                    URIAction(
                        label = '目前是ncnu im url',
                        uri = 'https://www.im.ncnu.edu.tw/'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttom_template_message)
    elif re.match('確認按鈕',message):
        confirm_template_message = TemplateSendMessage(
            alt_text='問問題',
            template=ConfirmTemplate(
                text='你喜這堂課嗎？',
                actions=[
                    PostbackAction(
                        label='喜歡',
                        display_text='超喜歡',
                        data='action=其實不喜歡'
                    ),
                    MessageAction(
                        label='愛',
                        text='愛愛❤'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, confirm_template_message)
    elif re.match('多按鈕選擇樣板',message):
        carousel_template_message = TemplateSendMessage(
            alt_text='免費教學影片',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/KLpBBsV.jpg',
                        title='Python基礎教學',
                        text='萬丈高樓平地起',
                        actions=[
                            MessageAction(
                                label='教學內容',
                                text='拆解步驟詳細介紹安裝並使用Anaconda、Python、Spyder、VScode…'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://marketingliveincode.com/?page_id=270'
                            ),
                            PostbackAction(
                                label = '輸入個人資料',
                                display_text = '感謝你的填寫',
                                data = 'action=還沒有東西'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/W7nI6fg.jpg',
                        title='Line Bot聊天機器人',
                        text='台灣最廣泛使用的通訊軟體',
                        actions=[
                            MessageAction(
                                label='教學內容',
                                text='Line Bot申請與串接'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://marketingliveincode.com/?page_id=2532'
                            ),
                            PostbackAction(
                                label = '輸入個人資料',
                                display_text = '感謝你的填寫',
                                data = 'action=還沒有東西'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/NDfQ43S.jpg',
                        title='青年第一讚',
                        text='用主題探索青年資源',
                        actions=[
                            MessageAction(
                                label='功用簡介',
                                text='點選按鈕查看資源'
                            ),
                            URIAction(
                                label='詳細內容',
                                uri='https://youthfirst.yda.gov.tw/'
                            ),
                            PostbackAction(
                                label = '輸入個人資料',
                                display_text = '感謝你的填寫',
                                data = 'action=還沒有東西'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
