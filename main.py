import os
import sys
import json
import numpy as np
import pyqtgraph as pg
from joblib import load
from font import FontType
from collections import deque
from datetime import datetime
from svm_training import svm_train
from PyQt5.QtNetwork import QTcpSocket, QTcpServer
from data_extraction import output_psd_txt, output_judge_result
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize, QEvent, QPoint, QByteArray
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QDesktopServices, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QStackedWidget, \
    QHBoxLayout, QFileDialog, QLineEdit, QButtonGroup, QGraphicsDropShadowEffect


class MainPage(QWidget):
    def __init__(self, stacked_widget, main_window):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_window = main_window

        font = FontType()

        layout_main = QHBoxLayout()
        layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout_main)

        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        height = int(screen_size.height() * 0.8)

        pixmap_wave = QPixmap('./picture/wave.jpg')
        pixmap_wave = pixmap_wave.scaledToHeight(height)
        pixmap_logo = QPixmap("./picture/logo.png")
        pixmap_logo = pixmap_logo.scaledToHeight(100)

        painter = QPainter(pixmap_wave)
        painter.setFont(font.light(25))
        painter.setPen(QColor('white'))
        painter.drawPixmap(50, 80, pixmap_logo.width(), pixmap_logo.height(), pixmap_logo)
        painter.drawText(50, 280, "The Brain-Powered")
        painter.drawText(50, 350, "Buggy System")
        painter.end()

        label_wave = QLabel(self)
        label_wave.setPixmap(pixmap_wave)
        label_wave.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        shadow_wave = QGraphicsDropShadowEffect()
        shadow_wave.setBlurRadius(50)
        shadow_wave.setXOffset(5)
        shadow_wave.setYOffset(5)
        shadow_wave.setColor(Qt.black)
        label_wave.setGraphicsEffect(shadow_wave)

        layout_main.addWidget(label_wave)

        layout_right = QVBoxLayout()
        layout_right.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout_main.addLayout(layout_right)

        layout_sys_btn = QHBoxLayout()
        layout_sys_btn.setAlignment(Qt.AlignRight)
        layout_sys_btn.setContentsMargins(0, 0, 0, 0)
        layout_right.addLayout(layout_sys_btn)

        layout_sys_btn.addStretch(1)

        self.min_btn = QPushButton()
        self.min_btn.setIcon(QIcon("./picture/min.png"))
        self.min_btn.setIconSize(QSize(80, 60))
        self.min_btn.setStyleSheet("""
            QPushButton {
                background-color: none;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(230, 230, 230, 255);
            }
        """)
        self.max_btn = QPushButton()
        self.max_btn.setIcon(QIcon("./picture/max.png"))
        self.max_btn.setIconSize(QSize(80, 60))
        self.max_btn.setStyleSheet("""
                    QPushButton {
                        background-color: none;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: rgba(230, 230, 230, 255);
                    }
                """)
        self.btn_exit = QPushButton()
        self.btn_exit.setIcon(QIcon("./picture/del.png"))
        self.btn_exit.setIconSize(QSize(80, 60))
        self.btn_exit.setStyleSheet("""
                    QPushButton {
                        background-color: none;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: rgba(216, 30, 6, 255);
                    }
                """)
        self.btn_exit.installEventFilter(self)

        layout_sys_btn.addWidget(self.min_btn)
        layout_sys_btn.addWidget(self.max_btn)
        layout_sys_btn.addWidget(self.btn_exit)

        self.min_btn.clicked.connect(self.minimize_window)
        self.max_btn.clicked.connect(self.maximize_window)
        self.btn_exit.clicked.connect(self.close_window)

        layout_info = QVBoxLayout()
        layout_info.setContentsMargins(100, 0, 100, 100)
        layout_right.addLayout(layout_info)

        label_tittle = QLabel("Introduction")
        label_tittle.setFont(font.medium(20))
        layout_info.addWidget(label_tittle)
        label_text = QLabel("Welcome to the Smart Brain-Controlled Buggy System! Our innovative system is designed to "
                            "offer a unique method of control, allowing you to maneuver a miniature buggy not with your "
                            "hands or voice, but with your thoughts (two distinct mental states), you have "
                            "the power to command the car's motion or halt it. Dive into this immersive "
                            "experience and have fun!")
        label_text.setWordWrap(True)
        label_text.setFont(font.regular(12))
        layout_info.addWidget(label_text)
        layout_pix_logic = QHBoxLayout()
        layout_info.addLayout(layout_pix_logic)
        layout_pix_logic.setContentsMargins(0, 20, 0, 20)
        layout_pix_logic.addStretch(1)
        pixmap = QPixmap('./picture/logic.png')
        pixmap = pixmap.scaledToWidth(1200)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        layout_pix_logic.addWidget(image_label)
        layout_pix_logic.addStretch(1)

        label_text = QLabel("First, you need to do some preparatory work, including electrodes placement and software "
                            "settings. Click <i>Preparation</i> for details.")
        label_text.setWordWrap(True)
        label_text.setFont(font.regular(12))
        layout_info.addWidget(label_text)

        layout_bt1 = QHBoxLayout()
        btn_bt1 = QPushButton("  Preparation ")
        btn_bt1.setFont(font.medium(12))
        btn_bt1.setIcon(QIcon("./picture/prep.png"))
        btn_bt1.setIconSize(QSize(40, 40))
        btn_bt1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        btn_bt1.setStyleSheet("""
                    QPushButton {
                        background-color: black;
                        color: white;
                        border-radius: 40px;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: rgba(80, 80, 80, 255);
                    }
                """)
        btn_bt1.setFixedHeight(80)
        btn_bt1.setFixedWidth(300)
        layout_bt1.addStretch(1)
        layout_bt1.addWidget(btn_bt1)
        layout_bt1.addStretch(1)
        layout_info.addLayout(layout_bt1)

        label_text = QLabel("Afterwards, begin controlling the buggy, which specifically involves generating prediction "
                            "models, monitoring electroencephalograms (EEG), and decision commands. "
                            "Click <i>Measurement</i> for details.")
        label_text.setWordWrap(True)
        label_text.setFont(font.regular(12))
        layout_info.addWidget(label_text)

        layout_bt2 = QHBoxLayout()
        btn_bt2 = QPushButton(" Measurement")
        btn_bt2.setFont(font.medium(12))
        btn_bt2.setIcon(QIcon("./picture/meas.png"))
        btn_bt2.setIconSize(QSize(43, 43))
        btn_bt2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        btn_bt2.setStyleSheet("""
                            QPushButton {
                                background-color: black;
                                color: white;
                                border-radius: 40px;
                                border: none;
                            }
                            QPushButton:hover {
                                background-color: rgba(80, 80, 80, 255);
                            }
                        """)
        btn_bt2.setFixedHeight(80)
        btn_bt2.setFixedWidth(300)
        layout_bt2.addStretch(1)
        layout_bt2.addWidget(btn_bt2)
        layout_bt2.addStretch(1)
        layout_info.addLayout(layout_bt2)
        layout_info.addStretch(1)

    def maximize_window(self):
        if self.main_window.isMaximized():
            self.main_window.showNormal()
        else:
            self.main_window.showMaximized()

    def minimize_window(self):
        self.main_window.showMinimized()

    def close_window(self):
        self.main_window.close()

    def eventFilter(self, watched, event):
        if watched == self.btn_exit and event.type() == QEvent.Enter:
            self.btn_exit.setIcon(QIcon('./picture/del_h.png'))
            return True
        elif watched == self.btn_exit and event.type() == QEvent.Leave:
            self.btn_exit.setIcon(QIcon('./picture/del.png'))
            return True
        return super().eventFilter(watched, event)


