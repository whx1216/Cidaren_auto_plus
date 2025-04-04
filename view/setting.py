from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget

class Ui_Form(QWidget):
    def __init__(self, public_info):
        super(Ui_Form, self).__init__()
        # 获取用户配置
        self.public_info = public_info
        self._min_time = self.public_info.min_time
        self._max_time = self.public_info.max_time
        self._spend_min_time = self.public_info.spend_min_time
        self._spend_max_time = self.public_info.spend_max_time
        self._api_choices = self.public_info.api_choices
        # 新增配置项初始化
        self._proxy_url = self.public_info.proxy_url
        self._openai_key = self.public_info.openai_key
        self._model = self.public_info.model
        self._model_ollama = self.public_info.model_ollama
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 400)  # 增加高度以适应新的选项卡
        self.tabWidget = QtWidgets.QTabWidget(parent=Form)
        self.tabWidget.setGeometry(QtCore.QRect(20, 20, 361, 320))  # 增加高度
        self.tabWidget.setObjectName("tabWidget")

        # Tab 1 - 刷题设置
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.groupBox = QtWidgets.QGroupBox(parent=self.tab_1)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 331, 121))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 311, 92))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.label.setCursor(QCursor(Qt.CursorShape.WhatsThisCursor))
        self.label.setToolTip("设置每一道题之间提交的最短间隔")
        self.verticalLayout.addWidget(self.label)
        self.min_time = QtWidgets.QSpinBox(parent=self.verticalLayoutWidget)
        self.min_time.setObjectName("min_time")
        self.verticalLayout.addWidget(self.min_time)
        self.label_2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.label_2.setCursor(QCursor(Qt.CursorShape.WhatsThisCursor))
        self.label_2.setToolTip("设置每一道题之间提交的最长间隔")
        self.verticalLayout.addWidget(self.label_2)
        self.max_time = QtWidgets.QSpinBox(parent=self.verticalLayoutWidget)
        self.max_time.setObjectName("max_time")
        self.verticalLayout.addWidget(self.max_time)
        self.tabWidget.addTab(self.tab_1, "")

        # Tab 2 - 高级设置
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setEnabled(True)
        self.tab_2.setObjectName("tab_2")

        # 答题用时 GroupBox
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 10, 331, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(parent=self.groupBox_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 311, 92))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.label_4.setCursor(QCursor(Qt.CursorShape.WhatsThisCursor))
        self.label_4.setToolTip("设置每一题提交后台显示的最短答题用时")
        self.verticalLayout_2.addWidget(self.label_4)
        self.min_time_2 = QtWidgets.QSpinBox(parent=self.verticalLayoutWidget_2)
        self.min_time_2.setObjectName("min_time_2")
        self.verticalLayout_2.addWidget(self.min_time_2)
        self.label_5 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.label_5.setCursor(QCursor(Qt.CursorShape.WhatsThisCursor))
        self.label_5.setToolTip("设置每一题提交后台显示的最长答题用时")
        self.verticalLayout_2.addWidget(self.label_5)
        self.max_time_2 = QtWidgets.QSpinBox(parent=self.verticalLayoutWidget_2)
        self.max_time_2.setObjectName("max_time_2")
        self.verticalLayout_2.addWidget(self.max_time_2)

        # 模型选择 GroupBox
        self.groupBox_3 = QtWidgets.QGroupBox(parent=self.tab_2)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 140, 331, 71))
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.groupBox_3)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 19, 311, 45))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.api_choices = QtWidgets.QComboBox(parent=self.verticalLayoutWidget_3)
        self.api_choices.setObjectName("comboBox")
        self.api_choices.addItem("官方api接口")
        self.api_choices.addItem("本地模型")
        self.verticalLayout_3.addWidget(self.api_choices)
        self.tabWidget.addTab(self.tab_2, "")

        # Tab 3 - API设置
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")

        # API设置 GroupBox
        self.groupBox_4 = QtWidgets.QGroupBox(parent=self.tab_3)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 10, 331, 271))
        self.groupBox_4.setObjectName("groupBox_4")

        # Proxy URL
        self.label_6 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_6.setGeometry(QtCore.QRect(10, 20, 100, 25))
        self.label_6.setObjectName("label_6")
        self.proxy_url = QtWidgets.QLineEdit(parent=self.groupBox_4)
        self.proxy_url.setGeometry(QtCore.QRect(10, 45, 311, 25))
        self.proxy_url.setObjectName("proxy_url")

        # OpenAI Key
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_7.setGeometry(QtCore.QRect(10, 80, 100, 25))
        self.label_7.setObjectName("label_7")
        self.openai_key = QtWidgets.QLineEdit(parent=self.groupBox_4)
        self.openai_key.setGeometry(QtCore.QRect(10, 105, 311, 25))
        self.openai_key.setObjectName("openai_key")
        # self.openai_key.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        # Model Name
        self.label_8 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_8.setGeometry(QtCore.QRect(10, 140, 100, 25))
        self.label_8.setObjectName("label_8")
        self.model = QtWidgets.QLineEdit(parent=self.groupBox_4)
        self.model.setGeometry(QtCore.QRect(10, 165, 311, 25))
        self.model.setObjectName("model")

        # Ollama Model
        self.label_9 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_9.setGeometry(QtCore.QRect(10, 200, 100, 25))
        self.label_9.setObjectName("label_9")
        self.model_ollama = QtWidgets.QLineEdit(parent=self.groupBox_4)
        self.model_ollama.setGeometry(QtCore.QRect(10, 225, 311, 25))
        self.model_ollama.setObjectName("model_ollama")

        self.tabWidget.addTab(self.tab_3, "")

        # 底部按钮
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(140, 360, 239, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.confirmBtn = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.confirmBtn.setObjectName("confirmBtn")
        self.horizontalLayout.addWidget(self.confirmBtn)
        self.cancelBtn = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout.addWidget(self.cancelBtn)
        self.inputBtn = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.inputBtn.setObjectName("inputBtn")
        self.horizontalLayout.addWidget(self.inputBtn)
        self.warn_info = QtWidgets.QLabel(parent=Form)
        self.warn_info.setGeometry(QtCore.QRect(30, 340, 341, 20))
        self.warn_info.setStyleSheet("color:rgb(255, 0, 0);")
        self.warn_info.setText("")
        self.warn_info.setObjectName("warn_info")

        # 点击应用事件
        self.confirmBtn.clicked.connect(self.confirm)
        # 取消点击事件
        self.cancelBtn.clicked.connect(self.cancel)
        # 确定点击事件
        self.inputBtn.clicked.connect(self.input)

        # 显示设置中的数据
        self.min_time.setValue(self._min_time)
        self.max_time.setValue(self._max_time)
        self.min_time_2.setValue(self._spend_min_time)
        self.max_time_2.setValue(self._spend_max_time)
        self.api_choices.setCurrentIndex(self._api_choices)

        # 设置新增配置项的值
        self.proxy_url.setText(self._proxy_url)
        self.openai_key.setText(self._openai_key)
        self.model.setText(self._model)
        if self._model_ollama:
            self.model_ollama.setText(self._model_ollama)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "首选项"))
        self.groupBox.setTitle(_translate("Form", "刷题间隔"))
        self.label.setText(_translate("Form", "最短间隔："))
        self.min_time.setSuffix(_translate("Form", "    秒"))
        self.label_2.setText(_translate("Form", "最长间隔："))
        self.max_time.setSuffix(_translate("Form", "    秒"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("Form", "刷题设置"))
        self.groupBox_2.setTitle(_translate("Form", "答题用时"))
        self.label_4.setText(_translate("Form", "最短用时："))
        self.min_time_2.setSuffix(_translate("Form", "    秒"))
        self.label_5.setText(_translate("Form", "最长用时："))
        self.max_time_2.setSuffix(_translate("Form", "    秒"))
        self.groupBox_3.setTitle(_translate("Form", "模型选择"))
        self.label_3.setText(_translate("Form", "词形还原"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "高级设置"))

        # 新增API设置标签
        self.groupBox_4.setTitle(_translate("Form", "API设置"))
        self.label_6.setText(_translate("Form", "代理URL："))
        self.label_7.setText(_translate("Form", "OpenAI密钥："))
        self.label_8.setText(_translate("Form", "chatGpt模型："))
        self.label_9.setText(_translate("Form", "Ollama模型："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "API设置"))

        self.confirmBtn.setText(_translate("Form", "确认"))
        self.cancelBtn.setText(_translate("Form", "取消"))
        self.inputBtn.setText(_translate("Form", "应用"))

    def confirm(self):
        self.warn_info.clear()
        if self.max_time.value() < self.min_time.value():
            self.warn_info.setText("修改失败！最长间隔不得短于最短间隔！")
        elif self.max_time_2.value() < self.min_time_2.value():
            self.warn_info.setText("设置失败！最长用时不得短于最短用时！")
        else:
            min_time = self.min_time.value()
            max_time = self.max_time.value()
            min_time_2 = self.min_time_2.value()
            max_time_2 = self.max_time_2.value()
            choices_api = self.api_choices.currentIndex()

            # 新增配置项
            proxy_url = self.proxy_url.text()
            openai_key = self.openai_key.text()
            model = self.model.text()
            model_ollama = self.model_ollama.text() if self.model_ollama.text() else None

            self.public_info.input_info(
                min_time, max_time, min_time_2, max_time_2, choices_api,
                proxy_url, openai_key, model, model_ollama
            )
            self.close()

    def cancel(self):
        self.close()

    def input(self):
        self.warn_info.clear()
        if self.max_time.value() < self.min_time.value():
            self.warn_info.setText("修改失败！最长间隔不得短于最短间隔！")
        elif self.max_time_2.value() < self.min_time_2.value():
            self.warn_info.setText("设置失败！最长用时不得短于最短用时！")
        else:
            min_time = self.min_time.value()
            max_time = self.max_time.value()
            min_time_2 = self.min_time_2.value()
            max_time_2 = self.max_time_2.value()
            choices_api = self.api_choices.currentIndex()

            # 新增配置项
            proxy_url = self.proxy_url.text()
            openai_key = self.openai_key.text()
            model = self.model.text()
            model_ollama = self.model_ollama.text() if self.model_ollama.text() else None

            self.public_info.input_info(
                min_time, max_time, min_time_2, max_time_2, choices_api,
                proxy_url, openai_key, model, model_ollama
            )