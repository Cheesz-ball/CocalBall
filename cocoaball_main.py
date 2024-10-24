# -*- coding: utf-8 -*-
import math

from PySide6.QtCore import QCoreApplication, QRect, QSize, Qt, QMetaObject
from PySide6.QtGui import QCursor, QFont, QIcon, QMouseEvent
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QStackedWidget,
    QTabWidget,
    QLabel,
    QSpinBox,
    QAbstractSpinBox,
    QComboBox,
    QFileDialog,
    QProgressBar,
    QMessageBox,
)
from matplotlib.colors import ListedColormap
from pywin.framework.mdi_pychecker import BUTTON
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.patches as mpatches
from Theme import Theme
import Icon_rc
from plot_tools import PlotTool, SaveLMDB
from matplotlib import rcParams
import os


rcParams["font.sans-serif"] = ["SimHei"]
rcParams["axes.unicode_minus"] = False


# *******************************************************
# *                                                     *
# *                 自定义标题栏                          *
# *                                                     *
# *******************************************************
class DraggableTitleBar(QFrame):
    def __init__(self, form, parent=None):
        super().__init__(parent)
        self.old_pos = None
        self.Form = form

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        # 判断是否为左键双击
        if event.button() == Qt.MouseButton.LeftButton:
            if self.Form.is_maximized:
                self.Form.showNormal()
            else:
                self.Form.showMaximized()
            self.Form.is_maximized = not self.Form.is_maximized
        else:
            super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton and self.old_pos:
            # 计算鼠标移动的位移
            delta = event.globalPosition().toPoint() - self.old_pos
            # 移动父窗口
            self.window().move(self.window().pos() + delta)
            # 更新鼠标位置
            self.old_pos = event.globalPosition().toPoint()


