import openai
import os
import base64

def encode_image_to_base64(image_path):
    """将本地图片转换为base64格式"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"读取图片失败: {e}")
        return None

# 获取图片的base64编码
image_path = "./local/妊娠期糖尿病2022指南/auto/images/06de36540a0fcecd97b6a0603067b6f313c05f5e538214019b133632f04673fa.jpg"
base64_image = encode_image_to_base64(image_path)

# 修改API调用部分
client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'], base_url=os.environ['OPENAI_BASE_URL'])
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's the content of this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    max_tokens=300,
)

content = response.choices[0].message.content
print(content)

