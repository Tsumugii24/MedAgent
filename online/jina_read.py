import requests
import os

url = 'https://r.jina.ai/https://mp.weixin.qq.com/s/CLz1tF9OGSz4stia2Rx4tA'
headers = {
    'X-With-Generated-Alt': 'true',
    'X-With-Images-Summary': 'true',
    'X-With-Links-Summary': 'true'
}

response = requests.get(url, headers=headers)

if __name__ == "__main__":
    # 创建online文件夹（如果不存在）
    if not os.path.exists('./online'):
        os.makedirs('./online')
    if not os.path.exists('./online/read'):
        os.makedirs('./online/read')
    
    # 查找现有的文件并确定新的文件编号
    existing_files = [f for f in os.listdir('./online') if f.startswith('article_') and f.endswith('.md')]
    if existing_files:
        # 从现有文件名中提取编号，找到最大值
        numbers = [int(f.split('_')[1].split('.')[0]) for f in existing_files]
        next_number = max(numbers) + 1
    else:
        next_number = 1
    
    # 构建新的文件名
    output_path = f'./online/read/article_{next_number}.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    print(f'文件已保存至: {output_path}')