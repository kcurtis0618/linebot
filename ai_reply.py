import openai

# 在程序启动时读取并设置 API 密钥
with open('key.txt', 'r') as file:
    openai.api_key = file.read().strip()

def reply(t_input):
    try:
        # 使用OpenAI API生成文章標題和標籤
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": t_input}
            ]
        )

        # 提取生成的回复
        generated_text = response['choices'][0]['message']['content']
        return generated_text
    except openai.error.OpenAIError as e:
        # 处理OpenAI错误
        print(f"OpenAI error: {e}")
    except Exception as e:
        # 处理其他可能的错误
        print(f"An error occurred: {e}")
