#sk-8712f85d2a524f79b772f1e27fba62f9
# 安装 OpenAI SDK：pip3 install openai

from openai import OpenAI
def ru(x):
    # 创建 API 客户端
    client = OpenAI(api_key="sk-8712f85d2a524f79b772f1e27fba62f9", base_url="https://api.deepseek.com")


    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": f"{x}"},
        ],
        stream=False
    )

    print(response.choices[0].message.content)

#distro