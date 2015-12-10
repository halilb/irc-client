class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError


class Types:
    originTypes = Enum(["SERVER", "LOCAL"])
    responseTypes = Enum(["NEW_LOGIN", "REJECTED", "PRIVATE_MES_FAILED"])
