import requests
import json
import argparse
import os
import sys
import time
import signal

# DeepSeek API 配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # 替换为实际的 DeepSeek API URL

# 全局变量用于统计
start_time = time.time()
translated_chars = 0

def signal_handler(sig, frame):
    """捕获 Ctrl+C 信号并输出统计信息"""
    elapsed_time = time.time() - start_time
    print(f"\n\nTranslation interrupted!")
    print(f"Translated characters: {translated_chars}")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    sys.exit(0)

def translate_text_batch(text_batch, target_lang="zh", api_key=None):
    """调用 DeepSeek 大模型 API 批量翻译文本"""
    if not api_key:
        raise ValueError("API key is required. Please provide it via --apikey or set the DEEPSEEK_API_KEY environment variable.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    # 构造提示词（prompt）要求模型翻译文本
    messages = [
        {"role": "system", "content": "你是一个专业的翻译。"},  # 设置 system 角色
        {"role": "user", "content": f"将以下内容翻译成{target_lang}，保持格式不变：\n\n{text_batch}"}
    ]
    data = {
        "model": "deepseek-chat",  # 使用 deepseek-chat 模型
        "messages": messages,
        "max_tokens": 4000,  # 每次翻译的最大 token 数
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        translated_text = response.json()["choices"][0]["message"]["content"]
        return translated_text.strip()
    else:
        raise Exception(f"Translation failed: {response.status_code}, {response.text}")

def parse_subtitle_file(file_path):
    """解析字幕文件，返回时间轴和内容的列表"""
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        buffer = []
        for line in lines:
            if line.strip() == "":
                if buffer:
                    subtitles.append(buffer)
                    buffer = []
            else:
                buffer.append(line.strip())
        if buffer:  # 处理最后一个块
            subtitles.append(buffer)
    return subtitles

def format_subtitle_batch(subtitles):
    """将字幕列表格式化为批量翻译的文本"""
    batch = []
    for subtitle in subtitles:
        if len(subtitle) >= 2:  # 确保有时间轴和文本
            batch.append("\n".join(subtitle))
    return "\n\n".join(batch)

def translate_file(input_file, output_file, target_lang="zh", api_key=None, batch_size=10):
    """翻译文件内容"""
    global translated_chars

    # 解析源文件
    subtitles = parse_subtitle_file(input_file)
    total_subtitles = len(subtitles)
    translated_subtitles = 0

    # 如果目标文件存在，读取已翻译的内容
    if os.path.exists(output_file):
        translated_subtitles = len(parse_subtitle_file(output_file))

    with open(output_file, 'a', encoding='utf-8') as f_out:  # 以追加模式打开文件
        # 按批次翻译
        for i in range(translated_subtitles, total_subtitles, batch_size):
            batch = subtitles[i:i + batch_size]
            text_batch = format_subtitle_batch(batch)
            translated_batch = translate_text_batch(text_batch, target_lang, api_key)

            # 将翻译结果写入文件
            f_out.write(translated_batch + "\n\n")
            f_out.flush()  # 刷新缓冲区，确保内容立即写入文件

            # 打印翻译结果到终端
            print(translated_batch)
            translated_chars += len(translated_batch)

            # 更新进度
            translated_subtitles += len(batch)
            print_progress(translated_subtitles, total_subtitles)

def print_progress(current, total):
    """在终端显示任务进度"""
    progress = (current / total) * 100
    sys.stdout.write(f"\rProgress: {progress:.2f}% ({current}/{total} subtitles)")
    sys.stdout.flush()

def main():
    global start_time

    # 设置命令行参数
    parser = argparse.ArgumentParser(description="Translate subtitle files (ASS/SRT) using DeepSeek API.")
    parser.add_argument("input_file", help="Path to the input subtitle file (ASS or SRT).")
    parser.add_argument("-o", "--output_file", help="Path to the output subtitle file.", default=None)
    parser.add_argument("-l", "--target_lang", help="Target language for translation (default: zh).", default="zh")
    parser.add_argument("--apikey", help="DeepSeek API key. If not provided, the DEEPSEEK_API_KEY environment variable will be used.", default=None)
    parser.add_argument("-b", "--batch_size", type=int, help="Number of subtitles per batch (default: 10).", default=10)
    args = parser.parse_args()

    # 如果未指定输出文件，则自动生成
    if args.output_file is None:
        input_name, input_ext = os.path.splitext(args.input_file)
        args.output_file = f"{input_name}.{args.target_lang}{input_ext}"

    # 优先使用命令行参数中的 API 密钥，否则使用环境变量
    api_key = args.apikey or os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("Please provide the API key via --apikey or set the DEEPSEEK_API_KEY environment variable.")

    # 注册信号处理函数
    signal.signal(signal.SIGINT, signal_handler)

    # 记录开始时间
    start_time = time.time()

    # 调用翻译函数
    translate_file(args.input_file, args.output_file, args.target_lang, api_key, args.batch_size)

    # 翻译完成后输出统计信息
    elapsed_time = time.time() - start_time
    print(f"\n\nTranslation complete!")
    print(f"Translated characters: {translated_chars}")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print(f"Output file: {args.output_file}")

if __name__ == "__main__":
    main()