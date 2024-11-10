import requests

url = "http://localhost:5000/chat"
session_id = "patient"  # 可以是任何唯一标识符

def send_message(message, npc_name):
    data = {"message": message, "session_id": session_id, "npc_name": npc_name}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("病人提问:", message)
        print("医生回复:", response.json()['reply'])
        if 'function_call' in response.json():
            print("函数调用:", response.json()['function_call'])
        if 'function_result' in response.json():
            print("函数结果:", response.json()['function_result'])
        print("---")
    else:
        print("错误:", response.status_code, response.text)

# 测试对话
print("与doctor的对话:")
send_message("你好", "doctor")
send_message("你是谁", "doctor")
