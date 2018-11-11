from PyQt5.QtWidgets import *
from RubriqueWidget import RubriqueValueFrame


class BlockValueFrame(QFrame):

    def __init__(self, block, conf_widget):
        self.instances = []
        super().__init__()
        self.block = block
        self.conf_widget = conf_widget
        self.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.setLineWidth(3)
        # Layout of the widget
        self.layout = QVBoxLayout()
        self.first_line_layout = QHBoxLayout()
        self.label = QLabel(text=self.block.name())

        self.new_instance = QPushButton(text='New instance')
        self.new_instance.clicked.connect(self.create_new_instance)

        self.first_line_layout.addWidget(self.label)
        self.first_line_layout.addStretch()
        self.first_line_layout.addWidget(self.new_instance)
        self.layout.addLayout(self.first_line_layout)
        for block_instance in self.block.instances:
            self.add_instance(block_instance)
        self.setLayout(self.layout)

    def create_new_instance(self):
        block_instance = self.block.add_instance()
        self.add_instance(block_instance)

    def add_instance(self, block_instance):
        instance = BlockInstanceFrame(block_instance)
        self.instances.append(instance)
        self.layout.addWidget(instance)

    def update_instances(self):
        instances_iter = iter(self.instances)
        for block_instance in self.block:
            try:
                block_instance_frame = next(instances_iter)
            except StopIteration:
                self.add_instance(block_instance)
            if block_instance != block_instance_frame.instance





class BlockInstanceFrame(QFrame):

    def __init__(self, instance):
        super().__init__()
        self.instance = instance
        self.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.setLineWidth(2)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.label = QLabel()
        self.label.setText(self.instance.name())
        self.layout.addWidget(self.label)
        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(5)
        for row, rubrique in enumerate(self.instance.rubriques):
            RubriqueValueFrame(rubrique, self.grid_layout, row)
        self.layout.addSpacing(10)
        self.layout.addLayout(self.grid_layout)
        self.setLayout(self.layout)
