from abc import ABC, abstractmethod
from enum import Enum
from PyQt5.QtWidgets import QWidget




class DisplaySubs(Enum):
    ALL = 0
    SELECTED = 1
    NONE = 2


class DsnRoot:

    def type_(self):
        """
        return the BlockType for block object, RubriqueType for rubrique object
        """
        pass

    def conf(self):
        """
        return the BlockConf for block object (except BlockType)
        RubriqueConf for rubrique object
        type object do not have conf
        """
        pass


class BlockRoot(DsnRoot, ABC):

    @abstractmethod
    def iterate_on_list(self):
        pass

    def __iter__(self):
        return iter(self.iterate_on_list())

    def __next__(self):
        return next(self.iterate_on_list())

    def __len__(self):
        return len(self.iterate_on_list())

    def __getitem__(self, n):
        return self.iterate_on_list()[n]

    def __setitem__(self, n, value):
        self.iterate_on_list()[n] = value

    def __delitem__(self, n):
        del (self.iterate_on_list()[n])

    def __str__(self):
        return '[{0.id}] {0.name} ({0.lower_bound}, {0.upper_bound})'.format(self.type_())

    def __repr__(self):
        return (f'{type(self).__name__}(id={self.type_().id}, name={self.type_().name},' 
                f'( {self.type_().lower_bound}, {self.type_().upper_bound}))')


class RubriqueRoot(DsnRoot):

    def block(self):
        pass


class WithWidget:

    def __init__(self):
        self.widget = None
        self.layout = None

    def new_widget(self):
        self.widget = QWidget
        return self.widget

    def create_widget(self, layout):
        self.layout = layout
        self.layout.addWidget(self.widget)

    def iterate_on_list(self):
        pass

    def delete_widget(self):
        self.layout.removeWidget(self.widget)
        del self.widget

    def __delitem__(self, n):
        self.iterate_on_list()[n].delete_widget()
        del (self.iterate_on_list()[n])




