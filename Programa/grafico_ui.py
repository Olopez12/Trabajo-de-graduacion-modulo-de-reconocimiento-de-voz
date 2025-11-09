# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GraficoXFxZxO.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QMenuBar, QPushButton, QRadioButton, QSizePolicy,
    QStatusBar, QTabWidget, QTextBrowser, QWidget)
import recursos_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(966, 559)
        MainWindow.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"QWidget { background:#2c673b; color: #c5e3d1; }\n"
"\n"
"#cardMoistTemp {\n"
"    background: #2c673b;\n"
"    border: 3px solid #c5e3d1;     /* dorado */\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"#cardMoistTemp2 {\n"
"    background: #2c673b;\n"
"    border: 3px solid #c5e3d1;     /* dorado */\n"
"    border-radius: 8px;\n"
"}\n"
"#cardMoistTemp3 {\n"
"    background: #2c673b;\n"
"    border: 3px solid #c5e3d1;     /* dorado */\n"
"    border-radius: 8px;\n"
"}")
        MainWindow.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(490, 250, 461, 251))
        self.textBrowser.setStyleSheet(u"QTextBrowser  {\n"
"    background: #ffffff;\n"
"    border: 3px solid #c5e3d1;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #231a09;                /* texto negro c\u00e1lido */\n"
"}")
        self.textBrowser.setFrameShape(QFrame.Shape.StyledPanel)
        self.cardMoistTemp = QFrame(self.centralwidget)
        self.cardMoistTemp.setObjectName(u"cardMoistTemp")
        self.cardMoistTemp.setGeometry(QRect(20, 10, 241, 161))
        self.cardMoistTemp.setFrameShape(QFrame.Shape.StyledPanel)
        self.cardMoistTemp.setFrameShadow(QFrame.Shadow.Raised)
        self.cardMoistTemp.setMidLineWidth(1)
        self.pushButton_2 = QPushButton(self.cardMoistTemp)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(20, 50, 201, 41))
        palette = QPalette()
        brush = QBrush(QColor(30, 26, 17, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(236, 255, 243, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        brush2 = QBrush(QColor(30, 26, 17, 128))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush2)
#endif
        self.pushButton_2.setPalette(palette)
        self.pushButton_2.setCursor(QCursor(Qt.CursorShape.UpArrowCursor))
        self.pushButton_2.setAutoFillBackground(False)
        self.pushButton_2.setStyleSheet(u"QPushButton {\n"
"    background-color: #ecfff3;   /* beige claro */\n"
"    color: #1E1A11;              /* texto negro c\u00e1lido */\n"
"    border: 2px solid #c5e3d1;   /* dorado medio */\n"
"    border-radius: 8px;\n"
"    padding: 6px 12px;\n"
"    \n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #FCEFD8;\n"
"    border: 2px solid #F6B21A;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #EBD4A3;\n"
"    border: 2px solid #B8860B;\n"
"}\n"
"")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AudioInputMicrophone))
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setFlat(False)
        self.pushButton_4 = QPushButton(self.cardMoistTemp)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(20, 100, 201, 41))
        self.pushButton_4.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        self.pushButton_4.setStyleSheet(u"\n"
"QPushButton {\n"
"    background-color: #ecfff3;   /* beige claro */\n"
"    color: #1E1A11;              /* texto negro c\u00e1lido */\n"
"    border: 2px solid #c5e3d1;   /* dorado medio */\n"
"    border-radius: 8px;\n"
"    padding: 6px 12px;\n"
"    \n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #FCEFD8;\n"
"    border: 2px solid #F6B21A;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #EBD4A3;\n"
"    border: 2px solid #B8860B;\n"
"}\n"
"")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.SystemReboot))
        self.pushButton_4.setIcon(icon1)
        self.label = QLabel(self.cardMoistTemp)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 221, 31))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"PanRoman"])
        font.setPointSize(10)
        font.setWeight(QFont.DemiBold)
        self.label.setFont(font)
        self.label.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #7cb58a;           /* amarillo s\u00f3lido */\n"
