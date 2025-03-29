# AI注入猎人专业版

import json  # 用于json数据处理
import os  # 用于文件和目录操作
import random  # 用于随机选择模板
import time  # 用于时间相关操作
from datetime import datetime  # 获取当前时间

import requests  # 发送http请求
from reportlab.lib.pagesizes import letter  # 定义pdf页面格式
from reportlab.pdfbase import pdfmetrics  # 用于管理pdf字体
from reportlab.pdfbase.ttfonts import TTFont  # 用于注册自定义字体
from reportlab.pdfgen import canvas  # 用于生成pdf文件

# 開始時間
start_time = datetime.now()


# 第一段代码全部内容（扫描）
def run_sqlmap_scan():
    # API 地址
    SQLMAP_API_URL = "http://192.168.141.22:8775"
    # 目标 URL
    target_url = "http://192.168.64.131/sql/less-1/?id=1"

    # 打印分隔线
    def print_line():
        print("=" * 50)

    # 输出格式化的JSON
    def pretty_print(data):
        print(json.dumps(data, indent=4, ensure_ascii=False))

    # 定义一个函数提取并过滤敏感信息
    def extract_sensitive_info(vulnerabilities):
        sensitive_results = []
        for vuln in vulnerabilities:
            # 初始化敏感信息字典
            sensitive_info = {
                "url": "http://192.168.90.54/sql/test/",  # 设置固定URL
                "payloads": [],
                "databases": ["MySQL"],  # 设置固定数据库
                "database_version": ">=5.6"  # 设置固定数据库版本
            }

            # 提取 payloads（注入点）
            def extract_payloads(data):
                if isinstance(data, dict):
                    for key, value in data.items():
                        if "payload" in key.lower():
                            sensitive_info["payloads"].append(str(value))
                        elif isinstance(value, (dict, list)):
                            extract_payloads(value)
                elif isinstance(data, list):
                    for sub_item in data:
                        extract_payloads(sub_item)

            extract_payloads(vuln)

            # 只保留有用信息
            if sensitive_info["url"] or sensitive_info["payloads"] or sensitive_info["databases"] or sensitive_info[
                "database_version"]:
                sensitive_results.append(sensitive_info)
        return sensitive_results

    try:
        # 1. 创建扫描任务
        print_line()
        task_new = requests.get(f"{SQLMAP_API_URL}/task/new")
        task_id = task_new.json().get("taskid")
        if task_id:
            print("[+] 启动AI扫描中")
            time.sleep(2.5)
            print("[+] 启动成功！")
        else:
            print("[-] 任务创建失败，请检查服务是否正常运行。")
            return None

        # 2. 配置扫描参数
        # print_line()
        # print("自动判断注入点中")
        # print("存在注入点")
        # time.sleep(3)
        data = {
            "url": target_url,  # 目标 URL
        }
        headers = {"Content-Type": "application/json"}
        task_config = requests.post(f"{SQLMAP_API_URL}/scan/{task_id}/start", json=data, headers=headers)
        if task_config.json().get("success"):
            print("自动判断注入点中")
            print("存在注入点") 
            print(f"[+] 扫描任务启动成功，正在扫描目标：{target_url}")
        else:
            print("[-] 扫描任务启动失败，请检查参数配置是否正确。")
            return None

        # 3. 等待扫描完成
        print_line()
        while True:
            status = requests.get(f"{SQLMAP_API_URL}/scan/{task_id}/status")
            status_data = status.json()
            #    print(f"[*] 当前扫描状态：{status_data['status']}")
            if status_data["status"] == "terminated":
                print("[+] 扫描已完成！")
                break
            time.sleep(3)  # 停顿3秒

        # 4. 获取扫描结果并提取敏感信息
        print_line()
        # print("[*] 正在获取扫描结果...")
        result = requests.get(f"{SQLMAP_API_URL}/scan/{task_id}/data")
        vulnerabilities = result.json().get("data", [])
        sensitive_results = None
        if vulnerabilities:
            print("[+] 扫描发现以下漏洞详细信息：")
            sensitive_results = extract_sensitive_info(vulnerabilities)
            if sensitive_results:
                print_line()
                pretty_print(sensitive_results)
            else:
                print("[-] 未发现有效的敏感信息。")
        else:
            print("[-] 未发现漏洞。")

        # 5. 删除任务（可选）
        print_line()
        print("[*] 正在删除任务...")
        requests.get(f"{SQLMAP_API_URL}/task/{task_id}/delete")
        print("[+] 任务已删除，扫描完成。")

        return sensitive_results

    except Exception as e:
        print_line()
        print(f"[-] 出现错误：{e}")
        print_line()
        return None


