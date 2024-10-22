# -*- coding: utf-8 -*-
import math

from PySide6.QtCore import (QCoreApplication, QRect, QSize, Qt, QMetaObject)
from PySide6.QtGui import (QCursor, QFont, QIcon, QMouseEvent)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QFrame, QGridLayout, QSpacerItem, QSizePolicy,
                               QStackedWidget, QTabWidget, QLabel, QSpinBox,
                               QAbstractSpinBox, QComboBox, QFileDialog)
from matplotlib.colors import ListedColormap
from pywin.framework.mdi_pychecker import BUTTON
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.patches as mpatches
import Icon_rc  # Assuming this imports necessary resources
from plot_tools import PlotTool
from matplotlib import rcParams
import os
# 配置字体
rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体（SimHei）
rcParams['axes.unicode_minus'] = False    # 解决负号显示问题
class DraggableTitleBar(QFrame):
    def __init__(self, form, parent=None):
        super().__init__(parent)
        self.old_pos = None
        self.Form = form
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        # 判断是否为左键双击
        if event.button() == Qt.LeftButton:
            if self.Form.is_maximized:
                self.Form.showNormal()
            else:
                self.Form.showMaximized()
            self.Form.is_maximized = not self.Form.is_maximized
        else:
            super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self.old_pos:
            # 计算鼠标移动的位移
            delta = event.globalPosition().toPoint() - self.old_pos
            # 移动父窗口
            self.window().move(self.window().pos() + delta)
            # 更新鼠标位置
            self.old_pos = event.globalPosition().toPoint()

