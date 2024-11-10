import os
from flask import Flask, request, jsonify
from autogen import ConversableAgent, UserProxyAgent
import json
import requests
import base64
from openai import OpenAI

app = Flask(__name__)

# LLM配置
config_list = [
    {
        "model": "gpt-4o",
        "base_url": os.getenv("OPENAI_BASE_URL"),
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
]

SYSTEM_PROMPT = f"""
you are an experienced doctor.
"""

# 定义tool_use
def analyze_image(image_source):
    """分析图片内容并返回描述"""
    try:
        # 判断是否为URL
        if image_source.startswith(('http://', 'https://')):
            response = requests.get(image_source)
            base64_image = base64.b64encode(response.content).decode('utf-8')
        else:
            with open(image_source, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_BASE_URL')
        )
        
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
        
        return json.dumps({
            "action": "analyze_image", 
            "source": image_source,
            "result": response.choices[0].message.content
        })
        
    except Exception as e:
        return json.dumps({
            "action": "analyze_image",
            "source": image_source,
            "error": str(e)
        })

# 定义可用的函数
functions = [
    {
        "name": "analyze_image",
        "description": "分析图片内容并返回描述",
        "parameters": {
            "type": "object",
            "properties": {
                "image_source": {
                    "type": "string", 
                    "description": "图片的本地路径或URL地址"
                }
            },
            "required": ["image_source"]
        }
    }
]

# 定义医生agent
agent = ConversableAgent(
    name="doctor",
    system_message=SYSTEM_PROMPT,
    human_input_mode="NEVER",
    llm_config={
        "config_list": config_list,
        "timeout": 180,
        "temperature": 0.0,
        "functions": functions,
    }
)

# 创建agent字典
npc_agents = {
    "doctor": agent,
}

# 创建用户代理
user = UserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False}
)

# 用于存储对话历史的字典
conversation_history = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    npc_name = data.get('npc_name', 'doctor')

    if npc_name not in npc_agents:
        return jsonify({"error": "Invalid NPC name"}), 400

    current_agent = npc_agents[npc_name]

    # 初始化对话历史
    if session_id not in conversation_history:
        conversation_history[session_id] = {}
    if npc_name not in conversation_history[session_id]:
        conversation_history[session_id][npc_name] = []

    # 添加用户消息到对话历史
    conversation_history[session_id][npc_name].append({"role": "user", "content": user_message})

    # 重置agent和user的对话状态
    current_agent.reset_consecutive_auto_reply_counter(user)
    user.reset_consecutive_auto_reply_counter(current_agent)
    current_agent.reply_at_receive[user] = True

    try:
        # 构建消息历史，过滤掉null值
        messages = [
            {"role": "system", "content": current_agent.system_message}
        ] + [
            msg for msg in conversation_history[session_id][npc_name]
            if msg.get('content') is not None
        ]

        # 发送用户消息并获取回复
        reply = current_agent.generate_reply(messages=messages, sender=user)

        function_call = None
        function_result = None
        reply_content = ''

        if isinstance(reply, dict) and 'function_call' in reply:
            function_call = reply['function_call']
            function_name = function_call['name']
            arguments = json.loads(function_call['arguments'])
            
            # 执行函数调用
            if function_name == 'analyze_image':
                function_result = analyze_image(arguments['image_source'])
            else:
                function_result = json.dumps({"error": "未知的函数调用"})

            print(f"执行动作: {function_result}")
            
            # 将function_result解析为字典
            result_dict = json.loads(function_result)
            
            # 使用result字段作为content
            reply_content = result_dict.get('result', '执行了一个动作，但没有具体结果。')
            
        elif isinstance(reply, dict):
            reply_content = reply.get('content', '')
        else:
            reply_content = reply

        # 确保reply_content不为空
        if not reply_content:
            reply_content = "对不起，我现在无法回答。让我们换个话题吧。"

        # 添加agent的回复到对话历史
        conversation_history[session_id][npc_name].append({"role": "assistant", "content": reply_content})

        # 构建响应
        response = {
            'reply': reply_content,
            'function_call': function_call,
            'function_result': function_result
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error in chat function: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)