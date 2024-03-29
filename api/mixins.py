from rest_framework.viewsets import ModelViewSet


class SerializeByActionMixin:
    serializer_classes = {}
    def get_serializer_class(self):
        # print(self.serializer_classes)
        if self.action == 'partial_update' or self.action == 'update_partial':
            serializer = self.serializer_classes.get('update', None)
        else:
            serializer = self.serializer_classes.get(self.action, None)
        return serializer if serializer is not None else super().get_serializer_class()

class PermissionByActionMixin:
    permission_classes_by_action = {}

    def get_permissions(self):
        permission_classes = self.permission_classes_by_action.get(self.action, None)
        print(permission_classes)
        if self.action == 'partial_update' or self.action == 'update_partial':
            permission_classes = self.permission_classes_by_action.get('update', None)
        if permission_classes is None:
            return super().get_permissions()
        return [permission() for permission in permission_classes]


class UltraModelViewSet(
    PermissionByActionMixin,
    SerializeByActionMixin,
    ModelViewSet,
):
    pass