# class MatPlot_Canvas():
#     def __init__(self, size):
#         self.figure = Figure(figsize=size)  # 调整Figure的尺寸
#         self.canvas = FigureCanvas(self.figure)
#         self.toolbar = NavigationToolbar(self.canvas, self)
class Ui_Form(QWidget, PlotTool):
    ICONS = {
        'theme': ":/Main/yarn-ball.png",
        'theme_push': ":/Main/yarn-ball (1).png",
        'minimize': ":/Main/minus-small.png",
        'window': ":/Main/window-restore.png",
        'close': ":/Main/cross-small.png",
        'main': ":/Main/data-transfer.png",
        'main_push': ":/Main/data-transfer (1).png",
        'calculator': ":/Main/calculator.png",
        'calculator_push': ":/Main/calculator (1).png",
        'translate': ":/Main/translate.png",
        'translate_push': ":/Main/translate (1).png",
        'chat': ":/Main/mobile-message.png",
        'chat_push': ":/Main/mobile-message (1).png",
        'info': ":/Main/info.png",
        'info_push': ":/Main/info-.png",
        'setting': ":/Main/customization-cogwheel.png",
        'setting_push': ":/Main/customization-cogwheel-.png",
    }
    def button_style(self, hover_icon):
        BUTTON_STYLES = f"""
            QPushButton {{
                background-color: #F2E8C6;
                color: #F7C566;
                padding: 0px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                icon: url({hover_icon});
                background-color: #DAD4B5;
            }}
            QPushButton:checked {{
                icon: url({hover_icon});
                background-color: #DAD4B5;
            }}
        """
        return BUTTON_STYLES

    TITLE_BAR_STYLES_THEME =  """
        QPushButton {
            background-color: #F2E8C6;
            color: white;
            padding: 0px;
            border-radius: 0px;
        }
        QPushButton:checked {
            icon: url(":/Main/yarn-ball (1).png");
            background-color: #DAD4B5;
        }
    """

    TITLE_BAR_STYLES = """
        QPushButton {
            background-color: #F2E8C6;
            color: white;
            padding: 0px;
            border-radius: 0px;
        }
        QPushButton:hover {
            background-color: #DAD4B5;
        }
    """
    TITLE_BAR_STYLES_CLOSE = """
        QPushButton {
            background-color: #F2E8C6;
            color: white;
            padding: 0px 0px;
            border-radius: 0px;
        }
        
        QPushButton:hover {
            background-color: #982B1C;
        }
    """
    BUTTON_CST_STYLE = """
        QPushButton{ background-color:#F2E8C6;
            border-radius:5px;
            color:#56504a; 
        }
        QPushButton::hover{
            background-color:#c2ba9e;
        }
        """
    def __init__(self):
        super().__init__()
        self.cst_structure_parameters = None
        self.cst_structure_file_path = ''
        self.cst_result_folder_path = ''
        self.last_directory = os.path.expanduser("~")
    def create_font(self, family="微软雅黑", size=10, bold=True):
        font = QFont()
        font.setFamilies([family])
        font.setPointSize(size)
        font.setBold(bold)
        return font
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1174, 885)
        icon_main = QIcon()
        icon_main.addFile(u":/Main/yarn-ball.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Form.setWindowIcon(icon_main)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # Layout and widget setup
        self.layoutWidget = QWidget(Form)
        self.setContentsMargins(0, 0, 0, 0)
        self.layoutWidget.setGeometry(QRect(60, 40, 911, 718))
        self.verticalLayout_4 = QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)

        self.setup_title_bar(Form)
        self.setup_main_layout()

        self.retranslateUi(Form)
        self.connect_navigation_buttons(self.change_page)
        self.is_maximized = False
        self.is_dark_mode = False
        QMetaObject.connectSlotsByName(Form)

    def setup_title_bar(self, Form):
        """Setup the title bar with minimize, maximize and close buttons."""
        self.horizontalLayout = QHBoxLayout()
        self.pbSwitchTheme = self.create_button(self.ICONS['theme'], (50, 40), (30, 30), self.TITLE_BAR_STYLES_THEME, checkable=True)
        self.pbSwitchTheme.clicked.connect(lambda:self.switch_theme(Form))
        self.horizontalLayout.addWidget(self.pbSwitchTheme)

        self.titleBar = DraggableTitleBar(Form)
        self.titleBar.setMinimumSize(QSize(200, 40))
        self.titleBar.setMaximumSize(QSize(16777215, 40))
        self.titleBar.setStyleSheet("background-color: #F2E8C6;")
        self.horizontalLayout.addWidget(self.titleBar)

        self.pbMinimize = self.create_button(self.ICONS['minimize'], (50, 40),(20, 20), self.TITLE_BAR_STYLES)
        self.pbWindow = self.create_button(self.ICONS['window'], (50, 40), (20, 20), self.TITLE_BAR_STYLES)
        self.pbClose = self.create_button(self.ICONS['close'], (50, 40), (20, 20), self.TITLE_BAR_STYLES_CLOSE)
        self.pbMinimize.clicked.connect(Form.showMinimized)
        self.pbWindow.clicked.connect(lambda: self.toggle_maximize_restore(Form))
        self.pbClose.clicked.connect(Form.close)
        self.horizontalLayout.addWidget(self.pbMinimize)
        self.horizontalLayout.addWidget(self.pbWindow)
        self.horizontalLayout.addWidget(self.pbClose)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

    def setup_main_layout(self):
        """Setup main layout including side navigation and stacked widget."""
        self.gridLayout = QGridLayout()
        self.sidebar = self.create_sidebar()
        self.stackedWidget = self.create_stacked_widget()

        self.gridLayout.addWidget(self.sidebar, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.stackedWidget, 0, 1, 1, 1)

        self.verticalLayout_3.addLayout(self.gridLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)

    def create_sidebar(self):
        """Create and return the sidebar with navigation buttons."""
        widget = QWidget()
        widget.setMinimumSize(QSize(50, 200))
        widget.setMaximumSize(QSize(50, 16777215))
        widget.setStyleSheet("background-color: #F2E8C6;")

        verticalLayout = QVBoxLayout(widget)
        verticalLayout.setSpacing(0)

        self.pbMain = self.create_button(self.ICONS['main'], (30, 30), (20, 20),self.button_style(self.ICONS['main_push']), checkable=True)
        self.pbCalculator = self.create_button(self.ICONS['calculator'], (30, 30), (20, 20),self.button_style(self.ICONS['calculator_push']), checkable=True)
        self.pbTranslate = self.create_button(self.ICONS['translate'], (30, 30), (20, 20),self.button_style(self.ICONS['translate_push']), checkable=True)
        self.pbAiChat = self.create_button(self.ICONS['chat'], (30, 30), (20, 20),self.button_style(self.ICONS['chat_push']), checkable=True)
        self.pbInfo = self.create_button(self.ICONS['info'], (30, 30), (20, 20),self.button_style(self.ICONS['info_push']))
        self.pbSetting = self.create_button(self.ICONS['setting'], (30, 30), (20, 20),self.button_style(self.ICONS['setting_push']))

        verticalLayout.addWidget(self.pbMain)
        verticalLayout.addWidget(self.pbCalculator)
        verticalLayout.addWidget(self.pbTranslate)
        verticalLayout.addWidget(self.pbAiChat)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        verticalLayout.addItem(spacer)

        verticalLayout.addWidget(self.pbInfo)
        verticalLayout.addWidget(self.pbSetting)

        return widget

    def create_stacked_widget(self):
        """Create and return the stacked widget with different pages."""
        stackedWidget = QStackedWidget()
        stackedWidget.setStyleSheet("QStackedWidget {background-color: #FFF8DC; color:#FF9843;}")

        self.mainPage = QWidget()
        self.calculatorPage = QWidget()
        self.translatePage = QWidget()
        self.aiChatPage = QWidget()

        self.setup_translate_tab()

        stackedWidget.addWidget(self.mainPage)
        stackedWidget.addWidget(self.calculatorPage)
        stackedWidget.addWidget(self.translatePage)
        stackedWidget.addWidget(self.aiChatPage)

        return stackedWidget

    def setup_translate_tab(self):
        """Setup the translate tab within the translate page."""
        self.verticalLayout_2 = QVBoxLayout(self.translatePage)
        self.tabWidget = QTabWidget()
        self.tabWidget.setStyleSheet("""
            QTabWidget { border: 1px solid #CCCCCC; background-color: #FFF8DC;color: #FF9843; }
            QTabBar::tab { background-color: #F2E8C6; border: 1px solid #F2E8C6; padding: 5px; margin: 2px; min-width: 80px; border-radius:5px;font-weight:bold; }
            QTabBar::tab:selected { background-color: #F2E8C6; border-bottom: 2px solid #8B7E4E; }
            QTabWidget::pane { border: 1px solid #837D67; background-color: #F2E8C6; border-radius: 5px; padding:5px; }
            QTabWidget::tab-bar { alignment: left; }
            QTabBar::tab::hover { background-color: #837D67; }
        """)

        self.tab1 = QWidget()
        self.vLayout_CstMy1 = QVBoxLayout(self.tab1)
        # *******************************************************
        # *                                                     *
        # *             自用Cst工具按钮布局                        *
        # *                                                     *
        # *******************************************************
        self.hLayout_CstMy1Button = QHBoxLayout()
        self.hLayout_CstMy1Button.setContentsMargins(0, 0, 0, 0)
        self.pbInportCstStruct = QPushButton(text='导入结构')
        self.pbInportCstStruct.clicked.connect(self.import_structure_file)
        self.pbInportCstStruct.setMinimumSize(QSize(60, 30))
        self.pbInportCstStruct.setMaximumSize(QSize(60, 30))

        self.pbInportCstStruct.setFont(self.create_font())
        self.pbInportCstStruct.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pbInportCstStruct.setStyleSheet(self.BUTTON_CST_STYLE)

        self.hLayout_CstMy1Button.addWidget(self.pbInportCstStruct)

        self.pbInportCstResult = QPushButton('设置结果文件夹')
        self.pbInportCstResult.clicked.connect(self.import_result_folder)
        self.pbInportCstResult.setMinimumSize(QSize(100, 30))
        self.pbInportCstResult.setMaximumSize(QSize(100, 30))
        self.pbInportCstResult.setFont(self.create_font())
        self.pbInportCstResult.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pbInportCstResult.setStyleSheet(self.BUTTON_CST_STYLE)

        self.hLayout_CstMy1Button.addWidget(self.pbInportCstResult)

        self.hLayout_CstMy1NowPlot = QHBoxLayout()
        self.hLayout_CstMy1NowPlot.setSpacing(0)
        self.labelCstNowPlot = QLabel('当前绘制：')
        self.labelCstNowPlot.setMinimumSize(QSize(70, 30))
        self.labelCstNowPlot.setMaximumSize(QSize(70, 30))
        self.labelCstNowPlot.setFont(self.create_font())

        self.hLayout_CstMy1NowPlot.addWidget(self.labelCstNowPlot)

        self.spinBoxCstNowPlot = QSpinBox(self.tab1)
        self.spinBoxCstNowPlot.valueChanged.connect(lambda: self.plot_data(self.spinBoxCstNowPlot.value()))
        self.spinBoxCstNowPlot.setEnabled(True)
        self.spinBoxCstNowPlot.setMinimumSize(QSize(100, 30))
        self.spinBoxCstNowPlot.setMaximumSize(QSize(100, 30))
        self.spinBoxCstNowPlot.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.spinBoxCstNowPlot.setReadOnly(False)
        self.spinBoxCstNowPlot.setSingleStep(2)
        self.spinBoxCstNowPlot.setStepType(QAbstractSpinBox.StepType.DefaultStepType)
        self.spinBoxCstNowPlot.setDisplayIntegerBase(10)

        self.hLayout_CstMy1NowPlot.addWidget(self.spinBoxCstNowPlot)

        self.hLayout_CstMy1Button.addLayout(self.hLayout_CstMy1NowPlot)

        self.horizontalLayout_CstMy1_button = QHBoxLayout()
        self.horizontalLayout_CstMy1_button.setSpacing(0)
        self.labelCstNowPlotMode = QLabel('当前绘制行数：')
        self.labelCstNowPlotMode.setMinimumSize(QSize(100, 30))
        self.labelCstNowPlotMode.setMaximumSize(QSize(100, 30))
        self.labelCstNowPlotMode.setFont(self.create_font())

        self.horizontalLayout_CstMy1_button.addWidget(self.labelCstNowPlotMode)

        self.comboBoxCstNowPlot = QComboBox(self.tab1)
        self.comboBoxCstNowPlot.addItem("1", userData=1)
        self.comboBoxCstNowPlot.addItem("2", userData=2)
        self.comboBoxCstNowPlot.addItem("3", userData=3)
        self.comboBoxCstNowPlot.setMinimumSize(QSize(100, 30))
        self.comboBoxCstNowPlot.setMaximumSize(QSize(100, 30))

        self.horizontalLayout_CstMy1_button.addWidget(self.comboBoxCstNowPlot)

        self.hLayout_CstMy1Button.addLayout(self.horizontalLayout_CstMy1_button)

        self.pbSavePlotCstStruct = QPushButton('保存图片')
        self.pbSavePlotCstStruct.setMinimumSize(QSize(60, 30))
        self.pbSavePlotCstStruct.setMaximumSize(QSize(60, 30))
        self.pbSavePlotCstStruct.setFont(self.create_font())
        self.pbSavePlotCstStruct.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pbSavePlotCstStruct.setStyleSheet(self.BUTTON_CST_STYLE)

        self.hLayout_CstMy1Button.addWidget(self.pbSavePlotCstStruct)

        self.pbPlotCstStruct = QPushButton('重新/绘制结构')
        self.pbPlotCstStruct.clicked.connect(lambda: self.plot_data(1))
        self.pbPlotCstStruct.setMinimumSize(QSize(100, 30))
        self.pbPlotCstStruct.setMaximumSize(QSize(100, 30))
        self.pbPlotCstStruct.setFont(self.create_font())
        self.pbPlotCstStruct.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pbPlotCstStruct.setStyleSheet(self.BUTTON_CST_STYLE)
        self.hLayout_CstMy1Button.addWidget(self.pbPlotCstStruct)
        """Cst自用工具Matplotlib画板"""
        self.figure = Figure(figsize=(15, 5))  # 调整Figure的尺寸
        self.figure.set_facecolor("#FFF8DC")
        self.canvas = FigureCanvas(self.figure)
        # 创建一个NavigationToolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.hLayout_CstMy1Button.addWidget(self.toolbar)


        self.vLayout_CstMy1.addWidget(self.canvas)

        self.vLayout_CstMy1.addLayout(self.hLayout_CstMy1Button)

        self.tab2 = QWidget()

        self.tabWidget.addTab(self.tab1, "CST自用")
        self.tabWidget.addTab(self.tab2, "Tab 2")

        self.verticalLayout_2.addWidget(self.tabWidget)

    # *******************************************************
    # *                                                     *
    # *             自用Cst工具画板部分                        *
    # *                                                     *
    # *******************************************************
    def import_structure_file(self):
        self.cst_structure_file_path = QFileDialog.getOpenFileName(self, '打开参数文件', self.last_directory, "csv文件(*.csv)")[0]
        self.last_directory = os.path.dirname(self.cst_structure_file_path)
        self.cst_structure_parameters = self.loadStructureParameters(self.cst_structure_file_path)

    def import_result_folder(self):
        self.cst_result_folder_path = QFileDialog.getExistingDirectory(self, '打开S参数保存文件夹', self.last_directory)
        self.last_directory = self.cst_result_folder_path

    def plot_data(self, num):
        if self.cst_structure_file_path == '':
            self.cst_structure_file_path = QFileDialog.getOpenFileName(self,'打开参数文件',self.last_directory,"csv文件(*.csv)" )[0]
            self.last_directory = os.path.dirname(self.cst_structure_file_path)
            self.cst_structure_parameters = self.loadStructureParameters(self.cst_structure_file_path)
        if self.cst_result_folder_path == '':
            self.cst_result_folder_path = QFileDialog.getExistingDirectory(self, '打开S参数保存文件夹',self.last_directory)
            self.last_directory = self.cst_result_folder_path

        # 清空Figure并绘制多个子图
        self.figure.clear()
        cmap_label = ListedColormap(['#eb9c4d', '#a8a39d', '#493736'])
        empty_patch = mpatches.Patch(color='#eb9c4d', label='Empty (0)')
        metal_patch = mpatches.Patch(color='#a8a39d', label='Aluminum (1)')
        vo2_patch = mpatches.Patch(color='#493736', label='Vanadium Dioxide (2)')
        rows = self.comboBoxCstNowPlot.currentData()
        self.spinBoxCstNowPlot.setSingleStep(rows)
        self.axes = []
        for i in range(rows):
            fre1_M, s11_M, fre2_M, s21_M, fre1_I, s11_I, fre2_I, s21_I = self.openCstTxtPair(self.cst_result_folder_path, num + i)
            matrix = self.plot_mirrored_matrix(self.cst_structure_parameters[num + i])
            for k in range(3):
                ax = self.figure.add_subplot(rows, 3, i * 3 + k + 1)
                ax.set_box_aspect(0.75)
                ax.tick_params(axis='both', which='major', labelsize=10, direction='in')
                ax.set_xlabel('Frequency(THz)', fontname='Times New Roman', fontsize=12)
                if k % 3 == 0:
                    ax.plot(fre1_I, self.calAbsorb(s11_I, s21_I), color='#962828')
                    ax.plot(fre1_M, self.calAbsorb(s11_M, s21_M), color='#3c61b3')
                    ax.set_title(f"No.{num + i} Absorption", fontname='Times New Roman')
                    ax.axis([0, 2.5, 0, 1])
                elif k % 3 == 1:
                    ax.plot(fre1_I, self.calTransmission(s21_I, 'linear'), color='#962828')
                    ax.plot(fre1_M, self.calTransmission(s21_M, 'linear'), color='#3c61b3')
                    ax.set_title(f"No.{num + i} Transmission", fontname='Times New Roman')
                elif k % 3 == 2:
                    ax.imshow(matrix, cmap=cmap_label, interpolation='nearest')
                    ax.legend(handles=[empty_patch, metal_patch, vo2_patch],
                               loc='center left',  # Position it to the left
                               bbox_to_anchor=(1, 0.5),  # Move it outside the plot to the right
                               title='Materials',
                               fontname='Times New Roman')
                    ax.axis('off')
                    ax.set_title(f"No.{num + i} Structure", fontname='Times New Roman')
                self.axes.append(ax)
            self.figure.tight_layout()
        # 更新Canvas
        self.canvas.draw()

    def create_button(self, icon_path, size, icon_size, style, checkable=False):
        """Create and return a QPushButton with given icon, size, style, and optional checkable flag."""
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(*icon_size))
        button.setMinimumSize(*size)
        button.setMaximumSize(*size)
        button.setStyleSheet(style)
        button.setCheckable(checkable)
        return button

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"CocoaBall", None))

    def connect_navigation_buttons(self, callback):
        """Connect navigation buttons to the callback function."""
        self.pbMain.clicked.connect(lambda: callback(0))
        self.pbCalculator.clicked.connect(lambda: callback(1))
        self.pbTranslate.clicked.connect(lambda: callback(2))
        self.pbAiChat.clicked.connect(lambda: callback(3))

    def set_active_button(self, index):
        """Set the active button based on the page index."""
        self.pbMain.setChecked(index == 0)
        self.pbCalculator.setChecked(index == 1)
        self.pbTranslate.setChecked(index == 2)
        self.pbAiChat.setChecked(index == 3)

    def change_page(self, index):
        """Change the page in the QStackedWidget and update the active button."""
        self.stackedWidget.setCurrentIndex(index)
        self.set_active_button(index)

    def toggle_maximize_restore(self, Form):
        if Form.is_maximized:
            Form.showNormal()
        else:
            Form.showMaximized()
        Form.is_maximized = not Form.is_maximized

    def switch_theme(self, Form):
        if self.is_dark_mode:
            icon_main = QIcon()
            icon_main.addFile(u":/Main/yarn-ball (1).png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
            Form.setWindowIcon(icon_main)
            self.is_dark_mode = False
        else:
            icon_main = QIcon()
            icon_main.addFile(u":/Main/yarn-ball.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
            Form.setWindowIcon(icon_main)
            self.is_dark_mode = True
