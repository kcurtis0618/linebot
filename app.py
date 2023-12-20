
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
your_id = 'Udd9d677bacb9d89bb80323b5c1c9a46a'
#主動推播
line_bot_api.push_message(your_id, TextMessage(text='你可以開始了'))

#使用者回復狀態
user_state = {}


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)

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
    user_id = event.source.user_id
    message = event.message.text
    reply_message = []

    end_template_message = TemplateSendMessage(
        alt_text='問問題',
        template=ConfirmTemplate(
            text='是否繼續使用服務',
            actions=[
                MessageAction(label='是', text='繼續使用服務'),
                MessageAction(label='否', text='希望本次服務隊您有幫助！')
            ]
        )
    )

    if user_id not in user_state:
        user_state[user_id] = {"state": "Normal", "workflow": 0}

    if user_state[user_id]["state"] == "Normal":
        if re.match('嗨', message) or re.match('繼續使用本服務',message):
            button_template_message = TemplateSendMessage(
                alt_text='Start talk flow, multiselection button',
                template=ButtonsTemplate(
                    title='青少年就學就業職訓機器人',
                    text='請點選下方功能',
                    actions=[
                        PostbackAction(label='填寫會員資料', data='action=register_member'),
                        MessageAction(label='最新消息', text='多按鈕選擇樣板'),
                        URIAction(label='目前是ncnu im url', uri='https://www.im.ncnu.edu.tw/')
                    ]
                )
            )
            reply_message.append(button_template_message)
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
            reply_message.append(confirm_template_message)
            reply_message.append(end_template_message)
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
            reply_message.append(carousel_template_message)
            reply_message.append(end_template_message)
        # elif re.match('機器人對話',message):
        #     while message != '謝謝':
    elif user_state[user_id]["state"] == "Member":
        # 收集會員資料的對話流程
        if user_state[user_id]["workflow"] == 0 :
            line_bot_api.push_message(your_id, TextMessage(text='你的姓名是'))
            user_state[user_id]["workflow"] +=1

        elif user_state[user_id]["workflow"] == 1:
            line_bot_api.push_message(your_id, TextMessage(text='您的可用信箱是'))
            user_state[user_id]["workflow"] +=1

        else: #對話結束
            reply_message.append(TextMessage(text='感謝您的回覆~'))
            user_state[user_id]["state"] = "Normal" #將狀態調回正常狀態
            user_state[user_id]["workflow"] = 0
            reply_message.append(end_template_message)

    else:
        line_bot_api.reply_message(event.reply_token, TextMessage(text='不太理解你的意思喔～'))
        line_bot_api.push_message(your_id, end_template_message)
    if reply_message:
        print(reply_message)
        line_bot_api.reply_message(event.reply_token, reply_message)
#利用postback按鈕可以設計一些當按下按鈕後的動作
@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data
    reply_messages = []

    if user_id not in user_state:
        user_state[user_id] = {"state": "Normal", "workflow": 0}
        
    if data == 'action=register_member':
        user_state[user_id]["state"] = "Member"
        #確認是否要填寫確認會員資料
        confirm_template_message = TemplateSendMessage(
                alt_text='確認是否要填寫確認會員資料',
                template=ConfirmTemplate(
                    text='確認是否要填寫確認會員資料',
                    actions=[
                        MessageAction(
                            label='是',
                            text='開始填寫'
                        ),
                        PostbackAction(
                            label='不是',
                            display_text='取消填寫會員資料',
                            data='action = 後悔填寫'
                        )
                    ]
                )
            )
        reply_messages.append(confirm_template_message)
    
    elif data == 'action=後悔填寫':
        user_state[user_id]["state"] = "Normal"
        # reply_messages.append(end_template_message)

    if reply_messages:
        line_bot_api.reply_message(event.reply_token, reply_messages)


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
