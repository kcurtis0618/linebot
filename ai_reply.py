import openai
# 打開檔案並讀取內容
with open('key.txt', 'r') as file:
    content = file.read()

# 找尋 "AI =" 後的字串
ai_index = content.find('AI =')
if ai_index != -1:
    # 取得 "AI =" 後面的字串
    ai_value = content[ai_index + 5:].strip()
else:
    print("找不到 'AI ='")

client = openai.OpenAI(api_key= ai_value)

def reply(t_input):
    # 使用OpenAI API生成文章標題和標籤
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": t_input}
        ]
    )

    # 提取生成的文章標題和標籤
    generated_text = response.choices[0].message.content
    return generated_text
