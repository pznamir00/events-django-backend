from .BaseDriver import BaseDriver


class VintedDriver(BaseDriver):
    @staticmethod
    def get_required_fields():
        return ['email', 'password']