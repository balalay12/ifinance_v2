from django.core.serializers.python import Serializer
from models import Categorys


class OperationsWithCategoryCollectionSerializer(Serializer):
    def end_object(self, obj):
        self._current['id'] = obj._get_pk_val()
        self._current['date'] = self._current['date'].isoformat()
        self._current['category_id'] = self._current['category']
        self._current['category'] = get_single_category(self._current['category'])
        self.objects.append(self._current)


class OperationsCollectionSerializer(Serializer):
    def end_object(self, obj):
        self._current['id'] = obj._get_pk_val()
        self._current['date'] = self._current['date'].isoformat()
        self.objects.append(self._current)


class CategorySerializer(Serializer):
    def end_object(self, obj):
        self._current['operation_type'] = self._current['operation_type']
        self._current['name'] = self._current['name']
        self.objects.append(self._current)

########################################################
def get_single_category(category_id):
    return str(Categorys.objects.get(operation_type=category_id))