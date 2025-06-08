import pytest
import os
import shutil
import argparse
import logging
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def parse_args():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description='App UI自动化测试执行工具')
    parser.add_argument('--cases', default='test/', help='测试用例路径，支持特定文件或目录')
    parser.add_argument('--markers', help='运行指定标记的用例，如：smoke, regression')
    parser.add_argument('--reruns', type=int, default=0, help='失败用例重试次数')
    parser.add_argument('--clean', action='store_true', help='是否清理历史报告和日志')
    return parser.parse_args()

def setup_logging():
    """
    配置日志记录
    """
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f'run_{timestamp}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def clean_dirs():
    """
    清理历史文件和目录
    """
    dirs_to_clean = [
        "reports",
        "screenshots",
        "logs",
        ".pytest_cache",
        "**/__pycache__"
    ]
    
    for dir_pattern in dirs_to_clean:
        try:
            if '*' in dir_pattern:
                # 处理通配符模式
                import glob
                for dir_path in glob.glob(dir_pattern, recursive=True):
                    if os.path.exists(dir_path):
                        shutil.rmtree(dir_path)
                        logging.info(f"已清理目录: {dir_path}")
            else:
                # 处理具体目录
                if os.path.exists(dir_pattern):
                    shutil.rmtree(dir_pattern)
                    logging.info(f"已清理目录: {dir_pattern}")
        except Exception as e:
            logging.warning(f"清理目录 {dir_pattern} 失败: {str(e)}")

def create_dirs():
    """
    创建必要的目录
    """
    dirs_to_create = [
        "logs",
        "screenshots",
        "reports/allure-results",
        "reports/allure-report"
    ]
    
    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)
        logging.info(f"已创建目录: {dir_path}")

def run_tests(args):
    """
    运行测试用例
    """
    pytest_args = [
        args.cases,
        '-v',
        '--alluredir=reports/allure-results',
        '--clean-alluredir'
    ]
    
    if args.markers:
        pytest_args.append(f"-m {args.markers}")
    
    if args.reruns > 0:
        pytest_args.extend(['--reruns', str(args.reruns)])
    
    logging.info(f"开始执行测试，参数: {' '.join(pytest_args)}")
    return pytest.main(pytest_args)

def zip_dir(dir_path, zip_path):
    """
    将指定目录打包为zip文件
    """
    import zipfile
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, dir_path)
                zipf.write(abs_path, rel_path)
    logging.info(f"已打包Allure报告为: {zip_path}")

# def send_report_via_email(report_html_path, report_zip_path, to_emails, custom_body=None):
#     """
#     將Allure報告發送到指定郵箱，支持多收件人、zip和index.html雙附件，正文含本地預覽指引。
#     :param report_html_path: Allure報告index.html路徑
#     :param report_zip_path: Allure報告zip包路徑
#     :param to_emails: 收件人郵箱，str或list
#     :param custom_body: 自定義郵件正文
#     """
#     from_email = "wuemily55@gmail.com"  # 請替換為你的發件郵箱
#     from_pass = "qwtp oxws vvjn hrmv"   # 請替換為你的郵箱授權碼或密碼
#     smtp_server = "smtp.gmail.com"
#     subject = "自動化測試Allure報告"
#
#     if isinstance(to_emails, str):
#         to_emails = [e.strip() for e in to_emails.split(",") if e.strip()]
#
#     # 郵件正文
#     body = custom_body or (
#         "本次自動化測試Allure報告已生成，詳見附件。\n\n"
#         "【本地預覽指引】\n"
#         "1. 解壓附件zip包\n"
#         "2. 安裝Allure命令行工具（如未安裝）\n"
#         "3. 命令行進入解壓目錄，執行：allure open .\n"
#         "4. 或直接打開index.html（部分瀏覽器可能無法正確顯示，推薦用allure open命令）\n\n"
#         "如有疑問請聯繫自動化負責人。"
#     )
#     msg = MIMEMultipart()
#     msg["Subject"] = subject
#     msg["From"] = from_email
#     msg["To"] = ", ".join(to_emails)
#     msg.attach(MIMEText(body, "plain", "utf-8"))
#
#     # 添加index.html附件
#     if os.path.exists(report_html_path):
#         with open(report_html_path, "rb") as f:
#             part = MIMEApplication(f.read(), Name="allure-report.html")
#             part["Content-Disposition"] = 'attachment; filename="allure-report.html"'
#             msg.attach(part)
#     # 添加zip附件
#     if os.path.exists(report_zip_path):
#         with open(report_zip_path, "rb") as f:
#             part = MIMEApplication(f.read(), Name="allure-report.zip")
#             part["Content-Disposition"] = 'attachment; filename="allure-report.zip"'
#             msg.attach(part)
#
#     try:
#         with smtplib.SMTP_SSL(smtp_server, 465) as server:
#             server.login(from_email, from_pass)
#             server.sendmail(from_email, to_emails, msg.as_string())
#         logging.info(f"Allure報告已發送到郵箱: {to_emails}")
#     except Exception as e:
#         logging.error(f"郵件發送失敗: {e}")

def zip_allure_report(report_dir, zip_path):
    """將Allure報告目錄打包為zip"""
    import zipfile
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(report_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, report_dir)
                zipf.write(abs_path, arcname=rel_path)
    logging.info(f"Allure報告已打包為: {zip_path}")

def generate_report():
    """
    生成Allure报告并打包zip，發送郵件，报告名为英文+年月日
    """
    try:
        today = datetime.now().strftime("%Y%m%d")
        report_dir = f"reports/allure-report-{today}"
        report_zip = f"reports/allure-report-{today}.zip"
        os.system(f"allure generate reports/allure-results -o {report_dir} --clean")
        logging.info(f"已生成Allure报告: {report_dir}")
        report_html = os.path.join(report_dir, "index.html")
        if os.path.exists(report_dir):
            zip_allure_report(report_dir, report_zip)
        if os.path.exists(report_html):
            logging.info(f"测试报告已生成: {os.path.abspath(report_html)}")
            # send_report_via_email(report_html, report_zip, "wuemily55@gmail.com")
    except Exception as e:
        logging.error(f"生成报告失败: {str(e)}")

if __name__ == "__main__":
    # 解析命令行参数
    args = parse_args()
    
    # 设置日志
    setup_logging()
    
    try:
        # 清理目录（如果需要）
        if args.clean:
            clean_dirs()
        
        # 创建必要的目录
        create_dirs()
        
        # 运行测试
        exit_code = run_tests(args)
        
        # 生成报告
        generate_report()
        
        # 退出
        exit(exit_code)
    except Exception as e:
        logging.error(f"执行测试过程中发生错误: {str(e)}")
        generate_report()
        exit(1)