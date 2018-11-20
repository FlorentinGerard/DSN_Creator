from New.DsnRoot import RubriqueRoot


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