class SubPage1(QWidget):
    def __init__(self, stacked_widget, main_window):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_window = main_window
        font = FontType()

        layout_main = QHBoxLayout()
        layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout_main)

        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        height = int(screen_size.height() * 0.8)

        pixmap_wave = QPixmap('./picture/black.png')
        pixmap_wave = pixmap_wave.scaledToHeight(height)
        pixmap_logo = QPixmap("./picture/logo_s.png")
        pixmap_logo = pixmap_logo.scaledToHeight(100)

        painter = QPainter(pixmap_wave)
        painter.setFont(font.semibold(22))
        painter.setPen(QColor('white'))
        painter.drawPixmap(22, 80, pixmap_logo.width(), pixmap_logo.height(), pixmap_logo)
        painter.translate(40, 200)
        painter.rotate(90)
        painter.drawText(0, 0, "Preparation")
        painter.end()

        label_wave = QLabel(self)
        label_wave.setPixmap(pixmap_wave)
        label_wave.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        shadow_wave = QGraphicsDropShadowEffect()
        shadow_wave.setBlurRadius(50)
        shadow_wave.setXOffset(5)
        shadow_wave.setYOffset(5)
        shadow_wave.setColor(Qt.black)
        label_wave.setGraphicsEffect(shadow_wave)

        layout_main.addWidget(label_wave)

        layout_text = QHBoxLayout()
        layout_text.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout_main.addLayout(layout_text)
        layout_text.setStretch(0, 1)
        layout_text.setStretch(1, 1)

        # First column
        layout_first_col = QVBoxLayout()
        layout_first_col.setContentsMargins(50, 50, 50, 0)
        layout_first_col.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout_text.addLayout(layout_first_col)

        label_1 = QLabel("Step 1")
        label_1.setFont(font.medium(20))
        layout_first_col.addWidget(label_1)

        label_1 = QLabel("Please attach the electrodes as shown below.")
        label_1.adjustSize()
        label_1.setFont(font.regular(11))
        layout_first_col.addWidget(label_1)

        label_1 = QLabel("<i>*Note: Ensure that the electrodes are in close contact with the skin.</i>")
        label_1.setFont(font.regular(11))
        layout_first_col.addWidget(label_1)

        layout_pix_place = QHBoxLayout()
        layout_first_col.addLayout(layout_pix_place)
        layout_pix_place.addStretch(1)
        pixmap = QPixmap('./picture/place.png')
        pixmap = pixmap.scaledToWidth(700)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        layout_pix_place.addWidget(image_label)
        layout_pix_place.addStretch(1)

        layout_pix_sensor = QHBoxLayout()
        layout_first_col.addLayout(layout_pix_sensor)
        layout_pix_sensor.addStretch(1)
        pixmap = QPixmap('./picture/sensor.png')
        pixmap = pixmap.scaledToWidth(500)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        layout_pix_sensor.addWidget(image_label)
        layout_pix_sensor.addStretch(1)

        label_1 = QLabel("Turn on the BITalino biosignal board, and a steady white light should be visible on it.")
        label_1.setWordWrap(True)
        label_1.setFont(font.regular(11))
        layout_first_col.addWidget(label_1)

        layout_pix_board_light = QHBoxLayout()
        layout_first_col.addLayout(layout_pix_board_light)
        layout_pix_board_light.addStretch(1)
        pixmap = QPixmap('./picture/board_light.jpg')
        pixmap = pixmap.scaledToWidth(500)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        layout_pix_board_light.addWidget(image_label)
        layout_pix_board_light.addStretch(1)
        layout_first_col.addStretch(1)

        # Second column
        layout_second_col = QVBoxLayout()
        layout_second_col.setContentsMargins(0, 50, 100, 50)
        layout_text.addLayout(layout_second_col)

        row_layout_1 = QVBoxLayout()
        layout_second_col.addLayout(row_layout_1)
        label_2 = QLabel("Step 2")
        label_2.setFont(font.medium(20))
        layout_second_col.addWidget(label_2)
        label_2 = QLabel("Please click on <i>Open</i> to select the location of the <b>OpenSignals</b> software "
                         "on your computer.")
        label_2.setWordWrap(True)
        label_2.setFont(font.regular(11))
        layout_second_col.addWidget(label_2)

        label_2 = QLabel("Click <i>Run</i> to run the software. In the settings menu, select <i>INTEGRATION</i>.")
        # label_2.setWordWrap(True)
        label_2.setFont(font.regular(11))
        layout_second_col.addWidget(label_2)

        label_2 = QLabel(
            "Check the <i>TCP/IP</i> box and set the port number to <b>5555</b>. Then, click <i>Connect</i>.")
        label_2.setWordWrap(True)
        label_2.setFont(font.regular(11))
        layout_second_col.addWidget(label_2)

        layout_pix_guide = QHBoxLayout()
        layout_second_col.addLayout(layout_pix_guide)
        layout_pix_guide.addStretch(1)
        pixmap = QPixmap('./picture/guide.png')
        pixmap = pixmap.scaledToWidth(900)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        layout_pix_guide.addWidget(image_label)
        layout_pix_guide.addStretch(1)

        label_2 = QLabel("Application directory: <i>OpenSignals.exe</i>")
        label_2.setFont(font.regular(11))
        layout_second_col.addWidget(label_2)

        row_layout_2 = QHBoxLayout()
        row_layout_2.setAlignment(Qt.AlignBottom)
        layout_second_col.addLayout(row_layout_2)

        row_layout_1_1 = QHBoxLayout()
        layout_second_col.addLayout(row_layout_1_1)

        self.path_edit = QLineEdit(self)
        current_working_directory = os.getcwd()
        current_working_directory = current_working_directory.replace("\\", "/")
        self.path_edit.setText(current_working_directory + '/app/OpenSignals (r)evolution/OpenSignals.exe')
        row_layout_1_1.addWidget(self.path_edit)
        self.btn_open = QPushButton("Open", self)
        self.btn_open.setFont(font.medium(9))
        self.btn_open.setIcon(QIcon("./picture/search.png"))
        self.btn_open.setIconSize(QSize(30, 30))
        self.btn_open.setStyleSheet("""
                                    QPushButton {
                                        background-color: black;
                                        color: white;
                                        border-radius: 30px;
                                        border: none;
                                    }
                                    QPushButton:hover {
                                        background-color: rgba(80, 80, 80, 255);
                                    }
                                """)

        self.btn_open.setFixedHeight(60)
        self.btn_open.setFixedWidth(150)
        self.btn_open.clicked.connect(self.browse_for_app)
        row_layout_1_1.addWidget(self.btn_open)

        self.btn_run = QPushButton("Run", self)
        self.btn_run.setFont(font.medium(9))
        self.btn_run.setIcon(QIcon("./picture/run.png"))
        self.btn_run.setIconSize(QSize(30, 30))
        self.btn_run.setStyleSheet("""
                                            QPushButton {
                                                background-color: #0e932e;
                                                color: white;
                                                border-radius: 30px;
                                                border: none;
                                            }
                                            QPushButton:hover {
                                                background-color: #38b957;
                                            }
                                        """)

        self.btn_run.setFixedHeight(60)
        self.btn_run.setFixedWidth(150)
        self.btn_run.clicked.connect(self.open_app)

        row_layout_1_1.addWidget(self.btn_run)

        layout_bt2 = QHBoxLayout()
        layout_bt2.addStretch(1)
        layout_bt2.setContentsMargins(0, 0, 0, 50)
        btn_bt2 = QPushButton(" Back")
        btn_bt2.setFont(font.medium(12))
        btn_bt2.setIcon(QIcon("./picture/back.png"))
        btn_bt2.setIconSize(QSize(43, 43))
        btn_bt2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        btn_bt2.setStyleSheet("""
                                    QPushButton {
                                        background-color: black;
                                        color: white;
                                        border-radius: 35px;
                                        border: none;
                                    }
                                    QPushButton:hover {
                                        background-color: rgba(80, 80, 80, 255);
                                    }
                                """)
        btn_bt2.setFixedHeight(70)
        btn_bt2.setFixedWidth(200)
        layout_bt2.addStretch(1)
        layout_bt2.addWidget(btn_bt2)
        layout_second_col.addStretch(1)
        layout_second_col.addLayout(layout_bt2)

    def browse_for_app(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an application", "",
                                                   "Executables (*.exe);;All Files (*)")
        if file_path:
            self.path_edit.setText(file_path)

    def open_app(self):
        app_path = self.path_edit.text()
        if app_path:
            QDesktopServices.openUrl(QUrl.fromLocalFile(app_path))


