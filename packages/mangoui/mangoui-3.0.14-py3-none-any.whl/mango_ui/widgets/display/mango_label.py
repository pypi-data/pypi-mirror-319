# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-08-24 17:08
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mango_ui.settings.settings import THEME


class MangoLabel(QLabel):
    def __init__(self, text=None, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.set_style()
        self.setText(str(text) if text is not None else '')

    def set_style(self, style="background-color: transparent; color: black;"):
        style = self.kwargs.get('style', style)
        self.setStyleSheet(style)


class MangoLabelWidget(QWidget):

    def __init__(self, text=None, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.kwargs['style'] = f"""
                   QLabel {{
                       color: {THEME.font_color};  /* 文字颜色 */
                       background-color: {kwargs.get('background_color', THEME.group.info)};  /* 背景颜色 */
                       padding: 6px 12px;  /* 内边距 */
                       border: none;  /* 无边框 */
                       border-radius: {THEME.border_radius};  /* 圆角 */
                       font-size: {THEME.font.text_size};  /* 字体大小 */
                       font-weight: 500;  /* 字体加粗 */
                   }}
               """
        # QLabel: hover
        # {{
        #     background - color: {THEME.hover.background_color}; / *悬停时背景颜色 * /
        # }}
        self.mango_label = MangoLabel(text=text, parent=self, **self.kwargs)

        layout = QHBoxLayout()
        layout.addWidget(self.mango_label, alignment=Qt.AlignCenter)  # type: ignore
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
