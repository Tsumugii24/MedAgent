import os
import subprocess

def process_pdf(input_file, output_dir):
    command = f"magic-pdf -p {input_file} --output-dir {output_dir}"
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"成功处理: {input_file}")
    except subprocess.CalledProcessError as e:
        print(f"处理失败: {input_file}. 错误: {str(e)}")

def batch_process_pdfs(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            input_path = os.path.join(input_folder, filename)
            process_pdf(input_path, output_folder)

if __name__ == "__main__":
    input_folder = input("请输入包含 PDF 文件的文件夹路径: ")
    output_folder = input("请输入输出文件夹路径: ")
    batch_process_pdfs(input_folder, output_folder)
    print("所有 PDF 文件处理完成!")
