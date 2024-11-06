import os

from lightrag import LightRAG, QueryParam
from lightrag.llm import gpt_4o_mini_complete, gpt_4o_complete

WORKING_DIR = "./medical"
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=gpt_4o_mini_complete,
    # llm_model_func=gpt_4o_complete
)

try:
    with open("./example.txt", "r", encoding="utf-8") as f:
        content = f.read()
        print("文件内容长度:", len(content))
        rag.insert(content)
except UnicodeDecodeError:
    print("UTF-8 编码失败,尝试其他编码...")
    try:
        with open("./example.txt", "r", encoding="latin-1") as f:
            content = f.read()
            print("文件内容长度:", len(content))
            rag.insert(content)
    except Exception as e:
        print("读取文件时发生错误:", str(e))
except Exception as e:
    print("发生其他错误:", str(e))

# Perform naive search
print(
    rag.query("Diagnostic standard procedures for pregnancy?", param=QueryParam(mode="naive"))
)

# # Perform local search
# print(
#     rag.query("What are the top themes in this story?", param=QueryParam(mode="local"))
# )

# # Perform global search
# print(
#     rag.query("What are the top themes in this story?", param=QueryParam(mode="global"))
# )

# Perform hybrid search
# print(
#     rag.query("What are the top themes in this story?", param=QueryParam(mode="hybrid"))
# )
