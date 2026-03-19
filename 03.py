from zhipuai import ZhipuAI

client = ZhipuAI(api_key="your-api-key")  # 请填写您自己的 API Key

response = client.chat.completions.create(
    model="glm-5",
    messages=[
        {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的口号"},
        {"role": "assistant", "content": "当然，要创作一个吸引人的口号，请告诉我一些关于您产品的信息"},
        {"role": "user", "content": "智谱AI开放平台"}
    ],
    thinking={
        "type": "enabled",
    },
    max_tokens=65536,
    temperature=1.0
)

# 获取完整回复
print(response.choices[0].message)