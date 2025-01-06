import sys
import os
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPoint, QProcess
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtWidgets import QWidget

class RoundedWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        brush = QBrush(QColor(46, 52, 64))  # 背景颜色
        painter.setBrush(brush)
        pen = QPen(Qt.NoPen)
        painter.setPen(pen)
        painter.drawRoundedRect(self.rect(), 10, 10)  # 圆角矩形，圆角半径为10

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口无边框和始终置顶
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置窗口标题
        self.setWindowTitle("我的工具")

        # 设置窗口大小（进一步缩小宽度和高度）
        self.setGeometry(100, 100, 200, 30)  # 宽度缩小为200，高度缩小为30

        # 设置扁平化主题
        self.setStyleSheet("""
            QMainWindow {
                background-color: transparent;
            }
            QToolBar {
                background-color: transparent;
                border: none;
                padding: 0px;
                spacing: 2px;
            }
            QToolButton {
                color: #ECEFF4;  /* 字体颜色为白色 */
                background-color: #4C566A;
                border: none;
                padding: 5px;
                margin: 0px;
                font-size: 12px;
                min-width: 25px;  /* 按钮最小宽度 */
                border-radius: 5px;  /* 圆角 */
            }
            QToolButton:hover {
                background-color: #5E81AC;  /* 鼠标悬停颜色 */
            }
            QToolButton:pressed {
                background-color: #81A1C1;  /* 鼠标按下颜色 */
            }
        """)

        # 创建工具栏
        toolbar = QToolBar("主工具栏")
        toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # 添加笔记按钮
        notes_action = QAction(QIcon(), "笔记", self)
        notes_action.triggered.connect(self.run_easynotes)
        toolbar.addAction(notes_action)

        # 添加任务按钮
        task_action = QAction(QIcon(), "任务", self)
        task_action.triggered.connect(self.run_task)
        toolbar.addAction(task_action)
        # 添加导图按钮
        mindmap_action = QAction(QIcon(), "导图", self)
        mindmap_action.triggered.connect(self.run_mind)
        toolbar.addAction(mindmap_action)


        # 添加截图按钮
        pdca_action = QAction(QIcon(), "截图", self)
        pdca_action.triggered.connect(self.run_pdca)
        toolbar.addAction(pdca_action)

        # 添加分隔符
        toolbar.addSeparator()

        # 添加关闭按钮（显示为X）
        close_action = QAction(QIcon(), '×', self)
        close_action.triggered.connect(self.close)
        toolbar.addAction(close_action)

        # 用于窗口拖动的变量
        self.dragging = False
        self.offset = QPoint()

        # 为每个任务创建一个独立的 QProcess 对象
        self.notes_process = QProcess(self)
        self.mind_process = QProcess(self)
        self.task_process = QProcess(self)
        self.pdca_process = QProcess(self)

        # 设置窗口启动位置为屏幕最上方偏右
        self.moveToTopRight()

        # 检查并初始化 setting.xml
        self.setting_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "setting.xml")
        self.work_dir = self.load_or_create_setting()

    def moveToTopRight(self):
        # 获取屏幕的几何信息
        screen_geometry = QApplication.desktop().screenGeometry()
        screen_width = screen_geometry.width()
        window_width = self.width()

        # 计算窗口的左上角坐标
        x = int(screen_width * 0.75) - window_width  # 右侧四分之三位置
        y = 0  # 紧贴屏幕顶部

        # 移动窗口
        self.move(x, y)

    def load_or_create_setting(self):
        """检查 setting.xml 是否存在，如果不存在则创建并选择工作目录"""
        if not os.path.exists(self.setting_file):
            # 弹出目录选择框
            work_dir = QFileDialog.getExistingDirectory(self, "选择工作目录", os.path.expanduser("~"))
            if not work_dir:
                QMessageBox.warning(self, "警告", "未选择工作目录，程序将退出！")
                sys.exit(1)

            # 创建 setting.xml 并保存工作目录
            root = ET.Element("settings")
            work_dir_element = ET.SubElement(root, "work_dir")
            work_dir_element.text = work_dir
            tree = ET.ElementTree(root)
            tree.write(self.setting_file, encoding="utf-8", xml_declaration=True)
            return work_dir
        else:
            # 读取 setting.xml 中的工作目录
            tree = ET.parse(self.setting_file)
            root = tree.getroot()
            work_dir = root.find("work_dir").text
            return work_dir

    def run_easynotes(self):
        if self.notes_process.state() == QProcess.Running:
            self.notes_process.terminate()
            self.notes_process.waitForFinished()
        self.notes_process.start("python", [os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__))), "notes.py")])

    def run_mind(self):
        if self.mind_process.state() == QProcess.Running:
            self.mind_process.terminate()
            self.mind_process.waitForFinished()
        self.mind_process.start("python",[os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__))), "mind.py")])

    def run_task(self):
        if self.task_process.state() == QProcess.Running:
            self.task_process.terminate()
            self.task_process.waitForFinished()
        self.task_process.start("python", [os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__))),"task.py")])

    def run_pdca(self):
        if self.pdca_process.state() == QProcess.Running:
            self.pdca_process.terminate()
            self.pdca_process.waitForFinished()
        self.pdca_process.start("python", [os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__))),"cut.py")])

    # 重写鼠标按下事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()

    # 重写鼠标移动事件
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    # 重写鼠标释放事件
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
