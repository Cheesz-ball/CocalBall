from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QFrame
from PySide6.QtCore import Qt

app = QApplication([])

# 创建主窗口
main_window = QWidget()
layout = QVBoxLayout()

# 创建一个容器作为按钮的背景
button_background = QFrame()
button_background.setStyleSheet("""
    QFrame {
        background-color: #A0D8E0; /* 背景颜色 */
        border-radius: 15px; /* 圆角半径 */
        padding: 0px; /* 内部填充设置为0 */
    }
""")

# 创建按钮
button = QPushButton("圆角按钮")
button.setStyleSheet("""
    QPushButton {
        border: none; /* 去掉按钮的边框 */
        background-color: transparent; /* 背景透明 */
        padding: 0px; /* 按钮内部填充设置为0 */
    }
    QPushButton:hover {
        background-color: #0078D7; /* 悬停时的背景颜色 */
        color: white; /* 悬停时的文字颜色 */
    }
""")

# 将按钮添加到背景容器中
button_layout = QVBoxLayout(button_background)
button_layout.setContentsMargins(0, 0, 0, 0)  # 设置边距为0
button_layout.setSpacing(0)  # 设置间距为0
button_layout.addWidget(button)
button_background.setLayout(button_layout)

# 将背景容器添加到主窗口的布局中
layout.addWidget(button_background)
main_window.setLayout(layout)

main_window.setWindowTitle("圆角按钮示例")
main_window.resize(300, 200)
main_window.show()

app.exec()