"    color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"    font-weight: 600;\n"
"    padding: 6px 8px;\n"
"    border-radius: 6px;\n"
"}")
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(False)
        self.cardMoistTemp2 = QFrame(self.centralwidget)
        self.cardMoistTemp2.setObjectName(u"cardMoistTemp2")
        self.cardMoistTemp2.setGeometry(QRect(280, 10, 191, 161))
        self.cardMoistTemp2.setFrameShape(QFrame.Shape.StyledPanel)
        self.cardMoistTemp2.setFrameShadow(QFrame.Shadow.Raised)
        self.label_8 = QLabel(self.cardMoistTemp2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 10, 171, 31))
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #7cb58a;           /* amarillo s\u00f3lido */\n"
"    color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"    font-weight: 600;\n"
"    padding: 6px 8px;\n"
"    border-radius: 6px;\n"
"}")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Absoluto = QRadioButton(self.cardMoistTemp2)
        self.Absoluto.setObjectName(u"Absoluto")
        self.Absoluto.setGeometry(QRect(40, 70, 71, 20))
        self.radioButton_2 = QRadioButton(self.cardMoistTemp2)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(40, 110, 71, 20))
        self.cardMoistTemp3 = QFrame(self.centralwidget)
        self.cardMoistTemp3.setObjectName(u"cardMoistTemp3")
        self.cardMoistTemp3.setGeometry(QRect(20, 190, 451, 311))
        self.cardMoistTemp3.setFrameShape(QFrame.Shape.StyledPanel)
        self.cardMoistTemp3.setFrameShadow(QFrame.Shadow.Raised)
        self.junta1 = QLabel(self.cardMoistTemp3)
        self.junta1.setObjectName(u"junta1")
        self.junta1.setGeometry(QRect(10, 60, 121, 31))
        font1 = QFont()
        font1.setFamilies([u"Swis721 BlkCn BT"])
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setItalic(True)
        self.junta1.setFont(font1)
        self.junta1.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.junta1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.junta3 = QLabel(self.cardMoistTemp3)
        self.junta3.setObjectName(u"junta3")
        self.junta3.setGeometry(QRect(10, 140, 121, 31))
        self.junta3.setFont(font1)
        self.junta3.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.junta3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_6 = QLabel(self.cardMoistTemp3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(270, 220, 171, 31))
        font2 = QFont()
        font2.setFamilies([u"Swis721 BlkCn BT"])
        font2.setPointSize(10)
        font2.setBold(True)
        self.label_6.setFont(font2)
        self.label_6.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.junta6 = QLabel(self.cardMoistTemp3)
        self.junta6.setObjectName(u"junta6")
        self.junta6.setGeometry(QRect(10, 260, 121, 31))
        self.junta6.setFont(font1)
        self.junta6.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.junta6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4 = QLabel(self.cardMoistTemp3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(270, 140, 171, 31))
        self.label_4.setFont(font2)
        self.label_4.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3 = QLabel(self.cardMoistTemp3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(270, 100, 171, 31))
        self.label_3.setFont(font2)
        self.label_3.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_7 = QLabel(self.cardMoistTemp3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(270, 260, 171, 31))
        self.label_7.setFont(font2)
        self.label_7.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ValorJ4 = QLabel(self.cardMoistTemp3)
        self.ValorJ4.setObjectName(u"ValorJ4")
        self.ValorJ4.setGeometry(QRect(140, 180, 121, 31))
        self.ValorJ4.setFont(font2)
        self.ValorJ4.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.ValorJ4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ValorJ1 = QLabel(self.cardMoistTemp3)
        self.ValorJ1.setObjectName(u"ValorJ1")
        self.ValorJ1.setGeometry(QRect(140, 60, 121, 31))
        font3 = QFont()
        font3.setFamilies([u"Swis721 BlkCn BT"])
        font3.setPointSize(10)
        font3.setBold(True)
        font3.setUnderline(False)
        self.ValorJ1.setFont(font3)
        self.ValorJ1.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.ValorJ1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.junta4 = QLabel(self.cardMoistTemp3)
        self.junta4.setObjectName(u"junta4")
        self.junta4.setGeometry(QRect(10, 180, 121, 31))
        self.junta4.setFont(font1)
        self.junta4.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.junta4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ValorJ2 = QLabel(self.cardMoistTemp3)
        self.ValorJ2.setObjectName(u"ValorJ2")
        self.ValorJ2.setGeometry(QRect(140, 100, 121, 31))
        self.ValorJ2.setFont(font2)
        self.ValorJ2.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.ValorJ2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ValorJ3 = QLabel(self.cardMoistTemp3)
        self.ValorJ3.setObjectName(u"ValorJ3")
        self.ValorJ3.setGeometry(QRect(140, 140, 121, 31))
        self.ValorJ3.setFont(font2)
        self.ValorJ3.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.ValorJ3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_5 = QLabel(self.cardMoistTemp3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(270, 180, 171, 31))
        self.label_5.setFont(font2)
        self.label_5.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.junta5 = QLabel(self.cardMoistTemp3)
        self.junta5.setObjectName(u"junta5")
        self.junta5.setGeometry(QRect(10, 220, 121, 31))
        self.junta5.setFont(font1)
        self.junta5.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.junta5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2 = QLabel(self.cardMoistTemp3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(270, 60, 171, 31))
        self.label_2.setFont(font2)
        self.label_2.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.junta2 = QLabel(self.cardMoistTemp3)
        self.junta2.setObjectName(u"junta2")
        self.junta2.setGeometry(QRect(10, 100, 121, 31))
        self.junta2.setFont(font1)
        self.junta2.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.junta2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ValorJ5 = QLabel(self.cardMoistTemp3)
        self.ValorJ5.setObjectName(u"ValorJ5")
        self.ValorJ5.setGeometry(QRect(140, 220, 121, 31))
        self.ValorJ5.setFont(font2)
        self.ValorJ5.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.ValorJ5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ValorJ6 = QLabel(self.cardMoistTemp3)
        self.ValorJ6.setObjectName(u"ValorJ6")
        self.ValorJ6.setGeometry(QRect(140, 260, 121, 31))
        self.ValorJ6.setFont(font2)
        self.ValorJ6.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #2c673b;\n"
