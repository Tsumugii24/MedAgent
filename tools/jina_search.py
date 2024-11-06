import requests
import os
url = 'https://s.jina.ai/Diagnostic%20algorithm%20for%20pregnant%20women'
headers = {
    'Authorization': 'Bearer jina_284b019f5fdc4a05a23c5ee7a04b6ce3NNXx74hnL8LQVKuC745tjKYzJpnp',
    "X-With-Generated-Alt": "true"
}

response = requests.get(url, headers=headers)

if __name__ == "__main__":
    # 创建online文件夹（如果不存在）
    if not os.path.exists('./online'):
        os.makedirs('./online')
    if not os.path.exists('./online/search'):
        os.makedirs('./online/search')
    
    # 查找现有的文件并确定新的文件编号
    existing_files = [f for f in os.listdir('./online') if f.startswith('article_') and f.endswith('.md')]
    if existing_files:
        # 从现有文件名中提取编号，找到最大值
        numbers = [int(f.split('_')[1].split('.')[0]) for f in existing_files]
        next_number = max(numbers) + 1
    else:
        next_number = 1
    
    # 构建新的文件名
    output_path = f'./online/search/article_{next_number}.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    print(f'文件已保存至: {output_path}')