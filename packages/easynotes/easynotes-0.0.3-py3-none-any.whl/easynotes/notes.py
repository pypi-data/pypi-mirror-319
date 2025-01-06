import sys
import os
import base64
import subprocess
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QTextEdit, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QFileDialog, QMessageBox, QFontDialog, QColorDialog, QInputDialog,
    QToolBar, QAction, QMenu, QLabel, QDialog, QSpinBox, QFormLayout, QDialogButtonBox
)
from PyQt5.QtGui import (
    QTextCharFormat, QFont, QColor, QTextCursor, QIcon, QImage, QPixmap, QTextImageFormat,
    QKeySequence, QPalette
)
from PyQt5.QtCore import Qt, QMimeData, QByteArray, QBuffer, QIODevice
import xml.etree.ElementTree as ET

class ResizeImageDialog(QDialog):
    """调整图片大小的对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("调整图片大小")
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(10, 1000)  # 设置宽度范围
        self.width_spinbox.setValue(200)  # 默认宽度
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(10, 1000)  # 设置高度范围
        self.height_spinbox.setValue(200)  # 默认高度

        # 布局
        layout = QFormLayout(self)
        layout.addRow("宽度:", self.width_spinbox)
        layout.addRow("高度:", self.height_spinbox)

        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)

    def get_size(self):
        """获取用户输入的宽度和高度"""
        return self.width_spinbox.value(), self.height_spinbox.value()

class NoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # 获取程序所在的目录
        self.program_dir = os.path.dirname(os.path.abspath(__file__))
        self.setting_file = os.path.join(self.program_dir, "setting.xml")
        self.work_dir = self.load_or_create_setting()  # 加载或创建工作目录
        self.current_file = os.path.join(self.work_dir, "notes.xml")  # notes.xml 文件路径
        self.backup_dir = os.path.join(self.work_dir, "backup")  # 备份文件夹路径

        # 初始化备份文件夹
        self.init_backup_dir()

        # 备份 notes.xml
        self.backup_notes_file()

        self.initUI()
        self.load_notes()

    def init_backup_dir(self):
        """初始化备份文件夹"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def backup_notes_file(self):
        """备份 notes.xml 文件"""
        if not os.path.exists(self.current_file):
            return

        # 获取当前备份文件列表
        backup_files = sorted(
            [f for f in os.listdir(self.backup_dir) if f.startswith("notes") and f.endswith(".xml")],
            key=lambda x: int(x[5:-4]) if x[5:-4].isdigit() else 0
        )

        # 计算下一个备份文件的编号
        if not backup_files:
            next_backup_num = 1
        else:
            last_backup_num = int(backup_files[-1][5:-4])
            next_backup_num = (last_backup_num % 20) + 1  # 循环覆盖 1-20

        # 备份文件路径
        backup_file = os.path.join(self.backup_dir, f"notes{next_backup_num}.xml")

        # 复制 notes.xml 到备份文件
        shutil.copy2(self.current_file, backup_file)
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
        self.setWindowTitle('笔记软件 v 0.0.2')  # 添加版本号
        self.setGeometry(100, 100, 800, 600)

        # 设置灰色主题
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E3440;
            }
            QListWidget {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 1px solid #4C566A;
                border-radius: 5px;
                padding: 5px;
            }
            QTextEdit {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 1px solid #4C566A;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #4C566A;
                color: #ECEFF4;
                border: none;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
            QToolBar {
                background-color: #3B4252;
                border: none;
                padding: 5px;
            }
            QToolButton {
                color: white;  /* 设置文本颜色为白色 */
                background-color: transparent;  /* 背景透明 */
                border: none;  /* 去除边框 */
                padding: 5px;  /* 内边距 */
            }
            QToolButton:hover {
                background-color: #5E81AC;  /* 悬停时背景颜色 */
            }
            QMenu {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 1px solid #4C566A;
                border-radius: 5px;
            }
            QMenu::item:selected {
                background-color: #5E81AC;
            }
        """)

        # 左侧笔记标题列表
        self.note_list = QListWidget()
        self.note_list.currentItemChanged.connect(self.show_note_content)  # 监听当前项变化
        self.note_list.setDragEnabled(True)  # 启用拖动
        self.note_list.setDragDropMode(QListWidget.InternalMove)  # 设置拖动模式为内部移动
        self.note_list.setContextMenuPolicy(Qt.CustomContextMenu)  # 启用右键菜单
        self.note_list.customContextMenuRequested.connect(self.show_note_list_context_menu)  # 连接右键菜单事件
        self.note_list.itemDoubleClicked.connect(self.rename_note)  # 双击修改笔记名称

        # 右侧笔记内容编辑框
        self.note_content = QTextEdit()
        self.note_content.textChanged.connect(self.save_note)
        self.note_content.setAcceptRichText(True)  # 允许富文本
        self.note_content.setContextMenuPolicy(Qt.CustomContextMenu)  # 启用自定义右键菜单
        self.note_content.customContextMenuRequested.connect(self.show_context_menu)  # 连接右键菜单事件

        # 设置默认字体为微软雅黑
        font = QFont("微软雅黑", 10)
        self.note_content.setFont(font)

        # 工具栏
        toolbar = QToolBar("格式工具栏")
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # 加粗按钮
        bold_action = QAction("B", self)  # 使用文本 "B"
        bold_action.triggered.connect(self.toggle_bold)
        toolbar.addAction(bold_action)

        # 斜体按钮
        italic_action = QAction("I", self)  # 使用文本 "I"
        italic_action.triggered.connect(self.toggle_italic)
        toolbar.addAction(italic_action)

        # 下划线按钮
        underline_action = QAction("_", self)  # 使用文本 "_"
        underline_action.triggered.connect(self.toggle_underline)
        toolbar.addAction(underline_action)

        # 字体按钮
        font_action = QAction("F", self)  # 使用文本 "F"
        font_action.triggered.connect(self.change_font)
        toolbar.addAction(font_action)

        # 颜色按钮
        color_action = QAction("C", self)  # 使用文本 "C"
        color_action.triggered.connect(self.change_color)
        toolbar.addAction(color_action)



        # 按钮
        self.new_as_button = QPushButton('新建')
        self.new_as_button.clicked.connect(self.new_file)
        # 按钮
        self.save_as_button = QPushButton('另存')
        self.save_as_button.clicked.connect(self.save_as)

        self.open_button = QPushButton('打开')
        self.open_button.clicked.connect(self.open_xml)

        self.clear_button = QPushButton('清空')  # 清空笔记按钮
        self.clear_button.clicked.connect(self.clear_notes)

        self.about_button = QPushButton('关于')  # 关于按钮
        self.about_button.clicked.connect(self.show_about)

        # 布局
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.note_list)
        left_layout.addWidget(self.new_as_button)  
        left_layout.addWidget(self.open_button)
        left_layout.addWidget(self.save_as_button)
        left_layout.addWidget(self.clear_button)  # 添加清空笔记按钮
        left_layout.addWidget(self.about_button)  # 添加关于按钮

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.note_content)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 3)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # 支持 Ctrl+C 和 Ctrl+V
        self.note_content.keyPressEvent = self.custom_key_press_event

    def show_note_list_context_menu(self, pos):
        """显示笔记列表的右键菜单"""
        context_menu = QMenu(self)

        # 添加菜单项
        add_note_action = context_menu.addAction("新增笔记")
        add_note_action.triggered.connect(self.add_note)

        delete_note_action = context_menu.addAction("删除笔记")
        delete_note_action.triggered.connect(self.delete_note)

        # 显示菜单
        context_menu.exec_(self.note_list.mapToGlobal(pos))

    def new_file(self):
        """新建文件"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "新建文件", "", "XML Files (*.xml);;All Files (*)", options=options)
        if file_name:
            self.current_file = file_name
            self.root = ET.Element('notes')  # 创建新的根节点
            self.tree = ET.ElementTree(self.root)
            self.tree.write(self.current_file)  # 保存空文件
            self.note_list.clear()  # 清空笔记列表
            self.note_content.clear()  # 清空笔记内容
            self.setWindowTitle(f'笔记软件 v1.0 - {self.current_file}')  # 更新窗口标题

    def add_note(self):
        """新增笔记"""
        while True:
            title, ok = QInputDialog.getText(self, '新增笔记', '请输入笔记标题:')
            if not ok:
                return  # 用户取消输入

            # 检查标题是否重复
            if title in [self.note_list.item(i).text() for i in range(self.note_list.count())]:
                QMessageBox.warning(self, "错误", "笔记标题不能重复，请重新输入！")
            else:
                break

        self.note_list.addItem(title)
        new_note = ET.SubElement(self.root, 'note')
        ET.SubElement(new_note, 'title').text = title
        ET.SubElement(new_note, 'content').text = ''
        self.tree.write(self.current_file)

    def rename_note(self, item):
        """双击修改笔记名称"""
        old_title = item.text()
        while True:
            new_title, ok = QInputDialog.getText(self, '改名', '请输入新的笔记标题:', text=old_title)
            if not ok:
                return  # 用户取消输入

            # 检查标题是否重复
            if new_title == old_title:
                break  # 标题未修改，直接退出

            if new_title in [self.note_list.item(i).text() for i in range(self.note_list.count())]:
                QMessageBox.warning(self, "错误", "笔记标题不能重复，请重新输入！")
            else:
                break

        # 更新笔记标题
        item.setText(new_title)
        for note in self.root.findall('note'):
            if note.find('title').text == old_title:
                note.find('title').text = new_title
                break
        self.tree.write(self.current_file)

    def delete_note(self):
        """删除笔记"""
        selected_item = self.note_list.currentItem()
        if selected_item:
            title = selected_item.text()
            for note in self.root.findall('note'):
                if note.find('title').text == title:
                    self.root.remove(note)
                    break
            self.tree.write(self.current_file)
            self.note_list.takeItem(self.note_list.row(selected_item))


    def custom_key_press_event(self, event):
        # 处理 Ctrl+C 和 Ctrl+V
        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_C:  # Ctrl+C
                self.note_content.copy()
            elif event.key() == Qt.Key_V:  # Ctrl+V
                self.paste_image_or_text()
        else:
            QTextEdit.keyPressEvent(self.note_content, event)

    def paste_image_or_text(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasImage():  # 粘贴图片
            self.paste_image()
        elif mime_data.hasText():  # 粘贴文本
            self.note_content.paste()

    def paste_image(self):
        """粘贴图片并插入原始大小"""
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasImage():
            image = QImage(mime_data.imageData())
            # 将图片转换为 Base64 编码
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QIODevice.WriteOnly)
            image.save(buffer, "PNG")
            base64_data = base64.b64encode(byte_array.data()).decode('utf-8')

            # 插入图片到笔记内容
            cursor = self.note_content.textCursor()
            image_format = QTextImageFormat()
            image_format.setName(f"data:image/png;base64,{base64_data}")
            cursor.insertImage(image_format)

    def resize_image(self, cursor):
        """调整图片大小"""
        # 获取图片格式
        image_format = cursor.charFormat().toImageFormat()
        if image_format.isValid():
            # 弹出调整大小的对话框
            dialog = ResizeImageDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                width, height = dialog.get_size()
                # 获取图片的 Base64 数据
                image_src = image_format.name()  # 获取图片的 src 属性
                if image_src.startswith("data:image/png;base64,"):
                    base64_data = image_src[len("data:image/png;base64,"):]
                    # 创建新的图片格式
                    new_image_format = QTextImageFormat()
                    new_image_format.setWidth(width)
                    new_image_format.setHeight(height)
                    new_image_format.setName(f"data:image/png;base64,{base64_data}")
                    # 删除原有图片
                    cursor.deleteChar()
                    # 插入调整大小后的图片
                    cursor.insertImage(new_image_format)

    def show_context_menu(self, pos):
        # 创建右键菜单
        context_menu = QMenu(self)

        # 添加菜单项
        undo_action = context_menu.addAction("撤销")
        undo_action.triggered.connect(self.note_content.undo)

        redo_action = context_menu.addAction("重做")
        redo_action.triggered.connect(self.note_content.redo)

        context_menu.addSeparator()

        copy_action = context_menu.addAction("复制")
        copy_action.triggered.connect(self.note_content.copy)

        paste_action = context_menu.addAction("粘贴")
        paste_action.triggered.connect(self.paste_image_or_text)

        context_menu.addSeparator()

        cut_action = context_menu.addAction("剪切")
        cut_action.triggered.connect(self.note_content.cut)

        delete_action = context_menu.addAction("删除")
        delete_action.triggered.connect(self.note_content.cut)  # 删除功能类似于剪切

        # 添加调整图片大小选项
        cursor = self.note_content.cursorForPosition(pos)
        image_format = cursor.charFormat().toImageFormat()
        if image_format.isValid():
            context_menu.addSeparator()
            resize_action = context_menu.addAction("调整图片大小")
            resize_action.triggered.connect(lambda: self.resize_image(cursor))

        # 显示菜单
        context_menu.exec_(self.note_content.mapToGlobal(pos))

    def load_notes(self):
        try:
            self.tree = ET.parse(self.current_file)
            self.root = self.tree.getroot()
            self.note_list.clear()
            for note in self.root.findall('note'):
                title = note.find('title').text
                self.note_list.addItem(title)
        except FileNotFoundError:
            self.root = ET.Element('notes')
            self.tree = ET.ElementTree(self.root)

    def show_note_content(self):
        # 保存当前笔记内容
        if hasattr(self, 'current_note_title') and self.current_note_title:
            self.save_note()

        # 加载新笔记内容
        selected_item = self.note_list.currentItem()
        if selected_item:
            self.current_note_title = selected_item.text()
            for note in self.root.findall('note'):
                if note.find('title').text == self.current_note_title:
                    content = note.find('content').text
                    self.note_content.setHtml(content)  # 使用 setHtml 加载带格式的内容
                    break

    def save_note(self):
        if hasattr(self, 'current_note_title') and self.current_note_title:
            content = self.note_content.toHtml()  # 使用 toHtml 保存带格式的内容
            for note in self.root.findall('note'):
                if note.find('title').text == self.current_note_title:
                    note.find('content').text = content
                    break
            self.tree.write(self.current_file)

    def clear_notes(self):
        """清空笔记"""
        # 弹出确认框
        confirm, ok = QInputDialog.getText(self, "确认清空", "请输入 'R' 确认清空所有笔记:")
        if ok and confirm == 'R':
            self.note_list.clear()
            self.note_content.clear()
            self.root.clear()  # 清空 XML 根节点
            self.tree.write(self.current_file)
            QMessageBox.information(self, "清空成功", "所有笔记已清空！")

    def save_as(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "另存为", "", "XML Files (*.xml);;All Files (*)", options=options)
        if file_name:
            self.tree.write(file_name)
            self.current_file = file_name
            self.setWindowTitle(f'笔记软件 v1.0 - {self.current_file}')  # 更新窗口标题

    def open_xml(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "打开", "", "XML Files (*.xml);;All Files (*)", options=options)
        if file_name:
            self.current_file = file_name
            self.setWindowTitle(f'笔记软件 v1.0 - {self.current_file}')  # 更新窗口标题
            self.load_notes()  # 重新加载笔记

    def show_about(self):
        # 显示关于信息
        QMessageBox.information(self, "关于", "开发者：sysucai\n411703730@qq.com")

    def change_font(self):
        cursor = self.note_content.textCursor()
        if cursor.hasSelection():
            # 设置默认字体为微软雅黑
            default_font = QFont("微软雅黑", 10)
            font, ok = QFontDialog.getFont(default_font, self, "选择字体")
            if ok:
                format = QTextCharFormat()
                format.setFont(font)
                cursor.mergeCharFormat(format)

    def change_color(self):
        cursor = self.note_content.textCursor()
        if cursor.hasSelection():
            color = QColorDialog.getColor()
            if color.isValid():
                format = QTextCharFormat()
                format.setForeground(color)
                cursor.mergeCharFormat(format)

    def toggle_bold(self):
        cursor = self.note_content.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            if cursor.charFormat().fontWeight() == QFont.Bold:
                format.setFontWeight(QFont.Normal)
            else:
                format.setFontWeight(QFont.Bold)
            cursor.mergeCharFormat(format)

    def toggle_italic(self):
        cursor = self.note_content.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            format.setFontItalic(not cursor.charFormat().fontItalic())
            cursor.mergeCharFormat(format)

    def toggle_underline(self):
        cursor = self.note_content.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            format.setFontUnderline(not cursor.charFormat().fontUnderline())
            cursor.mergeCharFormat(format)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NoteApp()
    ex.show()
    sys.exit(app.exec_())