"    border: 2px solid #7cb58a;     /* dorado */\n"
"    border-radius: 8px;\n"
"	color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"}")
        self.ValorJ6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_9 = QLabel(self.cardMoistTemp3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 10, 431, 31))
        self.label_9.setFont(font)
        self.label_9.setStyleSheet(u"/* Encabezado amarillo \u201cfull\u201d con texto negro */\n"
"QLabel {\n"
"    background: #7cb58a;          /* amarillo s\u00f3lido */\n"
"    color: #FFFFFF;                /* texto negro c\u00e1lido */\n"
"    font-weight: 600;\n"
"    padding: 6px 8px;\n"
"    border-radius: 6px;\n"
"}")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 966, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.pushButton_2.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"  Encender", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"   Reiniciar Posici\u00f3n", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Botones de inicio", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Modos de trabajo", None))
        self.Absoluto.setText(QCoreApplication.translate("MainWindow", u"Absoluto", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"Relativo", None))
        self.junta1.setText(QCoreApplication.translate("MainWindow", u"Junta 1", None))
        self.junta3.setText(QCoreApplication.translate("MainWindow", u"Junta 3", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"[Max Min] : [-120.0, 120.0]", None))
        self.junta6.setText(QCoreApplication.translate("MainWindow", u"Junta 6", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"[Max Min] : [0.0, 150.0]", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"[Max Min] : [-120.0, 0.0]", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"[Max Min] : [-160.0, 160.0]", None))
        self.ValorJ4.setText("")
        self.ValorJ1.setText("")
        self.junta4.setText(QCoreApplication.translate("MainWindow", u"Junta 4", None))
        self.ValorJ2.setText("")
        self.ValorJ3.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"[Max Min] : [-135.0, 135.0]", None))
        self.junta5.setText(QCoreApplication.translate("MainWindow", u"Junta 5", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"[Max Min] : [-150.0, 150.0]", None))
        self.junta2.setText(QCoreApplication.translate("MainWindow", u"Junta 2", None))
        self.ValorJ5.setText("")
        self.ValorJ6.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Posiciones del MyCobot280 M5 ", None))
    # retranslateUi


