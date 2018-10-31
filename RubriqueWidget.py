from PyQt5.QtWidgets import *


class RubriqueValueFrame(QWidget):

    def __init__(self, rubrique, grid_layout, vertical_rank):

        super().__init__()
        self.rubrique = rubrique

        #self.setFrameStyle(QFrame.Panel | QFrame.Plain)
        #self.setLineWidth(1)
        #self.layout = QHBoxLayout()
        #self.layout.setContentsMargins(2, 2, 2, 2)

        self.check_box = QCheckBox()
        self.name_label = QLabel()
        self.name_label.setText(str(rubrique.type_().id) + ' ' + rubrique.type_().name)
        print(type(self.rubrique.type_()))
        values = ['='.join(val)[:70] for val
                  in self.rubrique.type_().data_type().values]
        if values:
            self.value = QComboBox()
            self.value.addItems(values)
        else:
            self.value = QLineEdit()
        grid_layout.addWidget(self.check_box, vertical_rank, 0)
        grid_layout.addWidget(self.name_label, vertical_rank, 1)
        grid_layout.addWidget(self.value, vertical_rank, 2)
        #self.setLayout(self.layout)


