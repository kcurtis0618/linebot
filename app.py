
#載入LineBot所需要的套件
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#############################
import openai 
import re
import os
#############################
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

# OPENAI API Key初始化設定
openai.api_key = os.getenv('OPENAI_API_KEY')

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
    reply_message = []#統一用來裝欲回覆的訊息
    
    #使用者狀態
    if user_id not in user_state:
        user_state[user_id] = {"state": "Normal", "workflow": 0}
    
    #初始按鈕
    if user_state[user_id]["state"] == "Normal":
        if re.match('嗨', message) or re.match('繼續使用服務',message):
            button_template_message = TemplateSendMessage(
                alt_text='Start talk flow, multiselection button',
                template=ButtonsTemplate(
                    title='青少年就學就業職訓機器人',
                    text='請點選下方功能',
                    actions=[
                        PostbackAction(label='填寫會員資料', data='action=register_member'),
                        MessageAction(label='最新消息', text='獲得最新消息'),
                        PostbackAction(label='我想與機器人對話', data='action=robot'),
                    ]
                )
            )
            reply_message.append(button_template_message)


        #最新消息
        elif re.match('獲得最新消息',message):
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

    elif user_state[user_id]["state"] == "Robot":
        if re.match('謝謝',message):
            user_state[user_id]["state"] = "Normal" #將狀態調回正常狀態
            reply_message.append(TextMessage(text = '感謝您的使用，希望這些對您有幫助～'))
            reply_message.append(end_template_message)
        else:
            reply_text = GPT_response(message)
            if reply_text.strip():  # 檢查回文是否為空
                line_bot_api.reply_message(event.reply_token, TextMessage(text=reply_text))
            else:
                # 處理空回文的情況，例如記錄錯誤、發送預設消息等
                print("Received an empty response from GPT-3.")
    #填寫會員資料
    elif user_state[user_id]["state"] == "Member":
        # 收集會員資料的對話流程
        if user_state[user_id]["workflow"] == 0 :
            reply_message.append(TextMessage(text='你的姓名是'))
            user_state[user_id]["workflow"] +=1

        elif user_state[user_id]["workflow"] == 1:
            reply_message.append(TextMessage(text='您的可用信箱是'))
            user_state[user_id]["workflow"] +=1

        else: #對話結束
            reply_message.append(TextMessage(text='感謝您的回覆~'))
            user_state[user_id]["state"] = "Normal" #將狀態調回正常狀態
            user_state[user_id]["workflow"] = 0
            reply_message.append(end_template_message)



    #最後輸出
    if reply_message:
        line_bot_api.reply_message(event.reply_token, reply_message)

#利用postback按鈕可以設計一些當按下按鈕後的動作
@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data
    reply_message = []

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
                        MessageAction(label='是',text='開始填寫'),
                        PostbackAction(label='不是',display_text='取消填寫會員資料',data='action = 後悔填寫')
                    ]
                )
            )
        reply_message.append(confirm_template_message)
    
    elif data == 'action=robot':
        user_state[user_id]["state"] = "Robot"
        reply_message.append(TextMessage(text="歡迎使用青少年服務ai機器人～\n有什麼任何問題都可以進行訊問!\n\n若要結束使用請輸入「謝謝」\n就可以中斷對談了～"))


    elif data == 'action=後悔填寫':
        user_state[user_id]["state"] = "Normal"
        reply_message.append(end_template_message)#在對話結束之後要加上是否繼續使用服務的按鈕

    
    if reply_message:
        line_bot_api.reply_message(event.reply_token, reply_message)


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
