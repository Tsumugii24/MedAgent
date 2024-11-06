# pip install win32com
# pip install docx2pdf

import os
from docx2pdf import convert
import win32com.client

def convert_to_pdf(input_file, output_file):
    file_extension = os.path.splitext(input_file)[1].lower()
    
    if file_extension in ('.doc', '.docx'):
        convert(input_file, output_file)
    elif file_extension in ('.ppt', '.pptx'):
        try:
            powerpoint = win32com.client.Dispatch("Powerpoint.Application")
            deck = powerpoint.Presentations.Open(os.path.abspath(input_file))
            deck.SaveAs(os.path.abspath(output_file), 32)
            deck.Close()
        finally:
            powerpoint.Quit()

def batch_convert_to_pdf(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.doc', '.docx', '.ppt', '.pptx')):
            input_path = os.path.abspath(os.path.join(input_folder, filename))
            output_path = os.path.abspath(os.path.join(output_folder, os.path.splitext(filename)[0] + '.pdf'))
            print(f"正在转换: {filename}")
            try:
                convert_to_pdf(input_path, output_path)
                print(f"转换完成: {filename}")
            except Exception as e:
                print(f"转换失败: {filename}. 错误: {str(e)}")

if __name__ == "__main__":
    input_folder = "./test"
    output_folder = "./output"
    batch_convert_to_pdf(input_folder, output_folder)
    print("所有文件转换完成!")
