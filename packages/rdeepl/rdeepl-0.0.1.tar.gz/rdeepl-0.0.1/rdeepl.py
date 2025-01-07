import openai

def ru():
    # 创建 API 客户端
    openai.api_key = "sk-8712f85d2a524f79b772f1e27fba62f9"
    openai.api_base = "https://api.deepseek.com/beta"
    x = input("输入：")
    response = openai.Completion.create(
        model="deepseek-chat",
        prompt=f"System: You are a helpful assistant\nUser: {x}",
        stream=False
    )

    print(response.choices[0].text)
