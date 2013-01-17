from PySide.QtGui import *
from PySide.QtCore import *

from app.models import language

# class ActWidget(QListView):

#     def __init__(self, parent=None):
#         super(ActWidget, self).__init__(parent)

# class ActView(QListView):

#     def __init__(self, parent=None):
#         super(ActView, self).__init__(parent)
#         # self.setAcceptDrops(True)
#         self.setDragDropMode(QAbstractItemView.InternalMove)

class ActEdit(QWidget):

    def __init__(self, parent=None):
        super(ActEdit, self).__init__(parent)
        self._scenes = [
            VideoSceneWidget(self)
        ]
        self._setupUI()

    def _setupUI(self):
        layout = QVBoxLayout()
        for scene in self._scenes:
            layout.addWidget(scene)
        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.Act
        """
        return language.Act(map(lambda x: x.model(), self._scenes))

    def mousePressEvent(self,event):
        self.changed.emit(self.model().translate())

    changed = Signal(str)


class ActWidget(QWidget):

    def __init__(self, parent=None):
        super(ActWidget, self).__init__(parent)
        self._scenes = [
            VideoSceneWidget(self)
        ]
        self._setupUI()

    def _setupUI(self):
        layout = QVBoxLayout()
        for scene in self._scenes:
            layout.addWidget(scene)
        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.Act
        """
        return language.Act(map(lambda x: x.model(), self._scenes))

class SceneWidget(QWidget):

    def __init__(self,parent=None):
        super(SceneWidget, self).__init__(parent)
        self._setupUI()

    def _setupUI(self):
        comments = CommentWidget("comments", self)
        preCommands = CommandSequenceWidget(self)
        postCommands = CommandSequenceWidget(self)

        layout = QVBoxLayout()
        layout.addWidget(comments)
        layout.addWidget(preCommands)
        layout.addWidget(postCommands)

        self.setLayout(layout)

class CommentWidget(QPlainTextEdit):

    def __init__(self, text="", parent=None):
        super(CommentWidget, self).__init__(text, parent)
        self.setLineWrapMode(QPlainTextEdit.WidgetWidth)

        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Qt.ScrollBarAsNeeded
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        fm = QFontMetrics(self.font())
        h = fm.height() * 1.6
        self.setMinimumHeight(h)

        self.setMaximumHeight(50)

class VideoSceneWidget(QWidget):

    def __init__(self,parent=None):
        super(VideoSceneWidget, self).__init__(parent)
        self._setupUI()

    def _setupUI(self):
        self._comment = CommentWidget("comment", self)
        self._comment.setMaximumHeight(50)
        self._preCommands = CommandSequenceWidget(self)
        self._postCommands = CommandSequenceWidget(self)

        videoControls = QWidget(self)
        videoControlsLayout = QGridLayout()

        self._source = VideoSlotWidget()
        self._duration = NumberSlotWidget()
        self._offset = NumberSlotWidget()
        # self._volume = NumberSlotWidget()

        videoControlsLayout.addWidget(QLabel("play"), 0, 0)
        videoControlsLayout.addWidget(self._source, 0, 1)
        videoControlsLayout.addWidget(QLabel("for"), 1, 0)
        videoControlsLayout.addWidget(self._duration, 1, 1)
        videoControlsLayout.addWidget(QLabel("from offset"), 2, 0)
        videoControlsLayout.addWidget(self._offset, 2, 1)
        # videoControlsLayout.addWidget(QLabel("at volume"), 3, 0)
        # videoControlsLayout.addWidget(self._volume, 3, 1)

        videoControls.setLayout(videoControlsLayout)

        layout = QVBoxLayout()
        layout.addWidget(self._comment)
        layout.addWidget(self._preCommands)
        layout.addWidget(videoControls)
        layout.addWidget(self._postCommands)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.VideoScene
        """
        return language.VideoScene(
            self.title(),
            self.comment(),
            self.duration(),
            self.preCommands(),
            self.postCommands(),
            self.offset(),
            self.source()
        )

    def title(self):
        before, sep, after = self._comment.toPlainText().partition("\n")
        return before

    def comment(self):
        before, sep, after = self._comment.toPlainText().partition("\n")
        return after

    def duration(self):
        return self._duration.model()

    def preCommands(self):
        return self._preCommands.model()

    def postCommands(self):
        return self._postCommands.model()

    def offset(self):
        return self._duration.model()

    def source(self):
        return self._source.model()

class CommandSequenceWidget(QWidget):

    def __init__(self, parent=None):
        super(CommandSequenceWidget, self).__init__(parent)
        self._setupUI()

    def _setupUI(self):
        layout = QVBoxLayout()
        for i in range(1,4):
            layout.addWidget(QLabel("command %s" % i, self))
        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.CommandSequence
        """
        return language.CommandSequence()

