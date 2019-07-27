import copy

from rest_framework.permissions import DjangoModelPermissions


class AccurateDjangoModelPermissions(DjangoModelPermissions):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = [
            '%(app_label)s.view_%(model_name)s'
            ]
