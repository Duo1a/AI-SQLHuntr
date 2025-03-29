from PyQt5.QtGui import QIcon
import sys
import threading
from datetime import datetime
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QVBoxLayout, QWidget, QTextEdit, QComboBox,
                             QLabel, QHBoxLayout, QLineEdit)
from PyQt5.QtGui import QIcon
import sys
import ctypes
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

import webprofessional  # 引入后端模块



class OutputRedirector(QObject):
    outputWritten = pyqtSignal(str)  # 将后端的输出显示在GUI上


class SQLMapScannerApp(QMainWindow):  # 主窗口应用程序
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon("1.ico")) 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('AI-Sql Hunter')

    def initUI(self):
        self.setWindowTitle('AI注入猎人云端版')  # 设置窗口标题
        self.setGeometry(100, 100, 800, 600)  # 设置窗口的位置和尺寸
        central_widget = QWidget()  # 创建中央控件，是整个窗口的容器
        main_layout = QVBoxLayout()  # 创建垂直布局，中央控件的布局
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.setWindowIcon(QIcon('D:\\professional\\1.ico'))

        control_layout = QHBoxLayout()  # 创建控制面板
        format_label = QLabel('报告格式:')  # 创建标签控件
        self.format_combo = QComboBox()  # 创建下拉框，并添加两个选项：pdf和markdown
        self.format_combo.addItems(['Markdown', 'PDF'])
        control_layout.addWidget(format_label)
        control_layout.addWidget(self.format_combo)

        self.url_input = QLineEdit()  # 创建URL输入框
        self.url_input.setPlaceholderText("请输入URL")
        control_layout.addWidget(QLabel('目标URL:'))
        control_layout.addWidget(self.url_input)

        self.scan_button = QPushButton('启动AI扫描')  # 创建按钮
        self.scan_button.clicked.connect(self.run_sqlmap_scan)
        control_layout.addWidget(self.scan_button)  # 当按钮被点击时，调用run_sqlmap_scan

        main_layout.addLayout(control_layout)  # 将控制面板添加到主布局

        self.output_text = QTextEdit()  # 创建文本编辑框，用于显示输出
        self.output_text.setReadOnly(True)  # 设置文本框为只读，以便只能查看输出，不能编辑
        main_layout.addWidget(self.output_text)

        self.output_redirector = OutputRedirector()  # 将控制台输出重定向到GUI
        self.output_redirector.outputWritten.connect(self.append_output)

    def run_sqlmap_scan(self):
        url = self.url_input.text().strip()  # 获取用户输入的URL并去除空白字符

        # 检查URL输入是否为空
        if not url:
            self.output_redirector.outputWritten.emit("错误：请输入URL。")
            return  # 如果URL为空，则不执行扫描

        self.scan_button.setEnabled(False)  # 禁用扫描按钮
        self.url_input.setReadOnly(True)  # 设置URL输入框为只读，防止修改
        self.output_text.clear()  # 清空输出文本框

        class StreamToQt:  # 通过信号系统将输出的文本发送给GUI
            def __init__(self, signal):
                self.signal = signal

            def write(self, text):
                self.signal.outputWritten.emit(text)

            def flush(self):
                pass

        sys.stdout = StreamToQt(self.output_redirector)
        sys.stderr = sys.stdout

        def run_scan():  # 运行扫描，生成报告
            report_format = self.format_combo.currentText().lower()
            start_scan_time = datetime.now()  # 记录扫描开始时间
            # 调用后端模块执行扫描，假设不需要实际传入URL
            sensitive_results = webprofessional.run_sqlmap_scan()
            end_scan_time = datetime.now()  # 记录扫描结束时间
            # 调用后端模块生成报告，假设不需要实际传入结果
            webprofessional.generate_report(sensitive_results, report_format)
            elapsed_time = (end_scan_time - start_scan_time).total_seconds()  # 计算运行时间
            formatted_time = f"{elapsed_time:.2f}"  # 格式化为保留两位小数
            self.output_redirector.outputWritten.emit(f'脚本总运行时间为{formatted_time}秒')

            # 扫描完成后恢复按钮和输入框状态
            self.scan_button.setEnabled(True)
            self.url_input.setReadOnly(False)

        threading.Thread(target=run_scan, daemon=True).start()  # 启动新线程

    def append_output(self, text):
        self.output_text.append(text)  # 将接收到的文本追加到输出文本框中


def main():  # 初始化主窗口，并启动事件循环
    app = QApplication(sys.argv)
    scanner_app = SQLMapScannerApp()
    scanner_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":  # 如果脚本直接运行，调用main()启动程序
    main()