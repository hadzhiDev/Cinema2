from rest_framework.viewsets import ModelViewSet


class SerializeByActionMixin:
    serializer_classes = {}

    def get_serializer_class(self):
        if self.action == 'partial_update' or self.action == 'update_partial':
            serializer = self.serializer_classes.get('update', None)
        else:
            serializer = self.serializer_classes.get(self.action, None)
        return serializer if serializer is not None else super().get_serializer_class()
