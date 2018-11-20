from New.DsnRoot import BlockRoot, DisplaySubs
from New.RubriqueConf import RubriqueConf


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
