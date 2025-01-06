import sys, json, time
from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
)
from PySide6.QtCore import Qt
from qframelesswindow.utils import getSystemAccentColor
from qfluentwidgets import (
    setThemeColor,
    InfoBar,
    InfoBarPosition,
    IndeterminateProgressRing,
)

from PySide6.QtGui import QIcon
from httpgogui.layout.header import HeaderWidget
from httpgogui.layout.body import BodyWidget
from httpgogui.layout.bottom import BottomWidget
from httpgogui.components.table_widget import CommonTableWidget
from requests import request
from requests.exceptions import MissingSchema
from json.decoder import JSONDecodeError


class HttpgoWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        # 初始化 UI 和 信号
        self.ui = MainUI(self)
        self.signals = MainSignals(self.ui)
        self.signals.connect_signals()


class MainUI:

    def __init__(self, window: QMainWindow):
        super().__init__()
        self.window = window
        self.window.setWindowTitle("httpgo-gui")
        self.window.setWindowIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MailSend)))

        # 只能获取 Windows 和 macOS 的主题色
        if sys.platform in ["win32", "darwin"]:
            setThemeColor(getSystemAccentColor(), save=False)
        self.window.resize(1000, 800)
        # 创建中央窗口
        central_widget = QWidget()
        self.window.setCentralWidget(central_widget)
        # 创建主布局
        main_layout = QVBoxLayout()
        # 添加分区布局
        self.header_widget = HeaderWidget()
        main_layout.addWidget(self.header_widget)
        self.body_widget = BodyWidget()
        main_layout.addWidget(self.body_widget)
        self.bottom_widget = BottomWidget()
        main_layout.addWidget(self.bottom_widget)
        # main_layout.addStretch() # 添加弹性空间
        # 设置主布局到窗口
        central_widget.setLayout(main_layout)

        # loading
        self.spinner = IndeterminateProgressRing(self.window, False)
        # 获取窗口的宽度和高度
        window_width = self.window.width()
        window_height = self.window.height()
        # 获取进度环的宽度和高度
        spinner_width = self.spinner.width()
        spinner_height = self.spinner.height()

        # 计算偏移量，以使进度环居中
        offset_x = (window_width - spinner_width) // 2
        offset_y = (window_height - spinner_height) // 2

        # 设置进度环的位置，使其居中
        self.spinner.setGeometry(offset_x, offset_y, spinner_width, spinner_height)


class MainSignals:
    def __init__(self, ui: MainUI):
        self.ui = ui

    def connect_signals(self):
        """连接信号与槽"""
        self.ui.header_widget.send_button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):

        try:
            method = self.ui.header_widget.method_combo_box.currentText()
            url = self.ui.header_widget.url_line_text.text()
            body = self.ui.body_widget.body_widget.toPlainText()
            if body != "":
                body = json.loads(body)
        except JSONDecodeError:
            InfoBar.error(
                title="Error",
                content="无效的body参数",
                orient=Qt.Horizontal,  # 内容太长时可使用垂直布局
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
                duration=2000,
                # parent=self.ui.bottom_widget
                parent=self.ui.bottom_widget,
            )

        params = self.parse_key_value(self.ui.body_widget.params_widget)
        headers = self.parse_key_value(self.ui.body_widget.header_widget)
        cookies = self.parse_key_value(self.ui.body_widget.cookies_widget)

        try:
            # loading @TODO 使用QTherd多线程避免阻塞
            self.ui.spinner.start()
            response = request(
                method=method,
                url=url,
                json=body,
                headers=headers,
                params=params,
                cookies=cookies,
            )
        except MissingSchema:
            InfoBar.error(
                title="Error",
                content="无效的URL",
                orient=Qt.Horizontal,  # 内容太长时可使用垂直布局
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
                duration=2000,
                # parent=self.ui.bottom_widget
                parent=self.ui.bottom_widget,
            )
        # time.sleep(3)
        self.ui.spinner.stop()
        # 展示结果
        self.ui.bottom_widget.status_code_label.setText(
            f"status code: {response.status_code}"
        )
        self.ui.bottom_widget.result_edit.setText(
            json.dumps(response.json(), indent=4, ensure_ascii=False)
        )

    def parse_key_value(self, widget: CommonTableWidget):
        """解析参数"""
        key_value_dict = dict()
        for row in range(widget.rowCount()):
            temp_list = []
            for col in range(widget.columnCount()):
                line_widget = widget.cellWidget(row, col)  # 获取该单元格的lineEdit
                text = line_widget.text()  # 获取 QLineEdit 的文本内容
                if text:
                    temp_list.append(text)
            if temp_list:
                try:
                    key_value_dict[temp_list[0]] = temp_list[1]
                except IndexError:
                    InfoBar.error(
                        title="Error",
                        content="参数不正确",
                        orient=Qt.Horizontal,  # 内容太长时可使用垂直布局
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM,
                        duration=2000,
                        # parent=self.ui.bottom_widget
                        parent=self.ui.bottom_widget,
                    )
        return key_value_dict if key_value_dict else None


def main():
    app = QApplication([])
    window = HttpgoWidget()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
