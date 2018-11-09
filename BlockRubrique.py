from abc import ABC, abstractmethod
from enum import Enum

import numpy as np


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


class BlockType(BlockRoot):
    ids = {}

    def __init__(self, id, name, description='', lower_bound=1, upper_bound=1):
        self.id = id
        self.name = name
        self.full_name = name
        self.description = description
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.description = description
        self.sub_blocks = []
        self.rubriques = []
        # depth is set in append_in_parent(...)
        self.depth = 0
        BlockType.ids[id] = self

    def append(self, id, name, description='', lower_bound=1, upper_bound=1):
        sub_block = BlockType(id, name, description, lower_bound, upper_bound)
        self.sub_blocks.append(sub_block)
        return sub_block

    def iterate_on_list(self):
        return self.sub_blocks

    @classmethod
    def append_in_parent(cls, parent_id, id, name, description='', lower_bound=1, upper_bound=1):
        parent_block = cls.ids[parent_id]
        sub_block = parent_block.append(id, name, description, lower_bound, upper_bound)
        sub_block.depth = parent_block.depth + 1

    @classmethod
    def append_rubrique(cls, block_id, id, name, full_name, description, data_type_id):
        i = name.find('.')
        rubrique_name = name[i + 1:]
        name_block = name[:i]
        cls.ids[block_id].name = name_block
        cls.ids[block_id].rubriques.append(
            RubriqueType(block_id, id, rubrique_name, full_name, description, data_type_id))

    def deep_print(self, depth=0, print_rubriques=False):
        print(' ' * 8 * depth + ('' if not depth else '└─ ') + str(self))  # '├─ '
        [print(' ' * 8 * depth + '   > ' + str(r)) for r in self.rubriques if print_rubriques]
        [b.deep_print(depth + 1, print_rubriques) for b in self]

    def type_(self):
        return self


class RubriqueType(RubriqueRoot):
    ids = {}

    def __init__(self, block_id, id, name, full_name, description, data_type_id):
        self.id = id
        self.name = name
        self.full_name = full_name
        self.description = description
        self.data_type_id = data_type_id
        self.block_id = block_id
        RubriqueType.ids[block_id + str(id)] = self

    def __str__(self):
        return f"{'['+str(self.id)+']':5} {self.name:40}"

    def __repr__(self):
        return f'{type(self).__name__}(id={self.id}, name={self.name})'

    def data_type(self):
        return DataType.ids[self.data_type_id]

    def type_(self):
        return self


class DataType(DsnRoot):
    ids = {}

    def __init__(self, id, nature, regex, lg_min, lg_max, values):
        self.id = id
        self.nature = nature
        self.regex = regex
        self.lg_min, self.lg_max = lg_min, lg_max
        self.values = [tuple(v.split('=')) for v in values.split(';')] if values is not np.nan else []
        DataType.ids[id] = self


class RubriqueConf(RubriqueRoot):

    def __init__(self, rubrique_type, is_enabled_by_default=True, use_default_value=False, default_value=''):
        self.rubrique_type = rubrique_type
        self.is_enabled_by_default = is_enabled_by_default
        self.use_default_value = use_default_value
        self.default_value = default_value

    def __repr__(self):
        return f'{type(self).__name__}(id={self.rubrique_type.id}, name={self.rubrique_type.name})'

    def type_(self):
        return self.rubrique_type


class RubriqueValue(RubriqueRoot):

    def __init__(self, rubrique_conf, value='', is_enabled=None):
        self.rubrique_conf = rubrique_conf
        if is_enabled is None:
            self.is_enabled = rubrique_conf.is_enabled_by_default
        else:
            self.is_enabled = bool(is_enabled)
        if value != '':
            self.value = value
        elif rubrique_conf.use_default_value:
            self.value = rubrique_conf.default_value

    def __repr__(self):
        return f'{type(self).__name__}(id={self.rubrique_conf.rubrique.id}, name={self.rubrique_conf.rubrique.name})'

    def type_(self):
        return self.rubrique_conf.type_()


class BlockConf(BlockRoot):

    def __init__(self, block_type, is_enabled=True, display_subs=DisplaySubs.ALL, show_content=False):
        self.block_type = block_type
        self.rubriques = [RubriqueConf(r) for r in self.block_type.rubriques]
        self.sub_blocks = [BlockConf(b) for b in block_type]
        self.is_enabled = is_enabled or self.block_type.lower_bound > 0
        self.block_values = []
        self.display_subs = display_subs
        self.show_content = show_content

    def iterate_on_list(self):
        return self.sub_blocks

    def type_(self):
        return self.block_type


class BlockInstance(BlockRoot):

    def __init__(self, block_value):
        self.block_value = block_value
        self.rubriques = [RubriqueValue(r) for r in self.block_value.block_conf.rubriques]
        self.sub_blocks = [BlockValue(b, self) for b in self.block_value.block_conf]

    def iterate_on_list(self):
        return self.sub_blocks

    def type_(self):
        return self.block_value.type_()

    def name(self):
        result = self.block_value.name()
        result += ('/' if result else '') + self.type_().name
        if len(self.block_value.instances) > 1:
            result += '_' + str(self.block_value.instances.index(self) + 1)
        return result


class BlockValue(BlockRoot):

    def __init__(self, block_conf, parent_block_instance=None, number=None):
        self.block_conf = block_conf
        self.parent_block_instance = parent_block_instance
        if number is None:
            number = self.block_conf.block_type.lower_bound
            if self.block_conf.block_type.upper_bound == '*':
                number = 2
        self.block_conf.block_values.append(self)

        self.instances = [BlockInstance(self) for _ in range(number)]

    def add_instance(self):
        bi = BlockInstance(self)
        self.instances.append(bi)
        return bi

    def iterate_on_list(self):
        return self.instances

    def type_(self):
        return self.block_conf.type_()

    def name(self):
        if self.parent_block_instance:
            parent_value = self.parent_block_instance.block_value
            result = parent_value.name()

            if parent_value.parent_block_instance and parent_value.type_().upper_bound == '*':
                result += ('/' if result else '') + parent_value.type_().name + '_' + str(
                    self.parent_block_instance.block_value.instances.index(
                        self.parent_block_instance) + 1)
            return result
        return ''