class VideoDefnWidget(QWidget):

    def __init__(self, parent=None):
        super(VideoDefnWidget, self).__init__(parent)
        self._setupUI()

    def _setupUI(self):
        self.setGeometry(QRect(60, 30, 211, 71))
        self.setStyleSheet("background:red")
        self.setObjectName("widget_3")

        self.horizontalLayout_9 = QHBoxLayout(self)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")

        self.label_4 = QLabel(self)
        self.label_4.setText("")
        
        self.label_4.setPixmap(QPixmap("res/video-64-64.png"))
        self.label_4.setObjectName("label_4")

        self.horizontalLayout_8.addWidget(self.label_4)

        self.lineEdit_2 = QLineEdit(self)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.horizontalLayout_8.addWidget(self.lineEdit_2)

        self.horizontalLayout_9.addLayout(self.horizontalLayout_8)

class VideoSlotWidget(QLabel):

    def __init__(self, parent=None):
        super(VideoSlotWidget, self).__init__(parent)
        self.setPixmap(QPixmap("res/video-64-64.png"))
        self.setStyleSheet("background: red;")

    def model(self):
        """
        :rtype: models.language.VideoExpression
        """
        return language.VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0")

class VideoCollectionDefnWidget(QWidget):

    def __init__(self, parent=None):
        super(VideoCollectionDefnWidget, self).__init__(parent)
        self._setupUI()

    def _setupUI(self):
        self.setGeometry(QRect(60, 160, 191, 71))
        self.setStyleSheet("background:red")
        self.setObjectName("widget_4")

        self.horizontalLayout_11 = QHBoxLayout(self)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")

        self.label_5 = QLabel(self)
        self.label_5.setText("")
        self.label_5.setPixmap(QPixmap("res/video-collection-64-64.png"))
        self.label_5.setObjectName("label_5")

        self.horizontalLayout_10.addWidget(self.label_5)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")

        self.horizontalLayout_10.addWidget(self.lineEdit)

        self.horizontalLayout_11.addLayout(self.horizontalLayout_10)

class GetterWidget(QWidget):

    def __init__(self, parent=None):
        super(GetterWidget, self).__init__(parent)
        self._setupUI()

    def _setupUI(self):
    
        self.setMaximumSize(QSize(16777215, 71))
        self.setStyleSheet("background:white")
        self.setObjectName("widget_2")
        self.horizontalLayout_6 = QHBoxLayout(self)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.label_2 = QLabel("get",self)
        self.label_2.setObjectName("label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.comboBox_2 = QComboBox(self)
        self.comboBox_2.setObjectName("comboBox_2")
        self.horizontalLayout_5.addWidget(self.comboBox_2)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(spacerItem)

        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)

class SetterWidget(QWidget):

    def __init__(self, parent=None):
        super(SetterWidget, self).__init__(parent)
        self._setupUI()

    def _setupUI(self):

        self.setMaximumSize(QSize(16777215, 51))
        self.setAutoFillBackground(False)
        self.setStyleSheet("background:white;")
        self.setObjectName("widget")

        self.horizontalLayout_4 = QHBoxLayout(self)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.label = QLabel("set",self)
        self.label.setObjectName("label")

        self.horizontalLayout_3.addWidget(self.label)

        self.comboBox = QComboBox(self)
        self.comboBox.setObjectName("comboBox")

        self.horizontalLayout_3.addWidget(self.comboBox)

        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)

class TextValueWidget(QFrame):

    def __init__(self, text, parent=None):
        super(TextValueWidget, self).__init__(parent)
        self._text = QLineEdit(text, self)
        layout = QHBoxLayout()
        layout.addWidget(QLabel("\"", self))
        layout.addWidget(self._text)
        layout.addWidget(QLabel("\"", self))
        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.TextValue
        """
        return language.TextValue(self._text.text())

class NumberValueWidget(QFrame):

    def __init__(self, number, parent=None):
        super(NumberValueWidget, self).__init__(parent)
        self._number = QLineEdit(str(number), self)
        self._number.setValidator(QDoubleValidator())
        layout = QHBoxLayout()
        layout.addWidget(self._number)
        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.NumberValue
        """
        return language.NumberValue(float(self._number.text()))

class SlotWidget(QLabel):

    def __init__(self, parent=None):
        super(SlotWidget, self).__init__(parent)
        self.setFixedSize(QSize(50,50))

class NumberSlotWidget(SlotWidget):

    def __init__(self, parent=None):
        super(NumberSlotWidget, self).__init__(parent)
        self.setText("number")
        self.setStyleSheet("background: blue")

    def model(self):
        """
        :rtype: models.language.NumberExpression
        """
        return language.NumberValue(15)

class TextSlotWidget(SlotWidget):

    def __init__(self, parent=None):
        self.setText("text")
        super(TextSlotWidget, self).__init__(parent)
        self.setStyleSheet("background: green")