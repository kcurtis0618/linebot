import openai
client = openai.OpenAI(api_key='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')

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