class SubPage2(QWidget):
    def __init__(self, stacked_widget, main_window):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_window = main_window
        self.mainstart = False
        font = FontType()

        self.server = QTcpServer(self)
        if not self.server.listen(port=12345):
            print('Failed to start server')
            sys.exit(app.exec_())

        print('Server started on port', self.server.serverPort())

        self.server.newConnection.connect(self.on_new_connection)



        # main window
        layout_main = QHBoxLayout()
        layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout_main)

        # left sidebar
        layout_main.addWidget(self.sidebar())

        # right main
        layout_right = QVBoxLayout()
        layout_main.addLayout(layout_right)
        layout_right.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout_right.setContentsMargins(60, 50, 60, 0)

        # title and start button
        layout_title = QHBoxLayout()
        layout_right.addLayout(layout_title)
        layout_title.setContentsMargins(0, 0, 0, 0)
        label_title = QLabel("EEG display and analysis")
        label_title.setFont(font.medium(20))
        layout_title.addWidget(label_title)
        layout_title.addStretch(1)
        self.start_btn = QPushButton()
        layout_title.addWidget(self.start_btn)
        self.start_btn_clicks = 0
        self.start_btn.setIcon(QIcon("./picture/start.png"))
        self.start_btn.setFixedWidth(80)
        self.start_btn.setFixedHeight(80)
        self.start_btn.setIconSize(QSize(40, 40))
        self.start_btn.setStyleSheet("""
                                                    QPushButton {
                                                        background-color: #0e932e;
                                                        border-radius: 40px;
                                                        border: none;
                                                    }
                                                    QPushButton:hover {
                                                        background-color: #5bbd73;
                                                    }
                                                """)
        self.start_btn.clicked.connect(self.toggle_send_command)
        self.clf_svm = load('./model/svm_model.joblib')
        self.scaler = load('./model/scaler.joblib')

        # graph display
        layout_graphs = QVBoxLayout()
        layout_right.addLayout(layout_graphs)
        layout_graphs.setContentsMargins(100, 30, 100, 0)
        self.freq = 100
        self.data = np.zeros(self.freq * 10)
        self.is_running = False  # is collecting data
        self.plotWidget = pg.PlotWidget()
        layout_graphs.addWidget(self.plotWidget)
        self.plotWidget.setBackground('w')
        self.plot_items = self.plotWidget.getPlotItem()
        self.plot_items.getAxis('left').setPen(color='k')
        self.plot_items.getAxis('bottom').setPen(color='k')
        self.plot_items.setLabels(left='voltage (uV)', bottom='time (s)')
        height = self.main_window.height() // 4
        self.plotWidget.setFixedHeight(int(height))  # Set graph height
        self.plotData = self.plotWidget.plot(pen=pg.mkPen(color=(255, 0, 0), width=2))
        # tcp
        self.tcpIp = '127.0.0.1'
        self.tcpPort = 5555

        # Text
        layout_ct1 = QHBoxLayout()
        layout_ct1.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout_right.addLayout(layout_ct1)
        layout_ct1_left = QVBoxLayout()
        layout_ct1_left.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout_ct1_right = QVBoxLayout()
        layout_ct1_right.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout_ct1.addLayout(layout_ct1_left)
        layout_ct1.addLayout(layout_ct1_right)
        layout_ct1.setStretch(0, 1)
        layout_ct1.setStretch(1, 1)

        layout_ct1_left.setAlignment(Qt.AlignTop)
        status_title = QLabel("Connection status")
        status_title.setFont(font.medium(15))
        layout_ct1_left.addWidget(status_title)

        layout_connection_status = QHBoxLayout()
        layout_connection_status.setContentsMargins(0, 0, 0, 0)
        layout_ct1_left.addLayout(layout_connection_status)
        layout_connection_status.addStretch(1)
        layout_connection_status.setAlignment(Qt.AlignLeft)
        pix_sensor = QPixmap("./picture/sensor_logo.png")
        pix_sensor = pix_sensor.scaledToHeight(60)
        pix_sensor_label = QLabel()
        pix_sensor_label.setPixmap(pix_sensor)
        layout_connection_status.addWidget(pix_sensor_label)
        pix_line = QPixmap("./picture/line.png")
        pix_line = pix_line.scaledToHeight(60)
        pix_line_label = QLabel()
        pix_line_label.setPixmap(pix_line)
        layout_connection_status.addWidget(pix_line_label)
        pix_link_1 = QPixmap("./picture/unlink.png")
        pix_link_1 = pix_link_1.scaledToHeight(40)
        self.pix_link_1_label = QLabel()
        self.pix_link_1_label.setPixmap(pix_link_1)
        layout_connection_status.addWidget(self.pix_link_1_label)
        pix_line_label_1 = QLabel()
        pix_line_label_1.setPixmap(pix_line)
        pix_line_label_1.setContentsMargins(0, 0, 0, 0)
        layout_connection_status.addWidget(pix_line_label_1)
        pix_laptop = QPixmap("./picture/laptop.png")
        pix_laptop = pix_laptop.scaledToHeight(60)
        pix_laptop_label = QLabel()
        pix_laptop_label.setPixmap(pix_laptop)
        layout_connection_status.addWidget(pix_laptop_label)
        pix_line_label_2 = QLabel()
        pix_line_label_2.setPixmap(pix_line)
        pix_line_label_2.setContentsMargins(0, 0, 0, 0)
        layout_connection_status.addWidget(pix_line_label_2)
        pix_link_2 = QPixmap("./picture/unlink.png")
        pix_link_2 = pix_link_2.scaledToHeight(40)
        self.pix_link_2_label = QLabel()
        self.pix_link_2_label.setPixmap(pix_link_2)
        layout_connection_status.addWidget(self.pix_link_2_label)
        pix_line_label_3 = QLabel()
        pix_line_label_3.setPixmap(pix_line)
        pix_line_label_3.setContentsMargins(0, 0, 0, 0)
        layout_connection_status.addWidget(pix_line_label_3)
        pix_buggy = QPixmap("./picture/buggy.png")
        pix_buggy = pix_buggy.scaledToHeight(60)
        pix_buggy_label = QLabel()
        pix_buggy_label.setPixmap(pix_buggy)
        layout_connection_status.addWidget(pix_buggy_label)
        layout_connection_status.addStretch(1)

        self.connection_status = QLabel("Trying to reconnect...")
        self.connection_status.setFont(font.regular(11))
        self.connection_status.setStyleSheet("color: blue")
        layout_ct1_left.addWidget(self.connection_status)

        self.received_data_label = QLabel("Received Data: None")
        self.received_data_label.setFont(font.regular(11))
        layout_ct1_left.addWidget(self.received_data_label)


        layout_model_gen = QHBoxLayout()
        layout_ct1_left.addLayout(layout_model_gen)
        layout_model_gen.setContentsMargins(0, 0, 100, 0)
        model_gen_tittle = QLabel("Model generation")
        model_gen_tittle.setFont(font.medium(15))
        layout_model_gen.addWidget(model_gen_tittle)
        layout_model_gen.addStretch(1)
        self.btn_clear_gen = QPushButton()
        self.btn_clear_gen.clicked.connect(self.clear_gen)
        self.btn_clear_gen.setIcon(QIcon("./picture/clear.png"))
        self.btn_clear_gen.setStyleSheet("border: none;")
        self.btn_clear_gen.setIconSize(QSize(60, 60))
        layout_model_gen.addWidget(self.btn_clear_gen)
        self.btn_model_gen = QPushButton()
        self.btn_model_gen.clicked.connect(self.model_gen_collection)
        self.count_btn_model_gen = 0
        self.btn_model_gen.setIcon(QIcon("./picture/model_start.png"))
        self.btn_model_gen.setStyleSheet("border: none;")
        self.btn_model_gen.setIconSize(QSize(60, 60))
        layout_model_gen.addWidget(self.btn_model_gen)

        # layout_model: collect datas of different datas
        self.opt_label = QLabel("You selected: State 1")
        self.opt_label.setFont(font.regular(11))
        layout_ct1_left.addWidget(self.opt_label)
        layout_model = QHBoxLayout()
        layout_model.setAlignment(Qt.AlignLeft)
        layout_ct1_left.addLayout(layout_model)

        self.radio1 = QPushButton("State 1")
        self.radio1.setIcon(QIcon("./picture/check.png"))
        self.radio1.setFont(font.regular(11))
        self.radio1.setIconSize(QSize(40, 40))
        self.radio1.setStyleSheet("border: none;")
        self.radio2 = QPushButton("State 2")
        self.radio2.setIcon(QIcon("./picture/uncheck.png"))
        self.radio2.setFont(font.regular(11))
        self.radio2.setIconSize(QSize(40, 40))
        self.radio2.setStyleSheet("border: none;")
        self.btnGroup = QButtonGroup()
        self.btnGroup.addButton(self.radio1)
        self.btnGroup.addButton(self.radio2)
        self.radio1.setChecked(True)
        self.state_btn_state = 1
        self.btnGroup.buttonClicked.connect(self.on_button_clicked)
        layout_model.addWidget(self.radio1)
        layout_model.addWidget(self.radio2)

        layout_start_gen = QHBoxLayout()
        layout_start_gen.addStretch(1)
        btn_start_gen = QPushButton(" Start generation")
        btn_start_gen.setFont(font.medium(12))
        btn_start_gen.setIcon(QIcon("./picture/start.png"))
        btn_start_gen.setIconSize(QSize(30, 30))
        btn_start_gen.clicked.connect(self.generate_model)
        btn_start_gen.setStyleSheet("""
                                                    QPushButton {
                                                        background-color: #e0620d;
                                                        color: white;
                                                        border-radius: 40px;
                                                        border: none;
                                                    }
                                                    QPushButton:hover {
                                                        background-color: #e29969;
                                                    }
                                                """)
        btn_start_gen.setFixedHeight(80)
        btn_start_gen.setFixedWidth(400)
        layout_start_gen.addWidget(btn_start_gen)
        layout_start_gen.addStretch(1)
        layout_ct1_left.addLayout(layout_start_gen)

        test_label = QLabel("PSD")
        test_label.setFont(font.medium(15))
        layout_ct1_right.addWidget(test_label)

        layout_ct1_right.setAlignment(Qt.AlignTop)
        layout_psd = QVBoxLayout()
        layout_psd.setAlignment(Qt.AlignTop)
        layout_psd.setContentsMargins(200, 0, 200, 0)
        layout_ct1_right.addLayout(layout_psd)

        self.plotWidget_psd = pg.PlotWidget()
        layout_psd.addWidget(self.plotWidget_psd)
        self.plotWidget_psd.setBackground('w')
        height = self.main_window.height() // 6
        self.plotWidget_psd.setFixedHeight(int(height))  # Set graph height
        self.plotItem_psd = self.plotWidget_psd.getPlotItem()
        self.plotItem_psd.getAxis('left').setPen(color='k')
        self.plotItem_psd.getAxis('bottom').setPen(color='k')
        self.x = np.arange(5)
        self.heights = np.array([1, 2, 1, 2, 1])
        self.names = ['delta', 'theta', 'alpha', 'beta', 'gamma']
        ticks = [list(zip(self.x, self.names))]
        self.plotItem_psd.getAxis('bottom').setTicks(ticks)
        colors = [QColor(25, 79, 151, 255), QColor(85, 85, 85, 255), QColor(189, 107, 8, 255), QColor(0, 104, 107, 255),
                  QColor(200, 45, 49, 255)]
        brushes = [pg.mkBrush(color) for color in colors]
        self.bars = pg.BarGraphItem(x=self.x, height=self.heights, width=1, brushes=brushes)
        self.plotItem_psd.addItem(self.bars)

        layout_label_psd_data = QHBoxLayout()
        layout_label_psd_data.addStretch(1)
        self.label_psd_data = QLabel("")
        self.label_psd_data.setFont(font.regular(11))
        layout_label_psd_data.addWidget(self.label_psd_data)
        layout_label_psd_data.addStretch(1)
        layout_ct1_right.addLayout(layout_label_psd_data)

        label_result = QLabel("Result")
        label_result.setAlignment(Qt.AlignTop)
        label_result.setFont(font.medium(15))
        layout_ct1_right.addWidget(label_result)

        self.layout_last3state = QHBoxLayout()
        self.layout_last3state.addStretch(1)
        layout_ct1_right.addLayout(self.layout_last3state)
        self.list_last3state = deque(maxlen=3)
        for _ in range(3):
            self.list_last3state.append('./picture/grey.png')
        self.pix_state1 = QPixmap(self.list_last3state[0])
        self.pix_state1 = self.pix_state1.scaledToHeight(60)
        self.label_pix_state1 = QLabel()
        self.label_pix_state1.setPixmap(self.pix_state1)
        self.layout_last3state.addWidget(self.label_pix_state1)
        self.pix_state2 = QPixmap(self.list_last3state[1])
        self.pix_state2 = self.pix_state2.scaledToHeight(60)
        self.label_pix_state2 = QLabel()
        self.label_pix_state2.setPixmap(self.pix_state2)
        self.layout_last3state.addWidget(self.label_pix_state2)
        self.pix_state3 = QPixmap(self.list_last3state[2])
        self.pix_state3 = self.pix_state3.scaledToHeight(60)
        self.label_pix_state3 = QLabel()
        self.label_pix_state3.setPixmap(self.pix_state3)
        self.layout_last3state.addWidget(self.label_pix_state3)
        self.layout_last3state.addStretch(1)

        layout_runcar = QHBoxLayout()
        layout_ct1_right.addLayout(layout_runcar)
        layout_runcar.addStretch(1)
        pix_run_buggy = QPixmap("./picture/buggy.png")
        pix_run_buggy = pix_run_buggy.scaledToHeight(120)
        label_pix_run_buggy = QLabel()
        label_pix_run_buggy.setPixmap(pix_run_buggy)
        layout_runcar.addWidget(label_pix_run_buggy)

        self.pix_run_state = QPixmap("./picture/ban.png")
        self.pix_run_state = self.pix_run_state.scaledToHeight(60)
        self.label_pix_run_state = QLabel()
        self.label_pix_run_state.setPixmap(self.pix_run_state)
        layout_runcar.addWidget(self.label_pix_run_state)
        layout_runcar.addStretch(1)

        layout_buggy_test = QHBoxLayout()
        layout_ct1_right.addLayout(layout_buggy_test)
        label_buggy_test = QLabel("Buggy test")
        layout_buggy_test.addWidget(label_buggy_test)
        label_buggy_test.setFont(font.medium(15))
        layout_buggy_test.addStretch(1)
        self.btn_gofoward = QPushButton(" Move forward", self)
        self.btn_gofoward.setFont(font.medium(9))
        self.btn_gofoward.setIcon(QIcon("./picture/gofoward.png"))
        self.btn_gofoward.setIconSize(QSize(30, 30))
        self.btn_gofoward.setStyleSheet("""
                                                    QPushButton {
                                                        background-color: black;
                                                        color: white;
                                                        border-radius: 35px;
                                                        border: none;
                                                    }
                                                    QPushButton:hover {
                                                        background-color: rgba(80, 80, 80, 255);
                                                    }
                                                """)

        self.btn_gofoward.setFixedHeight(70)
        self.btn_gofoward.setFixedWidth(240)
        self.btn_gofoward.clicked.connect(lambda: self.send_message(True))
        layout_buggy_test.addWidget(self.btn_gofoward)

        self.btn_goback = QPushButton(" Move backward", self)
        self.btn_goback.setFont(font.medium(9))
        self.btn_goback.setIcon(QIcon("./picture/goback.png"))
        self.btn_goback.setIconSize(QSize(30, 30))
        self.btn_goback.setStyleSheet("""
                                                            QPushButton {
                                                                background-color: black;
                                                                color: white;
                                                                border-radius: 35px;
                                                                border: none;
                                                            }
                                                            QPushButton:hover {
                                                                background-color: rgba(80, 80, 80, 255);
                                                            }
                                                        """)

        self.btn_goback.setFixedHeight(70)
        self.btn_goback.setFixedWidth(240)
        self.btn_goback.clicked.connect(lambda: self.send_message(False))
        layout_buggy_test.addWidget(self.btn_goback)
        layout_buggy_test.addStretch(1)


        # layout_bottom: Button "Back"
        layout_bt2 = QHBoxLayout()
        layout_bt2.setContentsMargins(0, 0, 50, 50)
        btn_bt2 = QPushButton(" Back")
        btn_bt2.setFont(font.medium(12))
        btn_bt2.setIcon(QIcon("./picture/back.png"))
        btn_bt2.setIconSize(QSize(43, 43))
        btn_bt2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        btn_bt2.setStyleSheet("""
                                            QPushButton {
                                                background-color: black;
                                                color: white;
                                                border-radius: 35px;
                                                border: none;
                                            }
                                            QPushButton:hover {
                                                background-color: rgba(80, 80, 80, 255);
                                            }
                                        """)
        btn_bt2.setFixedHeight(70)
        btn_bt2.setFixedWidth(200)
        layout_bt2.addStretch(1)
        layout_bt2.addWidget(btn_bt2)
        layout_ct1_right.addStretch(1)
        layout_ct1_right.addLayout(layout_bt2)

        layout_ct1_right.addStretch(1)

        # Timer: time interval 1s

        self.reconnect_timer = QTimer(self)
        self.reconnect_timer.timeout.connect(self.try_reconnect)
        self.reconnect_timer.timeout.connect(self.display_judge_results)
        self.reconnect_timer.setInterval(500)  # 1 seconds
        self.timer_counter = 0
        self.timer_counter_1 = 0
        self.timer_counter_main = 0
        self.reconnect_timer.start()
        # self.setLayout(layout)

        # Set up TCP client
        self.socket = QTcpSocket(self)
        self.socket.connected.connect(self.on_connected)
        self.socket.disconnected.connect(self.on_disconnected)
        self.socket.readyRead.connect(self.read_data)
        self.socket.connectToHost(self.tcpIp, self.tcpPort)

        self.reconnect_message_index = 0

        # if self.socket.state() != QTcpSocket.ConnectedState:
        #     self.reconnect_timer.start()

    def sidebar(self):

        font = FontType()

        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        height = int(screen_size.height() * 0.8)

        pixmap_wave = QPixmap('./picture/black.png')
        pixmap_wave = pixmap_wave.scaledToHeight(height)
        pixmap_logo = QPixmap("./picture/logo_s.png")
        pixmap_logo = pixmap_logo.scaledToHeight(100)

        painter = QPainter(pixmap_wave)
        painter.setFont(font.semibold(22))
        painter.setPen(QColor('white'))
        painter.drawPixmap(22, 80, pixmap_logo.width(), pixmap_logo.height(), pixmap_logo)
        painter.translate(40, 200)
        painter.rotate(90)
        painter.drawText(0, 0, "Measurement")
        painter.end()

        label_wave = QLabel(self)
        label_wave.setPixmap(pixmap_wave)
        label_wave.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        shadow_wave = QGraphicsDropShadowEffect()
        shadow_wave.setBlurRadius(50)
        shadow_wave.setXOffset(5)
        shadow_wave.setYOffset(5)
        shadow_wave.setColor(Qt.black)
        label_wave.setGraphicsEffect(shadow_wave)

        return label_wave

    def on_new_connection(self):
        self.client_socket = self.server.nextPendingConnection()
        pix_link_2 = QPixmap("./picture/link.png")
        pix_link_2 = pix_link_2.scaledToHeight(40)
        self.pix_link_2_label.setPixmap(pix_link_2)
        print('Client connected')

    def send_message(self, is_move):
        if hasattr(self, 'client_socket'):
            if is_move:
                message = b'm\n'
            else:
                message = b's\n'
            self.client_socket.write(QByteArray(message))
            print('Message sent')
            # self.client_socket.disconnectFromHost()
        else:
            print('No client connected')

    def on_connected(self):  # Action while socket is connected
        self.connection_status.setText("The sensor and the laptop have been connected.")
        self.connection_status.setStyleSheet("color: green")
        pix_link_1 = QPixmap("./picture/link.png")
        pix_link_1 = pix_link_1.scaledToHeight(40)
        self.pix_link_1_label.setPixmap(pix_link_1)
        # self.reconnect_timer.stop()

    def on_disconnected(self):  # Action while socket is disconnected
        self.connection_status.setText("Disconnected")
        self.connection_status.setStyleSheet("color: red")
        self.timer_counter = 0

    def try_reconnect(self):  # Reconnection
        if self.is_running:
            self.timer_counter_1 += 1
            self.opt_label.setText(f"{self.timer_counter_1 // 2} seconds of data have been recorded.")
        if self.socket.state() != QTcpSocket.ConnectedState:
            messages = [
                "Trying to reconnect.",
                "Trying to reconnect..",
                "Trying to reconnect..."
            ]
            self.connection_status.setText(messages[self.reconnect_message_index])
            self.reconnect_message_index = (self.reconnect_message_index + 1) % 3

            self.timer_counter += 1
            if self.timer_counter >= 3:
                if self.socket.state() != QTcpSocket.ConnectedState:
                    self.socket.connectToHost(self.tcpIp, self.tcpPort)
                self.timer_counter = 0
        else:
            self.plotData.setData(self.data)

    def read_data(self):
        data = self.socket.readAll().data().decode()

        # Update plot with new data
        data_dict = json.loads(data)
        try:
            msg = data_dict["returnData"]["88:6B:0F:96:ED:FF"]
        except KeyError:
            pass
        except TypeError:
            pass
        try:
            data_list = [sublist[-1] for sublist in msg]
            self.received_data_label.setText(f"Received Data: {data_list[:6]}")
            self.received_data_label.setWordWrap(True)
            # float_list = [round(float(s), 2) for s in data_list]

            if self.state_btn_state == 1:
                with open('./data/data_state1.txt', 'a') as file1:
                    file1.write(str(data_list))
            elif self.state_btn_state == 2:
                with open('./data/data_state2.txt', 'a') as file1:
                    file1.write(str(data_list))

            self.data = np.concatenate((self.data, data_list))[-10000:]
            # self.plotData.setData(self.data)
        except UnboundLocalError:
            pass

    def update_plot_height(self):  # Set the height of the main window
        height = self.main_window.height() / 4
        self.plotWidget.setFixedHeight(int(height))

    def toggle_send_command(self):
        if self.socket.state() == QTcpSocket.ConnectedState:
            self.start_btn_clicks += 1

            if self.start_btn_clicks % 2 == 1:
                self.clf_svm = load('./model/svm_model.joblib')
                self.scaler = load('./model/scaler.joblib')
                self.socket.write(b'start')
                self.mainstart = True
                self.start_btn.setIcon(QIcon("./picture/end.png"))
            else:
                self.socket.write(b'stop')
                self.mainstart = False
                self.start_btn.setIcon(QIcon("./picture/start.png"))

    def display_judge_results(self):
        if self.mainstart:
            self.timer_counter_main += 1
            if not self.timer_counter_main % 2:
                abs_power, result = output_judge_result(self.data, self.scaler, self.clf_svm)
                self.label_psd_data.setText(str(abs_power)[1:-1])
                self.heights = abs_power
                self.bars.setOpts(height=self.heights)
                print(result)
                if result == '1':
                    self.list_last3state.append('./picture/green.png')
                elif result == '0':
                    self.list_last3state.append('./picture/red.png')
            self.pix_state1 = QPixmap(self.list_last3state[0])
            self.pix_state1 = self.pix_state1.scaledToHeight(60)
            self.label_pix_state1.setPixmap(self.pix_state1)
            self.pix_state2 = QPixmap(self.list_last3state[1])
            self.pix_state2 = self.pix_state2.scaledToHeight(60)
            self.label_pix_state2.setPixmap(self.pix_state2)
            self.pix_state3 = QPixmap(self.list_last3state[2])
            self.pix_state3 = self.pix_state3.scaledToHeight(60)
            self.label_pix_state3.setPixmap(self.pix_state3)
            light_count = 0
            for i in self.list_last3state:
                if i == './picture/green.png':
                    light_count += 1
                else:
                    light_count -= 1
            if light_count == 3:
                self.pix_run_state = QPixmap("./picture/go.png")
                self.pix_run_state = self.pix_run_state.scaledToHeight(60)
                self.label_pix_run_state.setPixmap(self.pix_run_state)
                self.send_message(True)
            elif light_count == -3:
                self.pix_run_state = QPixmap("./picture/ban.png")
                self.pix_run_state = self.pix_run_state.scaledToHeight(60)
                self.label_pix_run_state.setPixmap(self.pix_run_state)
                self.send_message(False)

    def model_gen_collection(self):
        if self.socket.state() == QTcpSocket.ConnectedState:
            self.count_btn_model_gen += 1

            if self.count_btn_model_gen % 2 == 1:
                self.socket.write(b'start')
                self.is_running = True
                self.btn_model_gen.setIcon(QIcon("./picture/end.png"))
            else:
                self.socket.write(b'stop')
                self.is_running = False
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                self.opt_label.setText(f"The data was recorded at {current_time} and took "
                                       f"{self.timer_counter_1 // 2} seconds.")
                self.timer_counter_1 = 0
                self.btn_model_gen.setIcon(QIcon("./picture/model_start.png"))

    def clear_gen(self):
        with open('./data/data_state1.txt', 'w') as file:
            pass
        with open('./data/data_state2.txt', 'w') as file:
            pass
        with open('./data/data_state1_cvt.txt', 'w') as file:
            pass
        with open('./data/data_state2_cvt.txt', 'w') as file:
            pass
        with open('./debug.txt', 'w') as file:
            pass
        self.opt_label.setText("All caches have been cleared.")

    def generate_model(self):
        output_psd_txt("./data/data_state1.txt")
        output_psd_txt("./data/data_state2.txt")
        self.opt_label.setText(svm_train())

    def on_button_pressed(self):
        if self.start_btn_clicks % 2 == 1:
            self.start_btn.setIcon(QIcon("./picture/end_p.png"))
        else:
            self.start_btn.setIcon(QIcon("./picture/start_p.png"))

    def on_button_released(self):
        if self.start_btn_clicks % 2 == 1:
            self.start_btn.setIcon(QIcon("./picture/end.png"))
        else:
            self.start_btn.setIcon(QIcon("./picture/start.png"))

    def back_on_button_pressed(self):
        self.back_btn.setIcon(QIcon("./picture/back_p.png"))

    def back_on_button_released(self):
        self.back_btn.setIcon(QIcon("./picture/back.png"))

    def on_button_clicked(self, button):
        self.opt_label.setText(f"You selected: {button.text()}")
        if button.text() == "State 2":
            self.state_btn_state = 2
            self.radio1.setIcon(QIcon("./picture/uncheck.png"))
            self.radio2.setIcon(QIcon("./picture/check.png"))
        else:
            self.state_btn_state = 1
            self.radio1.setIcon(QIcon("./picture/check.png"))
            self.radio2.setIcon(QIcon("./picture/uncheck.png"))


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("Brain powered buggy design")
        # self.setWindowIcon(QIcon('./picture/logo_0.png'))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.stacked_widget = QStackedWidget(self)

        self.setStyleSheet("""
                    QMainWindow {
                        border: 2px solid black;
                    }
                """)

        screen = QApplication.primaryScreen()
        screen_size = screen.size()

        width = int(screen_size.width() * 0.8)
        height = int(screen_size.height() * 0.8)
        self.resize(width, height)

        main_page = MainPage(self.stacked_widget, self)
        self.stacked_widget.addWidget(main_page)

        sub_page1 = SubPage1(self.stacked_widget, self)
        self.stacked_widget.addWidget(sub_page1)

        sub_page2 = SubPage2(self.stacked_widget, self)
        self.stacked_widget.addWidget(sub_page2)

        self.setCentralWidget(self.stacked_widget)

        self.m_drag = False
        self.m_DragPosition = QPoint()

    # for dragging to move window
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.m_drag:
                self.move(event.globalPos() - self.m_DragPosition)
                event.accept()

    def mouseReleaseEvent(self, event):
        self.m_drag = False


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # white bg
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))  # RGB for white
    app.setPalette(palette)

    window = AppWindow()
    window.show()
    sys.exit(app.exec_())
