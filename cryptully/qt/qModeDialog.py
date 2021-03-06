import os
import signal

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QVBoxLayout

from qLinkLabel import QLinkLabel
from qModeButton import QModeButton
import qtUtils

from utils import constants
from utils import utils

class QModeDialog(QDialog):
    def __init__(self, isLightTheme):
        QDialog.__init__(self)

        self.mode = None

        # Set the title and icon
        self.setWindowTitle("Cryptully")
        self.setWindowIcon(QIcon(utils.getAbsoluteResourcePath('images/' + ('light' if isLightTheme else 'dark') + '/icon.png')))

        clientButton = QModeButton("Connect to friend", utils.getAbsoluteResourcePath('images/client.png'), lambda: self.modeSelected(constants.MODE_CLIENT), 150, self)
        serverButton = QModeButton("Wait for connection", utils.getAbsoluteResourcePath('images/server.png'), lambda: self.modeSelected(constants.MODE_SERVER), 150, self)

        helpLink = QLinkLabel("Confused? Read the docs.", "https://cryptully.readthedocs.org/en/latest/", self)

        # Center the buttons horizontally
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(clientButton)
        hbox.addSpacing(45)
        hbox.addWidget(serverButton)
        hbox.addStretch(1)

        # Add the help link to the bottom left corner
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(helpLink)

        self.setLayout(vbox)

        qtUtils.resizeWindow(self, 500, 200)
        qtUtils.centerWindow(self)


    def modeSelected(self, mode):
        self.mode = mode
        self.close()


    @staticmethod
    def getMode(isLightTheme):
        modeDialog = QModeDialog(isLightTheme)
        modeDialog.exec_()
        return modeDialog.mode
