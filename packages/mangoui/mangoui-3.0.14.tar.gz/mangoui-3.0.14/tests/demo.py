import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, \
    QListWidgetItem, \
    QTextEdit, QStatusBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle("PySide6 界面示例")

        # 创建主窗口的中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QHBoxLayout(central_widget)

        # 左侧菜单栏
        left_menu = QListWidget()
        left_menu.setFixedWidth(200)  # 设置固定宽度

        # 创建一级菜单项
        menu_item1 = QListWidgetItem("菜单项1")
        menu_item2 = QListWidgetItem("菜单项2")
        menu_item3 = QListWidgetItem("菜单项3")

        # 添加一级菜单项到左侧菜单栏
        left_menu.addItem(menu_item1)
        left_menu.addItem(menu_item2)
        left_menu.addItem(menu_item3)

        # 创建二级菜单项
        sub_menu1 = QListWidget()
        sub_menu1.addItem("子菜单项1")
        sub_menu1.addItem("子菜单项2")
        sub_menu1.setVisible(False)  # 初始隐藏二级菜单

        sub_menu2 = QListWidget()
        sub_menu2.addItem("子菜单项3")
        sub_menu2.setVisible(False)  # 初始隐藏二级菜单

        sub_menu3 = QListWidget()
        sub_menu3.addItem("子菜单项4")
        sub_menu3.setVisible(False)  # 初始隐藏二级菜单

        # 将二级菜单与一级菜单项关联
        menu_item1.setData(1, sub_menu1)
        menu_item2.setData(1, sub_menu2)
        menu_item3.setData(1, sub_menu3)

        # 将左侧菜单栏添加到主布局
        main_layout.addWidget(left_menu)

        # 中间内容展示区域
        content_area = QVBoxLayout()
        text_edit = QTextEdit()
        content_area.addWidget(text_edit)
        main_layout.addLayout(content_area)

        # 底部状态栏
        status_bar = QStatusBar()
        status_bar.showMessage("状态栏：就绪")
        self.setStatusBar(status_bar)

        # 连接一级菜单项的点击事件
        left_menu.itemClicked.connect(self.on_menu_item_clicked)

    def on_menu_item_clicked(self, item):
        # 获取与一级菜单项关联的二级菜单
        sub_menu = item.data(1)

        # 切换二级菜单的显示状态
        if sub_menu:
            sub_menu.setVisible(not sub_menu.isVisible())

        # 更新状态栏显示当前选中的菜单项
        self.statusBar().showMessage(f"选中菜单项: {item.text()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