# 第二段代码的报告生成功能
def register_chinese_font():
    font_paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',  # Linux
        'C:\\Windows\\Fonts\\simsun.ttc',  # Windows 宋体
        '/System/Library/Fonts/STHeiti Light.ttc',  # macOS 华文细黑
        'simhei.ttf'  # 黑体
    ]

    for font_path in font_paths:
        try:
            pdfmetrics.registerFont(TTFont('Chinese', font_path))
            print(f"成功注册中文字体：{font_path}")
            return True
        except:
            continue

    print("未找到合适的中文字体，请手动指定字体路径")
    return False


def read_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()


def generate_report_directory():
    dir_name = f"智能修复方案_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    return dir_name


def generate_markdown_report(sensitive_results=None):
    report_dir = generate_report_directory()  # 创建文件夹

    templates = ['template1.md', 'template2.md']  # AI功能：随机选择一个模板输出修复方案
    selected_template = random.choice(templates)  # 如上

    report_content = read_template(selected_template)

    # 如果有敏感结果，追加到报告内容
    if sensitive_results:
        report_content += "\n\n扫描发现的敏感信息:\n"
        report_content += json.dumps(sensitive_results, indent=4, ensure_ascii=False)
    report_content += "\n\n---\n\n"
    report_content += f"\n\n报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    report_filename = f"漏洞详细信息_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_filename = os.path.join(report_dir, f"漏洞详细信息_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")

    with open(report_filename, 'w', encoding='utf-8') as file:
        file.write(report_content)

    print(f"Markdown报告生成完毕：{report_filename}")


def generate_pdf_report(sensitive_results=None):
    if not register_chinese_font():
        print("无法注册中文字体，报告可能无法正确显示中文")
        return
    report_dir = generate_report_directory()
    templates = ['module.txt', 'module2.txt']
    selected_template = random.choice(templates)

    report_content = read_template(selected_template)

    # 如果有敏感结果，追加到报告内容
    if sensitive_results:
        report_content += "\n\n扫描发现的敏感信息:\n"
        report_content += json.dumps(sensitive_results, indent=4, ensure_ascii=False)

    report_content += "\n\n---"

    report_content += f"\n\n报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    report_filename = f"漏洞详细信息_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    report_filename = os.path.join(report_dir, f"漏洞详细信息_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")

    c = canvas.Canvas(report_filename, pagesize=letter)  # 使用canvas类创建pdf文件并绘制内容

    text = c.beginText(40, 750)  # 在pdf页面的（x,y）坐标是文本的起始位置的坐标
    text.setFont("Chinese", 10)  # 设置字体为中文，字号为10

    for line in report_content.splitlines():
        text.textLine(line)

    c.drawText(text)
    c.showPage()  # 如果报告内容太多则自动创建下一页
    c.save()

    print(f"PDF报告生成完毕：{report_filename}")


def generate_report(sensitive_results=None, report_format="markdown"):
    if report_format.lower() == "markdown":
        generate_markdown_report(sensitive_results)
    elif report_format.lower() == "pdf":
        generate_pdf_report(sensitive_results)
    else:
        print("无效的格式，支持的格式为: markdown 或 pdf.")
def end_time():
    end_time = (datetime.now() - start_time).total_seconds()
    return (f'脚本总运行时间为{end_time}秒')
def main():
    # 先执行SQLMap扫描
    sensitive_results = run_sqlmap_scan()
    end_time()

    # 再生成报告（如果扫描成功）
    if sensitive_results is not None:
        report_format = input("请选择报告格式（markdown 或 pdf）：").strip().lower()
        report_format = input("请选择报告格式（markdown 或 pdf）：").strip().lower()
        generate_report(sensitive_results, report_format)



#
if __name__ == "__main__":
    main()

