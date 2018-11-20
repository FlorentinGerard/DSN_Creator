from New.DsnRoot import BlockRoot
from New.BlockInstance import BlockInstance


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
