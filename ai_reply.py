from openai import OpenAI# 打開檔案並讀取內容
with open('key.txt', 'r') as file:
    content = file.readline()
    
client = OpenAI(api_key=content)

def reply(t_input):
    print(content)
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
