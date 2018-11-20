from New.DsnRoot import DsnRoot, BlockRoot, RubriqueRoot
import numpy as np


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