# *******************************************************
# *                                                     *
# *                      主窗口                          *
# *                                                     *
# *******************************************************
class Ui_Form(QWidget):
    ICONS = {
        "qiuqiu": ":/Title/brandball.png",
        "keke": ":/Title/brandball_invert.png",
        "minimize": ":/Title/min.png",
        "window": ":/Title/window.png",
        "close": ":/Title/close.png",
        "home": ":/SideBar/home.png",
        "home_push": ":/SideBar/home_push.png",
        "calculator": ":/SideBar/calculator.png",
        "calculator_push": ":/SideBar/calculator_push.png",
        "translate": ":/SideBar/data_transfer.png",
        "translate_push": ":/SideBar/data_transfer_push.png",
        "chat": ":/SideBar/message.png",
        "chat_push": ":/SideBar/message_push.png",
        "info": ":/SideBar/info.png",
        "info_push": ":/SideBar/info_push.png",
        "setting": ":/SideBar/setting.png",
        "setting_push": ":/SideBar/setting_push.png",
        "up_arrow": ":/SpinBox/up.png",
        "down_arrow": ":/SpinBox/down.png",
    }

    def __init__(self):
        super().__init__()
        self.is_dark_mode = False
        self.theme = Theme(self.is_dark_mode)
        self.cst_structure_parameters = None
        self.cst_structure_file_path = ""
        self.cst_result_folder_path = ""
        self.last_directory = os.path.expanduser("~")
        self.plot_tools = PlotTool()

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
        icon_main.addFile(
            self.ICONS["qiuqiu"], QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        Form.setWindowIcon(icon_main)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # Layout and widget setup
        self.layoutWidget = QWidget(Form)
        self.setContentsMargins(0, 0, 0, 0)
        self.layoutWidget.setGeometry(QRect(60, 40, 911, 718))
        self.vLayout_Mainform = QVBoxLayout(Form)
        self.vLayout_Mainform.setContentsMargins(0, 0, 0, 0)
        self.vLayout_Main = QVBoxLayout()
        self.vLayout_Main.setSpacing(0)

        self.setup_title_bar(Form)

        self.setup_main_layout()
        self.setup_button_bar(Form)
        self.retranslateUi(Form)
        self.connect_navigation_buttons(self.change_page)
        self.is_maximized = False
        self.is_dark_mode = False
        self.applyTheme()
        QMetaObject.connectSlotsByName(Form)

    def setup_title_bar(self, Form):
        """Setup the title bar with minimize, maximize and close buttons."""
        self.horizontalLayout = QHBoxLayout()
        pbSwitchThemeStyle = self.button_title_style(
            self.theme.title_bar_color,
            self.theme.main_font,
            self.theme.button_highlight_hover_color,
            self.ICONS["keke"],
        )
        self.pbSwitchTheme = self.create_icon_button(
            self.ICONS["qiuqiu"], (50, 40), (30, 30), pbSwitchThemeStyle
        )
        self.pbSwitchTheme.clicked.connect(lambda: self.switch_theme(Form))
        self.horizontalLayout.addWidget(self.pbSwitchTheme)

        self.titleBar = DraggableTitleBar(Form)
        self.titleBar.setMinimumSize(QSize(200, 40))
        self.titleBar.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout.addWidget(self.titleBar)
        pbMinimizeStyle = self.button_title_style(
            self.theme.title_bar_color,
            self.theme.main_font,
            self.theme.button_highlight_hover_color,
            self.ICONS["minimize"],
        )
        self.pbMinimize = self.create_icon_button(
            self.ICONS["minimize"], (50, 40), (20, 20), pbMinimizeStyle
        )
        pbWindowStyle = self.button_title_style(
            self.theme.title_bar_color,
            self.theme.main_font,
            self.theme.button_highlight_hover_color,
            self.ICONS["window"],
        )
        self.pbWindow = self.create_icon_button(
            self.ICONS["window"], (50, 40), (20, 20), pbWindowStyle
        )
        pbCloseStyle = self.button_title_style(
            self.theme.title_bar_color,
            self.theme.main_font,
            self.theme.title_bar_close_color,
            self.ICONS["close"],
        )
        self.pbClose = self.create_icon_button(
            self.ICONS["close"], (50, 40), (20, 20), pbCloseStyle
        )
        self.pbMinimize.clicked.connect(Form.showMinimized)
        self.pbWindow.clicked.connect(lambda: self.toggle_maximize_restore(Form))
        self.pbClose.clicked.connect(Form.close)
        self.horizontalLayout.addWidget(self.pbMinimize)
        self.horizontalLayout.addWidget(self.pbWindow)
        self.horizontalLayout.addWidget(self.pbClose)

        self.vLayout_Main.addLayout(self.horizontalLayout)

    def setup_main_layout(self):
        """Setup main layout including side navigation and stacked widget."""
        self.gridLayout = QGridLayout()
        self.sidebar = self.create_sidebar()
        self.stackedWidget = self.create_stacked_widget()

        self.gridLayout.addWidget(self.sidebar, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.stackedWidget, 0, 1, 1, 1)

        self.vLayout_Main.addLayout(self.gridLayout)
        self.vLayout_Mainform.addLayout(self.vLayout_Main)

    def create_sidebar(self):
        """Create and return the sidebar with navigation buttons."""
        widget = QWidget()
        widget.setMinimumSize(QSize(50, 200))
        widget.setMaximumSize(QSize(50, 16777215))

        verticalLayout = QVBoxLayout(widget)
        verticalLayout.setSpacing(0)
        pbHomeStyle = self.button_sidebar_style(
            self.theme.button_sidebar_color,
            self.theme.main_font,
            self.theme.button_border_color,
            self.theme.button_sidebar_hover_color,
            self.ICONS["home_push"],
        )
        self.pbHome = self.create_icon_button(
            self.ICONS["home"], (30, 30), (20, 20), pbHomeStyle, checkable=True
        )
        pbCalculatorStyle = self.button_sidebar_style(
            self.theme.button_sidebar_color,
            self.theme.main_font,
            self.theme.button_border_color,
            self.theme.button_sidebar_hover_color,
            self.ICONS["calculator_push"],
        )
        self.pbCalculator = self.create_icon_button(
            self.ICONS["calculator"],
            (30, 30),
            (20, 20),
            pbCalculatorStyle,
            checkable=True,
        )
        pbTranslateStyle = self.button_sidebar_style(
            self.theme.button_sidebar_color,
            self.theme.main_font,
            self.theme.button_border_color,
            self.theme.button_sidebar_hover_color,
            self.ICONS["translate_push"],
        )
        self.pbTranslate = self.create_icon_button(
            self.ICONS["translate"],
            (30, 30),
            (20, 20),
            pbTranslateStyle,
            checkable=True,
        )
        pbAiChatStyle = self.button_sidebar_style(
            self.theme.button_sidebar_color,
            self.theme.main_font,
            self.theme.button_border_color,
            self.theme.button_sidebar_hover_color,
            self.ICONS["chat_push"],
        )
        self.pbAiChat = self.create_icon_button(
            self.ICONS["chat"], (30, 30), (20, 20), pbAiChatStyle, checkable=True
        )
        pbInfoStyle = self.button_sidebar_style(
            self.theme.button_sidebar_color,
            self.theme.main_font,
            self.theme.button_border_color,
            self.theme.button_sidebar_hover_color,
            self.ICONS["info_push"],
        )
        self.pbInfo = self.create_icon_button(
            self.ICONS["info"], (30, 30), (20, 20), pbInfoStyle
        )
        pbSettingStyle = self.button_sidebar_style(
            self.theme.button_sidebar_color,
            self.theme.main_font,
            self.theme.button_border_color,
            self.theme.button_sidebar_hover_color,
            self.ICONS["setting_push"],
        )
        self.pbSetting = self.create_icon_button(
            self.ICONS["setting"], (30, 30), (20, 20), pbSettingStyle
        )

        verticalLayout.addWidget(self.pbHome)
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

    def setup_button_bar(self, Form):
        self.hLayout_button = QHBoxLayout()
        self.hLayout_button.setSpacing(0)
        self.frameBottomBar = QFrame(Form)
        self.frameBottomBar.setMinimumSize(QSize(40, 20))

        self.frameBottomBar.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameBottomBar.setFrameShadow(QFrame.Shadow.Raised)

        self.hLayout_button.addWidget(self.frameBottomBar)

        self.progressBarLabel = QLabel(Form)
        self.progressBarLabel.setMinimumSize(QSize(40, 20))
        self.progressBarLabel.setMaximumSize(QSize(150, 20))

        self.progressBarLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hLayout_button.addWidget(self.progressBarLabel)

        self.progressBar = QProgressBar(Form)
        self.progressBar.setMinimumSize(QSize(200, 20))
        self.progressBar.setMaximumSize(QSize(200, 20))
        self.hLayout_button.addWidget(self.progressBar)
        self.vLayout_Main.addLayout(self.hLayout_button)

        self.vLayout_Mainform.addLayout(self.vLayout_Main)

    def setup_translate_tab(self):
        """Setup the translate tab within the translate page."""
        self.verticalLayout_2 = QVBoxLayout(self.translatePage)
        self.tabWidget = QTabWidget()
        self.tab1 = QWidget()
        self.vLayout_CstMy1 = QVBoxLayout(self.tab1)
        # *******************************************************
        # *                                                     *
        # *             自用Cst工具按钮布局                        *
        # *                                                     *
        # *******************************************************
        self.hLayout_CstMy1Button = QHBoxLayout()
        self.hLayout_CstMy1Button.setContentsMargins(0, 0, 0, 0)
        pbInportCstStructStyle = self.button_common_style(
            self.theme.button_common_color,
            self.theme.main_font,
            self.theme.button_border_color,
            self.theme.button_common_hover_color,
        )
        self.pbInportCstStruct = self.create_text_button(
            "导入结构", (60, 30), pbInportCstStructStyle
        )
        self.pbInportCstStruct.clicked.connect(self.import_structure_file)
        self.pbInportCstStruct.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.hLayout_CstMy1Button.addWidget(self.pbInportCstStruct)

        pbInportCstResultStyle = self.button_common_style(
            self.theme.button_common_color,
            self.theme.main_font,
            self.theme.button_border_color,
            self.theme.button_common_hover_color,
        )
        self.pbInportCstResult = self.create_text_button(
            "设置结果文件夹", (100, 30), pbInportCstResultStyle
        )
        self.pbInportCstResult.clicked.connect(self.import_result_folder)
        self.pbInportCstResult.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.hLayout_CstMy1Button.addWidget(self.pbInportCstResult)

        self.hLayout_CstMy1NowPlot = QHBoxLayout()
        self.hLayout_CstMy1NowPlot.setSpacing(0)
        self.labelCstNowPlot = QLabel("当前绘制：")
        self.labelCstNowPlot.setMinimumSize(QSize(70, 30))
        self.labelCstNowPlot.setMaximumSize(QSize(70, 30))

        self.hLayout_CstMy1NowPlot.addWidget(self.labelCstNowPlot)

        self.spinBoxCstNowPlot = QSpinBox(self.tab1)
        self.spinBoxCstNowPlot.valueChanged.connect(
            lambda: self.plot_data(self.spinBoxCstNowPlot.value())
        )
        self.spinBoxCstNowPlot.setEnabled(True)
        self.spinBoxCstNowPlot.setMinimumSize(QSize(100, 30))
        self.spinBoxCstNowPlot.setMaximumSize(QSize(100, 30))
        self.spinBoxCstNowPlot.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.spinBoxCstNowPlot.setReadOnly(False)
        self.spinBoxCstNowPlot.setSingleStep(2)
        self.spinBoxCstNowPlot.setStepType(QAbstractSpinBox.StepType.DefaultStepType)
        self.spinBoxCstNowPlot.setMaximum(999999)
        self.spinBoxCstNowPlot.setDisplayIntegerBase(10)

        self.hLayout_CstMy1NowPlot.addWidget(self.spinBoxCstNowPlot)

        self.hLayout_CstMy1Button.addLayout(self.hLayout_CstMy1NowPlot)

        self.horizontalLayout_CstMy1_button = QHBoxLayout()
        self.horizontalLayout_CstMy1_button.setSpacing(0)
        self.labelCstNowPlotMode = QLabel("绘制行数：")
        self.labelCstNowPlotMode.setMinimumSize(QSize(70, 30))
        self.labelCstNowPlotMode.setMaximumSize(QSize(70, 30))

        self.horizontalLayout_CstMy1_button.addWidget(self.labelCstNowPlotMode)

        self.comboBoxCstNowPlot = QComboBox(self.tab1)
        self.comboBoxCstNowPlot.addItem("1", userData=1)
        self.comboBoxCstNowPlot.addItem("2", userData=2)
        self.comboBoxCstNowPlot.addItem("3", userData=3)
        self.comboBoxCstNowPlot.addItem("4", userData=4)
        self.comboBoxCstNowPlot.setMinimumSize(QSize(50, 30))
        self.comboBoxCstNowPlot.setMaximumSize(QSize(50, 30))

        self.horizontalLayout_CstMy1_button.addWidget(self.comboBoxCstNowPlot)

        self.hLayout_CstMy1Button.addLayout(self.horizontalLayout_CstMy1_button)
        pbSaveToLMDBStyle = self.button_common_style(
            self.theme.button_highlight_color,
            self.theme.main_font,
            self.theme.button_border_color,
            self.theme.button_highlight_hover_color,
        )
        self.pbSaveToLMDB = self.create_text_button(
            "转换为LMDB数据集", (140, 30), pbSaveToLMDBStyle
        )

        self.pbSaveToLMDB.clicked.connect(self.startSaveLMDB)
        self.pbSaveToLMDB.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.hLayout_CstMy1Button.addWidget(self.pbSaveToLMDB)
        pbPlotCstStructStyle = self.button_common_style(
            self.theme.button_common_color,
            self.theme.main_font,
            self.theme.button_border_color,
            self.theme.button_common_hover_color,
        )
        self.pbPlotCstStruct = self.create_text_button(
            "重新/绘制结构", (110, 30), pbPlotCstStructStyle
        )
        self.pbPlotCstStruct.clicked.connect(lambda: self.plot_data(1))
        self.pbPlotCstStruct.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.hLayout_CstMy1Button.addWidget(self.pbPlotCstStruct)
        """Cst自用工具Matplotlib画板"""
        self.figure = Figure(figsize=(15, 5))  # 调整Figure的尺寸
        self.figure.set_facecolor(self.theme.main_color)
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
        self.cst_structure_file_path = QFileDialog.getOpenFileName(
            self, "打开参数文件", self.last_directory, "csv文件(*.csv)"
        )[0]
        self.last_directory = os.path.dirname(self.cst_structure_file_path)
        self.cst_structure_parameters = self.plot_tools.loadStructureParameters(
            self.cst_structure_file_path
        )

    def import_result_folder(self):
        self.cst_result_folder_path = QFileDialog.getExistingDirectory(
            self, "打开S参数保存文件夹", self.last_directory
        )
        self.last_directory = self.cst_result_folder_path

    def plot_data(self, num):
        if self.cst_structure_file_path == "":
            self.cst_structure_file_path = QFileDialog.getOpenFileName(
                self, "打开参数文件", self.last_directory, "csv文件(*.csv)"
            )[0]
            self.last_directory = os.path.dirname(self.cst_structure_file_path)
            self.cst_structure_parameters = self.plot_tools.loadStructureParameters(
                self.cst_structure_file_path
            )
        if self.cst_result_folder_path == "":
            self.cst_result_folder_path = QFileDialog.getExistingDirectory(
                self, "打开S参数保存文件夹", self.last_directory
            )
            self.last_directory = self.cst_result_folder_path

        # 清空Figure并绘制多个子图
        self.figure.clear()
        cmap_label = ListedColormap(["#eb9c4d", "#a8a39d", "#493736"])
        empty_patch = mpatches.Patch(color="#eb9c4d", label="Empty (0)")
        metal_patch = mpatches.Patch(color="#a8a39d", label="Aluminum (1)")
        vo2_patch = mpatches.Patch(color="#493736", label="Vanadium Dioxide (2)")
        rows = self.comboBoxCstNowPlot.currentData()
        self.spinBoxCstNowPlot.setSingleStep(rows)
        self.axes = []
        for i in range(rows):
            fre1_M, s11_M, fre2_M, s21_M, fre1_I, s11_I, fre2_I, s21_I = (
                self.plot_tools.openCstTxtPair(self.cst_result_folder_path, num + i)
            )
            matrix = self.plot_tools.plot_mirrored_matrix(
                self.cst_structure_parameters[num + i]
            )
            for k in range(3):
                ax = self.figure.add_subplot(rows, 3, i * 3 + k + 1)
                ax.set_box_aspect(0.75)
                ax.tick_params(axis="both", which="major", labelsize=10, direction="in")
                ax.set_xlabel("Frequency(THz)", fontname="Times New Roman", fontsize=12)
                if k % 3 == 0:
                    ax.plot(
                        fre1_I, self.plot_tools.calAbsorb(s11_I, s21_I), color="#962828"
                    )
                    ax.plot(
                        fre1_M, self.plot_tools.calAbsorb(s11_M, s21_M), color="#3c61b3"
                    )
                    ax.set_title(f"No.{num + i} Absorption", fontname="Times New Roman")
                    ax.legend(
                        ["介质态", "金属态"],
                        loc="upper right",
                        frameon=False,
                        fontsize="small",
                        draggable=True,
                    )
                    ax.axis([0, 2.5, 0, 1])
                elif k % 3 == 1:
                    ax.plot(
                        fre1_I,
                        self.plot_tools.calTransmission(s21_I, "linear"),
                        color="#962828",
                    )
                    ax.plot(
                        fre1_M,
                        self.plot_tools.calTransmission(s21_M, "linear"),
                        color="#3c61b3",
                    )
                    ax.legend(
                        ["介质态", "金属态"],
                        loc="upper right",
                        frameon=False,
                        fontsize="small",
                        draggable=True,
                    )
                    ax.set_title(
                        f"No.{num + i} Transmission", fontname="Times New Roman"
                    )
                elif k % 3 == 2:
                    ax.imshow(matrix, cmap=cmap_label, interpolation="nearest")
                    ax.legend(
                        handles=[empty_patch, metal_patch, vo2_patch],
                        loc="center left",  # Position it to the left
                        bbox_to_anchor=(
                            1,
                            0.5,
                        ),  # Move it outside the plot to the right
                        title="Materials",
                        prop={"family": "Times New Roman"},
                    )
                    ax.axis("off")
                    ax.set_title(f"No.{num + i} Structure", fontname="Times New Roman")
                self.axes.append(ax)
            self.figure.tight_layout()
        # 更新Canvas
        self.canvas.draw()

    def startSaveLMDB(self):
        self.progressBar.show()
        save_path = QFileDialog.getExistingDirectory(
            self, "打开数据集保存位置", self.last_directory
        )
        self.pbSaveToLMDB.setEnabled(False)
        self.worker = SaveLMDB(
            self.cst_result_folder_path, save_path, self.cst_structure_parameters
        )
        self.worker.process_signal.connect(self.progressBar.setValue)
        self.worker.finished_signal.connect(self.task_finished)
        self.worker.start()

    def task_finished(self):
        QMessageBox.information(self, "完成", "保存已完成！")
        self.progressBar.hide()
        self.pbSaveToLMDB.setEnabled(True)

    def create_message(self, text):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Info")
        msg_box.setText(text)
        return msg_box

    def button_title_style(self, background_c, font_c, hover_check_c, hover_icon=None):
        BUTTON_STYLES = f"""
            QPushButton {{
                background-color: {background_c};
                color: {font_c};
                border-radius: 0px;
            }}
            QPushButton:hover {{
                icon: url({hover_icon});
                background-color: {hover_check_c};
            }}
            QPushButton:checked {{
                icon: url({hover_icon});
                background-color: {hover_check_c};
            }}
        """
        return BUTTON_STYLES

    def button_sidebar_style(
        self, background_c, font_c, border_c, hover_check_c, hover_icon=None
    ):
        BUTTON_STYLES = f"""
            QPushButton {{
                background-color: {background_c};
                color: {font_c};
                padding: 0px;
                border: 0px solid {border_c};
                border-radius: 5px;
            }}
            QPushButton:hover {{
                icon: url({hover_icon});
                background-color: {hover_check_c};
            }}
            QPushButton:checked {{
                icon: url({hover_icon});
                background-color: {hover_check_c};
            }}
        """
        return BUTTON_STYLES

    def button_common_style(
        self, background_c, font_c, border_c, hover_check_c, hover_icon=None
    ):
        BUTTON_STYLES = f"""
            QPushButton {{
                background-color: {background_c};
                color: {font_c};
                padding: 0px;
                border: 1px solid {border_c};
                border-radius: 3px;
            }}
            QPushButton:hover {{
                icon: url({hover_icon});
                background-color: {hover_check_c};
            }}
            QPushButton:checked {{
                icon: url({hover_icon});
                background-color: {hover_check_c};
            }}
        """
        return BUTTON_STYLES

    def create_icon_button(self, icon_path, size, icon_size, style, checkable=False):
        """Create and return a QPushButton with given icon, size, style, and optional checkable flag."""
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(*icon_size))
        button.setMinimumSize(*size)
        button.setMaximumSize(*size)
        button.setStyleSheet(style)
        button.setCheckable(checkable)
        return button

    def create_text_button(self, text, size, style, checkable=False):
        """Create and return a QPushButton with given icon, size, style, and optional checkable flag."""
        button = QPushButton(text)
        button.setMinimumSize(*size)
        button.setMaximumSize(*size)
        button.setStyleSheet(style)
        button.setCheckable(checkable)
        return button

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "CocoaBall", None))

    def connect_navigation_buttons(self, callback):
        """Connect navigation buttons to the callback function."""
        self.pbHome.clicked.connect(lambda: callback(0))
        self.pbCalculator.clicked.connect(lambda: callback(1))
        self.pbTranslate.clicked.connect(lambda: callback(2))
        self.pbAiChat.clicked.connect(lambda: callback(3))

    def set_active_button(self, index):
        """Set the active button based on the page index."""
        self.pbHome.setChecked(index == 0)
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
            icon_main.addFile(
                self.ICONS["qiuqiu"], QSize(), QIcon.Mode.Normal, QIcon.State.Off
            )
            Form.setWindowIcon(icon_main)
            print(True)
            self.is_dark_mode = False
        else:
            icon_main = QIcon()
            icon_main.addFile(
                self.ICONS["keke"], QSize(), QIcon.Mode.Normal, QIcon.State.Off
            )
            Form.setWindowIcon(icon_main)
            print(False)
            self.is_dark_mode = True
        # 更新主题
        self.theme = Theme(self.is_dark_mode)

        # 重新应用主题
        self.applyTheme()

    def applyTheme(self):
        """根据当前主题应用样式"""
        self.pbHome.setStyleSheet(
            self.button_sidebar_style(
                self.theme.button_sidebar_color,
                self.theme.main_font,
                self.theme.button_border_color,
                self.theme.button_sidebar_hover_color,
                self.ICONS["home_push"],
            )
        )
        self.pbCalculator.setStyleSheet(
            self.button_sidebar_style(
                self.theme.button_sidebar_color,
                self.theme.main_font,
                self.theme.button_border_color,
                self.theme.button_sidebar_hover_color,
                self.ICONS["calculator_push"],
            )
        )
        self.pbTranslate.setStyleSheet(
            self.button_sidebar_style(
                self.theme.button_sidebar_color,
                self.theme.main_font,
                self.theme.button_border_color,
                self.theme.button_sidebar_hover_color,
                self.ICONS["translate_push"],
            )
        )
        self.pbAiChat.setStyleSheet(
            self.button_sidebar_style(
                self.theme.button_sidebar_color,
                self.theme.main_font,
                self.theme.button_border_color,
                self.theme.button_sidebar_hover_color,
                self.ICONS["chat_push"],
            )
        )
        self.pbInfo.setStyleSheet(
            self.button_sidebar_style(
                self.theme.button_sidebar_color,
                self.theme.main_font,
                self.theme.button_border_color,
                self.theme.button_sidebar_hover_color,
                self.ICONS["info_push"],
            )
        )
        self.pbSetting.setStyleSheet(
            self.button_sidebar_style(
                self.theme.button_sidebar_color,
                self.theme.main_font,
                self.theme.button_border_color,
                self.theme.button_sidebar_hover_color,
                self.ICONS["setting_push"],
            )
        )
        self.setStyleSheet(f"background-color: {self.theme.main_color};")
        self.titleBar.setStyleSheet(f"background-color: {self.theme.title_bar_color};")
        self.sidebar.setStyleSheet(f"background-color: {self.theme.sidebar_color};")
        self.stackedWidget.setStyleSheet(
            f"QStackedWidget {{background-color: {self.theme.title_bar_color}; color:{self.theme.main_font};}}"
        )
        self.frameBottomBar.setStyleSheet(
            f"""QFrame {{
                border: 0px;
                border-radius: 0px;
                background-color: {self.theme.bottom_bar_color};
        }}
        """
        )
        self.progressBarLabel.setStyleSheet(
            f"""QLabel {{
            background-color: {self.theme.bottom_bar_color};  /* 背景颜色 */
            color: {self.theme.main_font};              /* 字体颜色 */
            padding: 0px;                /* 内边距 */
            border-radius: 0px;         /* 边角半径 */
            }}
        """
        )
        self.progressBar.setStyleSheet(
            f"""
            QProgressBar {{
                border-radius: 0px;             /* 圆角半径 */
                text-align: center;              /* 文字居中 */
                background-color: {self.theme.bottom_bar_color};      /* 进度条背景色 */
                color: {self.theme.main_font};                  /* 字体颜色 */
            }}
            QProgressBar::chunk {{
                background-color: {self.theme.processbar_color};      /* 进度条块背景色 */
                border-radius: 5px;             /* 进度部分也要圆角 */
            }}
        """
        )
        self.tabWidget.setStyleSheet(
            f"""
            QTabWidget {{ 
                border: 1px solid #CCCCCC; 
                background-color: {self.theme.title_bar_color};
                color: {self.theme.main_font}; 
            }}
            QTabBar::tab {{ 
                background-color: {self.theme.title_bar_color};
                padding: 5px;
                margin: 2px;
                min-width: 80px;
                border-radius:5px;font-weight:bold; 
              }}
            QTabBar::tab:selected {{ 
                background-color: {self.theme.button_highlight_color};
                border-bottom: 2px solid {self.theme.button_highlight_hover_color}; 
             }}
            QTabWidget::pane {{ 
                border: 0px solid {self.theme.button_highlight_color}; 
                background-color: {self.theme.title_bar_color}; 
                border-radius: 5px; 
                padding:5px; 
            }}
            QTabWidget::tab-bar {{ alignment: left; }}
            QTabBar::tab::hover {{ background-color: {self.theme.button_highlight_hover_color}; }}
        """
        )
        self.pbSwitchTheme.setIcon(
            QIcon(self.ICONS["keke"] if self.is_dark_mode else self.ICONS["qiuqiu"])
        )
        self.pbSwitchTheme.setStyleSheet(
            self.button_title_style(
                self.theme.title_bar_color,
                self.theme.main_font,
                self.theme.button_theme_hover_color,
                self.ICONS["qiuqiu"] if self.is_dark_mode else self.ICONS["keke"],
            )
        )

        self.pbMinimize.setStyleSheet(
            self.button_title_style(
                self.theme.title_bar_color,
                self.theme.main_font,
                self.theme.button_highlight_hover_color,
                self.ICONS["minimize"],
            )
        )
        self.pbWindow.setStyleSheet(
            self.button_title_style(
                self.theme.title_bar_color,
                self.theme.main_font,
                self.theme.button_highlight_hover_color,
                self.ICONS["window"],
            )
        )
        self.pbClose.setStyleSheet(
            self.button_title_style(
                self.theme.title_bar_color,
                self.theme.main_font,
                self.theme.title_bar_close_color,
                self.ICONS["close"],
            )
        )
        self.figure.set_facecolor(self.theme.main_color)
        self.pbInportCstStruct.setStyleSheet(
            self.button_common_style(
                self.theme.button_common_color,
                self.theme.main_font,
                self.theme.button_border_color,
                self.theme.button_common_hover_color,
            )
        )
        self.pbInportCstResult.setStyleSheet(
            self.button_common_style(
                self.theme.button_common_color,
                self.theme.main_font,
                self.theme.button_border_color,
                self.theme.button_common_hover_color,
            )
        )
        self.pbSaveToLMDB.setStyleSheet(
            self.button_common_style(
                self.theme.button_highlight_color,
                self.theme.main_font,
                self.theme.button_border_color,
                self.theme.button_highlight_hover_color,
            )
        )
        self.pbPlotCstStruct.setStyleSheet(
            self.button_common_style(
                self.theme.button_common_color,
                self.theme.main_font,
                self.theme.button_border_color,
                self.theme.button_common_hover_color,
            )
        )
        self.labelCstNowPlot.setStyleSheet(
            f"""QLabel {{color: {self.theme.main_font};}}"""
        )
        self.labelCstNowPlotMode.setStyleSheet(
            f"""QLabel {{color: {self.theme.main_font};}}"""
        )
        self.spinBoxCstNowPlot.setStyleSheet(
            f"""
        QSpinBox {{
            font: 9pt ;              /* 字体 */
            color: {self.theme.main_font};                            /* 文本颜色 */
            background-color: {self.theme.spinbox_color};                 /* 背景颜色 */
            border: 1px solid {self.theme.spinbox_border_color};                 /* 边框 */
            border-radius: 5px;                        /* 边框圆角 */
        }}
        QSpinBox::up-button {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            background-color: {self.theme.button_common_color};                 /* 上按钮背景色 */
            border: 1px solid {self.theme.spinbox_border_color};                 /* 上按钮边框 */
            border-radius: 3px;                        /* 边框圆角 */
        }}
        
        QSpinBox::down-button {{
            subcontrol-origin: padding;
            subcontrol-position: bottom right;
            width: 20px;
            background-color: {self.theme.button_common_color};                 /* 下按钮背景色 */
            border: 1px solid {self.theme.spinbox_border_color};                 /* 下按钮边框 */
            border-radius: 3px;                        /* 边框圆角 */
        }}
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
            background-color: {self.theme.spinbox_border_color};                 /* 悬停时背景色 */
        }}
        QSpinBox:hover {{
            border: 2px solid {self.theme.spinbox_border_hover_color}; /* 悬停时边框颜色 */
        }}
        QSpinBox::up-arrow {{ 
            image: url({self.ICONS["up_arrow"]});  /* 自定义上箭头图标，可指定图标文件路径 */
            width: 7px;
            height: 7px;
        }}

        QSpinBox::down-arrow {{ 
            image: url({self.ICONS["down_arrow"]}); /* 自定义下箭头图标，可指定图标文件路径 */
            width: 7px;
            height: 7px;
        }}
        """
        )
        self.comboBoxCstNowPlot.setStyleSheet(
            f"""
        QComboBox {{
            font: 9pt ;              /* 字体 */
            color: {self.theme.combobox_font};                            /* 文本颜色 */
            background-color: {self.theme.combobox_color};                 /* 背景颜色 */
            border: 1px solid {self.theme.combobox_boder_color};                 /* 边框 */
            padding: 5px;                              /* 内边距 */
            border-radius: 3px;                        /* 边框圆角 */
        }}
        
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;            /* 下拉按钮位置 */
            width: 10px;                               /* 下拉按钮宽度 */
            border-left: 1px solid {self.theme.combobox_boder_color};           /* 左边框 */
        }}
        QComboBox::down-arrow {{
            image: url({self.ICONS["down_arrow"]});
            width: 10px;
            height: 10px;
        }}
        QComboBox::drop-down:hover {{
            background-color: {self.theme.button_highlight_hover_color};                 /* 悬停时背景色 */
        }}
        QComboBox:hover {{
            border: 2px solid {self.theme.button_highlight_hover_color}; /* 悬停时边框颜色 */
        }}
        QComboBox QAbstractItemView {{
            background-color: {self.theme.button_common_color};
            border: 1px solid {self.theme.combobox_boder_color};
            min-height: 20px;
            padding: 5px;
            scrollbar-width: 10px;
        }}
        QComboBox QAbstractItemView::item:selected {{
            background-color: {self.theme.button_highlight_hover_color};
            color: {self.theme.combobox_font};
        }}
        """
        )
        self.figure.clear()
        self.figure.set_facecolor(self.theme.main_color)
        self.canvas.draw()
