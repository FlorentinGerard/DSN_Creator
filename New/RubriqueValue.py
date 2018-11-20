from New.DsnRoot import RubriqueRoot


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
