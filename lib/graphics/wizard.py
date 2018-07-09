from PyQt5.QtWidgets import (QMainWindow, QLayout, QPushButton, QHBoxLayout, QMessageBox, QLabel, QFileDialog)
from PyQt5 import QtWidgets
from ..services.bendcomm import *


class QIComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(QIComboBox, self).__init__(parent)


class ImportWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(ImportWizard, self).__init__(parent)
        self.addPage(Page1(self))
        self.addPage(Page2(self))
        self.setWindowTitle("Import Wizard")
        # Trigger close event when pressing Finish button to redirect variables to backend
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.onFinished)
        self.variable = None

    def onFinished(self):
        print("Finish")
        # Return variables to use in main
        print(self.variable)
        Communicator.send_paths(self.variable)


class Page1(QtWidgets.QWizardPage):

    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.comboBox = QIComboBox(self)
        self.comboBox.addItem("Python", "/path/to/filename1")
        self.comboBox.addItem("PyQt5", "/path/to/filename2")
        self.openFileBtn = QPushButton("Import Edge List")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.comboBox)
        layout.addWidget(self.openFileBtn)
        self.setLayout(layout)
        self.openFileBtn.clicked.connect(self.openFileNameDialog)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;Python Files (*.py)", options=options)
        # if user selected a file store its path to a variable
        if fileName:
            self.wizard().variable = fileName


class Page2(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.label1 = QtWidgets.QLabel()
        self.label2 = QtWidgets.QLabel()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        self.setLayout(layout)

    def initializePage(self):
        self.label1.setText("Example text")
        self.label2.setText("Example text")


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wizard = ImportWizard()
    wizard.show()
    sys.exit(app.exec_())