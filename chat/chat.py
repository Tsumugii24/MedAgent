import os
from flask import Flask, request, jsonify
from autogen import ConversableAgent, UserProxyAgent
import json

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
you are a helpful assistant.
"""

# 定义tool_use
def find_path(x, y):
    return json.dumps({"action": "find_path", "position": [x, y], "result": "成功找到通往({},{})的路径".format(x, y)})

def chop_tree(x, y):
    return json.dumps({"action": "chop_tree", "position": [x, y], "result": "在({},{})砍倒了一棵树".format(x, y)})

def plow_land(x, y):
    return json.dumps({"action": "plow_land", "position": [x, y], "result": "在({},{})耕地完成".format(x, y)})

def cut_grass(x, y):
    return json.dumps({"action": "cut_grass", "position": [x, y], "result": "在({},{})割掉了杂草".format(x, y)})

def water_plant(x, y):
    return json.dumps({"action": "water_plant", "position": [x, y], "result": "在({},{})给植物浇了水".format(x, y)})

def plant_seed(x, y, seed_type):
    return json.dumps({"action": "plant_seed", "position": [x, y], "seed_type": seed_type, "result": "在({},{})种下了{}".format(x, y, seed_type)})

def harvest(x, y):
    return json.dumps({"action": "harvest", "position": [x, y], "result": "在({},{})收获了作物".format(x, y)})

def build_furniture(x, y, furniture_type):
    return json.dumps({"action": "build_furniture", "position": [x, y], "type": furniture_type, "result": "在({},{})建造了{}".format(x, y, furniture_type)})

def do_nothing(x, y):
    return json.dumps({"action": "do_nothing", "position": [x, y], "result": "在({},{})无所事事地度过了一段时间".format(x, y)})

def sleep(x, y):
    return json.dumps({"action": "sleep", "position": [x, y], "result": "在({},{})睡了一觉".format(x, y)})

def plan_daily_schedule():
    return json.dumps({
        "action": "plan_daily_schedule",
        "schedule": [
            {"time": "morning", "activity": "", "function": None},
            {"time": "noon", "activity": "", "function": None},
            {"time": "afternoon", "activity": "", "function": None},
            {"time": "evening", "activity": "", "function": None}
        ]
    })

# 定义可用的函数
functions = [
    {
        "name": "find_path",
        "description": "寻找到指定位置的路径",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "目标位置的X坐标"},
                "y": {"type": "integer", "description": "目标位置的Y坐标"}
            },
            "required": ["x", "y"]
        }
    },
    {
        "name": "chop_tree",
        "description": "在指定位置砍树",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "砍树位置的X坐标"},
                "y": {"type": "integer", "description": "砍树位置的Y坐标"}
            },
            "required": ["x", "y"]
        }
    },
    {
        "name": "plow_land",
        "description": "在指定位置耕地",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "耕地位置的X坐标"},
                "y": {"type": "integer", "description": "耕地位置的Y坐标"}
            },
            "required": ["x", "y"]
        }
    },
    {
        "name": "cut_grass",
        "description": "在指定位置割草",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "割草位置的X坐标"},
                "y": {"type": "integer", "description": "割草位置的Y坐标"}
            },
            "required": ["x", "y"]
        }
    },
    {
        "name": "water_plant",
        "description": "在指定位置给植物浇水",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "浇水位置的X坐标"},
                "y": {"type": "integer", "description": "浇水位置的Y坐标"}
            },
            "required": ["x", "y"]
        }
    },
    {
        "name": "plant_seed",
        "description": "在指定位置播种",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "播种位置的X坐标"},
                "y": {"type": "integer", "description": "播种位置的Y坐标"},
                "seed_type": {"type": "string", "description": "种子类型"}
            },
            "required": ["x", "y", "seed_type"]
        }
    },
    {
        "name": "harvest",
        "description": "在指定位置收获作物",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "收获位置的X坐标"},
                "y": {"type": "integer", "description": "收获位置的Y坐标"}
            },
            "required": ["x", "y"]
        }
    },
    {
        "name": "build_furniture",
        "description": "在指定位置建造家具",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "建造位置的X坐标"},
                "y": {"type": "integer", "description": "建造位置的Y坐标"},
                "furniture_type": {"type": "string", "description": "家具类型"}
            },
            "required": ["x", "y", "furniture_type"]
        }
    },
    {
        "name": "do_nothing",
        "description": "在指定位置无所事事",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "X坐标"},
                "y": {"type": "integer", "description": "Y坐标"}
            },
            "required": ["x", "y"]
        }
    },
    {
        "name": "sleep",
        "description": "在指定位置睡觉",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "X坐标"},
                "y": {"type": "integer", "description": "Y坐标"}
            },
            "required": ["x", "y"]
        }
    },
    {
        "name": "plan_daily_schedule",
        "description": "规划一天的行程,包括morning, noon, afternoon, evening四个时间段及其对应的活动",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]

# 创建村长爷爷NPC
agent = ConversableAgent(
    name="village_elder",
    system_message=SYSTEM_PROMPT,
    human_input_mode="NEVER",
    llm_config={
        "config_list": config_list,
        "timeout": 180,
        "temperature": 0.0,
        "functions": functions,
    }
)

# 创建NPC字典
npc_agents = {
    "village_elder": agent,
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
    npc_name = data.get('npc_name', 'village_elder')

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
            if function_name == 'find_path':
                function_result = find_path(arguments['x'], arguments['y'])
            elif function_name == 'chop_tree':
                function_result = chop_tree(arguments['x'], arguments['y'])
            elif function_name == 'plow_land':
                function_result = plow_land(arguments['x'], arguments['y'])
            elif function_name == 'cut_grass':
                function_result = cut_grass(arguments['x'], arguments['y'])
            elif function_name == 'water_plant':
                function_result = water_plant(arguments['x'], arguments['y'])
            elif function_name == 'plant_seed':
                function_result = plant_seed(arguments['x'], arguments['y'], arguments['seed_type'])
            elif function_name == 'harvest':
                function_result = harvest(arguments['x'], arguments['y'])
            elif function_name == 'build_furniture':
                function_result = build_furniture(arguments['x'], arguments['y'], arguments['furniture_type'])
            elif function_name == 'do_nothing':
                function_result = do_nothing(arguments['x'], arguments['y'])
            elif function_name == 'sleep':
                function_result = sleep(arguments['x'], arguments['y'])
            elif function_name == 'plan_daily_schedule':
                function_result = plan_daily_schedule()
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