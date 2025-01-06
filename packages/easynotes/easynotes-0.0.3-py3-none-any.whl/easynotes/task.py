import sys
import os
import random
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QListWidgetItem, QVBoxLayout, QWidget, QMenu, QTextEdit, QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import xml.etree.ElementTree as ET

class DraggableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)  # 允许拖动
        self.setAcceptDrops(True)  # 允许放置
        self.setDropIndicatorShown(True)  # 显示拖动指示器
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # 启用右键菜单
        self.customContextMenuRequested.connect(self.showContextMenu)  # 连接右键菜单事件

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        # 获取拖动源和目标位置
        source = event.source()
        item = source.currentItem()
        if item:
            # 保存当前任务的备注
            self.window().saveTaskNote()

            # 获取目标位置
            target_row = self.indexAt(event.pos()).row()
            if target_row == -1:
                target_row = self.count()  # 如果拖动到空白区域，放到最后

            # 从原列表中移除任务
            source.takeItem(source.row(item))
            # 插入到目标位置
            self.insertItem(target_row, item)
            self.setCurrentItem(item)  # 设置当前选中项

            # 更新当前选中项并刷新备注栏
            self.window().current_item = item
            self.window().showTaskNote(item)  # 刷新备注栏

            # 保存任务状态
            self.window().saveTasks()

    def showContextMenu(self, position):
        menu = QMenu(self)
        add_action = menu.addAction("新建任务")
        delete_action = menu.addAction("删除任务")

        # 连接菜单选项的点击事件
        add_action.triggered.connect(self.addTask)
        item = self.itemAt(position)
        if item:
            delete_action.triggered.connect(lambda: self.deleteTask(item))

        menu.exec_(self.viewport().mapToGlobal(position))

    def addTask(self):
        # 在当前列表中添加一个可编辑的项
        task_id = self.window().generateUniqueTaskId()  # 生成唯一ID
        item = QListWidgetItem("新任务")
        item.setData(Qt.UserRole, task_id)  # 将任务ID存储在Item中
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.addItem(item)
        self.editItem(item)  # 直接进入编辑模式

        # 更新当前选中项并清空备注栏
        self.window().current_item = item
        self.window().note_edit.clear()

        self.window().saveTasks()  # 实时保存

    def deleteTask(self, item):
        self.takeItem(self.row(item))  # 删除任务
        self.window().saveTasks()  # 保存任务

