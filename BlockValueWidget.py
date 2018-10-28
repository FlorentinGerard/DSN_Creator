from PyQt5.QtWidgets import *

class BlockValueFrame(QFrame):

    def __init__(self, block):
        self.instances = []

        super().__init__()
        self.block = block

        self.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.setLineWidth(2)

        ''' 
        # Create main label of the frame
        self.main_label = QLabel()
        self.main_label.setText(str(block))
        self.main_label.setMaximumWidth(400)
        '''
        '''
        # Layout for the frame
        self.frameLayout = QHBoxLayout()
        self.frameLayout.addWidget(self.front_check_box)
        self.frameLayout.addWidget(self.main_label)
        self.frame.setLayout(self.frameLayout)
        self.frameLayout.setContentsMargins(5, 5, 5, 5)
        '''

        # Layout of the widget
        self.layout = QVBoxLayout()
        #self.layout.setContentsMargins(10, 10, 10, 10)

        for bi in self.block.instances:
            bci = BlockConfInstance(bi)
            self.instances.append(bci)
            self.layout.addWidget(bci)

        self.setLayout(self.layout)


class BlockConfInstance(QFrame):

    def __init__(self, block):

        super().__init__()
        self.block = block

        self.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.setLineWidth(1)
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setText(str(block))
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
