from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QUrl
from PyQt6.QtWidgets import QFileDialog
import os


class Backend(QObject):
    textChanged = pyqtSignal(str)
    headerChanged = pyqtSignal(str)
    filePathChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._currentText = ""
        self._currentHeader = "Note"
        self._currentFilePath = ""
        self._noteCounter = 1

    @pyqtProperty(str, notify=textChanged)
    def currentText(self):
        return self._currentText

    @currentText.setter
    def currentText(self, value):
        if value != self._currentText:
            self._currentText = value
            self.textChanged.emit(self._currentText)

    @pyqtProperty(str, notify=headerChanged)
    def currentHeader(self):
        return self._currentHeader

    @currentHeader.setter
    def currentHeader(self, value):
        if value != self._currentHeader:
            self._currentHeader = value
            self.headerChanged.emit(self._currentHeader)

    @pyqtProperty(str, notify=filePathChanged)
    def currentFilePath(self):
        return self._currentFilePath

    @currentFilePath.setter
    def currentFilePath(self, value):
        if value != self._currentFilePath:
            self._currentFilePath = value
            self.filePathChanged.emit(self._currentFilePath)

    def _getNextNoteName(self):
        name = f"Note {self._noteCounter}" if self._noteCounter > 1 else "Note"
        self._noteCounter += 1
        return name

    @pyqtSlot()
    def createFile(self):
        self.currentText = ""
        self.currentHeader = self._getNextNoteName()
        self.currentFilePath = ""

    @pyqtSlot()
    def openFileDialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Open Text File",
            "",
            "Text files (*.txt);;All files (*.*)"
        )

        if file_path:
            self.openFile(QUrl.fromLocalFile(file_path).toString())

    @pyqtSlot(str)
    def openFile(self, file_url):
        file_path = QUrl(file_url).toLocalFile()

        if not os.path.exists(file_path):
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.currentText = content

            filename = os.path.basename(file_path)
            if filename.endswith('.txt'):
                filename = filename[:-4]
            self.currentHeader = filename
            self.currentFilePath = file_path
        except Exception as e:
            print(f"Error opening file: {e}")

    @pyqtSlot()
    def saveFileDialog(self):
        default_name = self._currentHeader + ".txt"

        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Save Text File",
            default_name,
            "Text files (*.txt);;All files (*.*)"
        )

        if file_path:
            if not file_path.endswith('.txt'):
                file_path += '.txt'
            self.saveFile(QUrl.fromLocalFile(file_path).toString())

    @pyqtSlot(str)
    def saveFile(self, file_url=""):
        if file_url:
            file_path = QUrl(file_url).toLocalFile()
            self.currentFilePath = file_path
        elif not self._currentFilePath:
            default_path = self._currentHeader + ".txt"
            file_path, _ = QFileDialog.getSaveFileName(
                None,
                "Save Text File",
                default_path,
                "Text files (*.txt);;All files (*.*)"
            )

            if not file_path:
                return

            if not file_path.endswith('.txt'):
                file_path += '.txt'

            self.currentFilePath = file_path

        try:
            with open(self._currentFilePath, "w", encoding="utf-8") as f:
                f.write(self._currentText)

            filename = os.path.basename(self._currentFilePath)
            if filename.endswith('.txt'):
                filename = filename[:-4]
            self.currentHeader = filename
        except Exception as e:
            print(f"Error saving file: {e}")

    @pyqtSlot()
    def deleteFile(self):
        if self._currentFilePath and os.path.exists(self._currentFilePath):
            try:
                os.remove(self._currentFilePath)
            except Exception as e:
                print(f"Error deleting file: {e}")

        self.createFile()