class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        # 获取程序所在的目录
        self.program_dir = os.path.dirname(os.path.abspath(__file__))
        self.setting_file = os.path.join(self.program_dir, "setting.xml")
        self.work_dir = self.load_or_create_setting()  # 加载或创建工作目录
        self.task_file = os.path.join(self.work_dir, "task.xml")  # task.xml 文件路径
        self.backup_dir = os.path.join(self.work_dir, "backup")  # 备份文件夹路径
        self.current_item = None  # 当前选中的任务项

        # 初始化备份文件夹
        self.init_backup_dir()

        # 备份 task.xml
        self.backup_task_file()

        self.initUI()
        self.loadTasks()

    def init_backup_dir(self):
        """初始化备份文件夹"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def backup_task_file(self):
        """备份 task.xml 文件"""
        if not os.path.exists(self.task_file):
            return

        # 获取当前备份文件列表
        backup_files = sorted(
            [f for f in os.listdir(self.backup_dir) if f.startswith("task") and f.endswith(".xml")],
            key=lambda x: int(x[4:-4]) if x[4:-4].isdigit() else 0
        )

        # 计算下一个备份文件的编号
        if not backup_files:
            next_backup_num = 1
        else:
            last_backup_num = int(backup_files[-1][4:-4])
            next_backup_num = (last_backup_num % 20) + 1  # 循环覆盖 1-20

        # 备份文件路径
        backup_file = os.path.join(self.backup_dir, f"task{next_backup_num}.xml")

        # 复制 task.xml 到备份文件
        shutil.copy2(self.task_file, backup_file)
        print(f"已备份到: {backup_file}")

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

    def initUI(self):
        self.setWindowTitle('任务管理软件')
        self.setGeometry(100, 100, 1024, 768)  # 设置窗体大小为1024x768

        # 设置灰色主题
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E;
            }
            QListWidget {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #555555;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:hover {
                background-color: #4E4E4E;
            }
            QTextEdit {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #555555;
                padding: 5px;
                font-size: 14px;
            }
        """)

        # 创建主布局
        main_layout = QHBoxLayout()

        # 左侧任务列表布局
        task_layout = QVBoxLayout()

        # 未开展的任务
        self.todo_list = DraggableListWidget()
        self.todo_list.itemClicked.connect(self.showTaskNote)
        self.todo_list.itemDoubleClicked.connect(self.editTask)
        self.todo_list.currentItemChanged.connect(self.handleCurrentItemChanged)  # 绑定 currentItemChanged 事件
        task_layout.addWidget(self.todo_list)

        # 正在开展的任务
        self.in_progress_list = DraggableListWidget()
        self.in_progress_list.itemClicked.connect(self.showTaskNote)
        self.in_progress_list.itemDoubleClicked.connect(self.editTask)
        self.in_progress_list.currentItemChanged.connect(self.handleCurrentItemChanged)  # 绑定 currentItemChanged 事件
        self.in_progress_list.setStyleSheet("QListWidget::item { color: red; }")
        task_layout.addWidget(self.in_progress_list)

        # 已完成的任务
        self.done_list = DraggableListWidget()
        self.done_list.itemClicked.connect(self.showTaskNote)
        self.done_list.itemDoubleClicked.connect(self.editTask)
        self.done_list.currentItemChanged.connect(self.handleCurrentItemChanged)  # 绑定 currentItemChanged 事件
        font = QFont()
        font.setStrikeOut(True)
        self.done_list.setFont(font)
        self.done_list.setStyleSheet("QListWidget::item { color: #888888; }")
        task_layout.addWidget(self.done_list)

        # 右侧备注窗体
        self.note_edit = QTextEdit()
        self.note_edit.setPlaceholderText("备注")
        self.note_edit.textChanged.connect(self.saveTaskNote)  # 实时保存备注

        # 将任务列表和备注窗体添加到主布局
        main_layout.addLayout(task_layout, 3)  # 任务列表占3份宽度
        main_layout.addWidget(self.note_edit, 1)  # 备注窗体占1份宽度

        # 设置主窗口的中心部件
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # 定时器用于实时保存
        self.save_timer = QTimer()
        self.save_timer.timeout.connect(self.saveTasks)
        self.save_timer.start(1000)  # 每1秒保存一次

    def handleCurrentItemChanged(self, current, previous):
        # 当当前选中项改变时，更新备注栏
        if current:
            self.current_item = current
            self.showTaskNote(current)

    def generateUniqueTaskId(self):
        # 生成一个6位随机数作为任务ID，确保不与现有ID重复
        existing_ids = self.getAllTaskIds()
        while True:
            task_id = str(random.randint(100000, 999999))  # 生成6位随机数
            if task_id not in existing_ids:
                return task_id

    def getAllTaskIds(self):
        # 获取所有任务的ID
        try:
            if not os.path.exists(self.task_file):
                return set()

            tree = ET.parse(self.task_file)
            root = tree.getroot()
            return {task.get("id") for task in root.findall("task")}
        except Exception as e:
            print(f"获取任务ID失败: {e}")
            return set()

    def showTaskNote(self, item):
        # 显示当前任务的备注
        if item:
            self.current_item = item  # 更新当前选中项
            task_id = item.data(Qt.UserRole)  # 获取任务ID
            task_note = self.getTaskNote(task_id)
            self.note_edit.setPlainText(task_note)

    def saveTaskNote(self):
        # 保存当前任务的备注
        if self.current_item:
            task_id = self.current_item.data(Qt.UserRole)  # 获取任务ID
            task_note = self.note_edit.toPlainText()
            self.updateTaskNote(task_id, task_note)
            self.saveTasks()  # 实时保存

    def getTaskNote(self, task_id):
        # 从 XML 文件中获取任务的备注
        try:
            if not os.path.exists(self.task_file):
                return ""

            tree = ET.parse(self.task_file)
            root = tree.getroot()

            for task in root.findall("task"):
                if task.get("id") == task_id:
                    return task.get("note", "")
            return ""
        except Exception as e:
            print(f"获取备注失败: {e}")
            return ""

    def updateTaskNote(self, task_id, task_note):
        # 更新任务的备注
        try:
            if not os.path.exists(self.task_file):
                return

            tree = ET.parse(self.task_file)
            root = tree.getroot()

            for task in root.findall("task"):
                if task.get("id") == task_id:
                    task.set("note", task_note)
                    break

            tree.write(self.task_file, encoding="utf-8", xml_declaration=True)
        except Exception as e:
            print(f"更新备注失败: {e}")

    def editTask(self, item):
        # 根据任务所在的列表来调用相应的 editItem 方法
        if self.todo_list.row(item) != -1:
            self.todo_list.editItem(item)
        elif self.in_progress_list.row(item) != -1:
            self.in_progress_list.editItem(item)
        elif self.done_list.row(item) != -1:
            self.done_list.editItem(item)
        self.saveTasks()  # 实时保存

    def saveTasks(self):
        root = ET.Element("tasks")

        # 保存未开展的任务
        for i in range(self.todo_list.count()):
            item = self.todo_list.item(i)
            task_id = item.data(Qt.UserRole)
            text = item.text()
            if text.strip():  # 跳过空任务
                task = ET.SubElement(root, "task")
                task.set("id", task_id)
                task.set("status", "todo")
                task.set("text", text)
                task.set("note", self.getTaskNote(task_id))

        # 保存正在开展的任务
        for i in range(self.in_progress_list.count()):
            item = self.in_progress_list.item(i)
            task_id = item.data(Qt.UserRole)
            text = item.text()
            if text.strip():  # 跳过空任务
                task = ET.SubElement(root, "task")
                task.set("id", task_id)
                task.set("status", "in_progress")
                task.set("text", text)
                task.set("note", self.getTaskNote(task_id))

        # 保存已完成的任务
        for i in range(self.done_list.count()):
            item = self.done_list.item(i)
            task_id = item.data(Qt.UserRole)
            text = item.text()
            if text.strip():  # 跳过空任务
                task = ET.SubElement(root, "task")
                task.set("id", task_id)
                task.set("status", "done")
                task.set("text", text)
                task.set("note", self.getTaskNote(task_id))

        try:
            tree = ET.ElementTree(root)
            tree.write(self.task_file, encoding="utf-8", xml_declaration=True)
        except Exception as e:
            print(f"保存任务失败: {e}")

    def loadTasks(self):
        try:
            if not os.path.exists(self.task_file):
                # 如果文件不存在，创建一个空的 XML 文件
                root = ET.Element("tasks")
                tree = ET.ElementTree(root)
                tree.write(self.task_file, encoding="utf-8", xml_declaration=True)
                print("任务文件不存在，已创建空文件")
                return

            # 清空现有任务
            self.todo_list.clear()
            self.in_progress_list.clear()
            self.done_list.clear()

            tree = ET.parse(self.task_file)
            root = tree.getroot()

            for task in root.findall("task"):
                status = task.get("status")
                task_id = task.get("id")
                text = task.get("text")
                note = task.get("note", "")

                if text.strip():  # 跳过空任务
                    item = QListWidgetItem(text)
                    item.setData(Qt.UserRole, task_id)  # 存储任务ID
                    item.setFlags(item.flags() | Qt.ItemIsEditable)  # 允许编辑
                    if status == "todo":
                        self.todo_list.addItem(item)
                    elif status == "in_progress":
                        self.in_progress_list.addItem(item)
                    elif status == "done":
                        self.done_list.addItem(item)

        except Exception as e:
            print(f"加载任务失败: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = TaskManager()
    manager.show()
    sys.exit(app.exec_())
