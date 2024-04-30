from rest_framework import serializers


class Conversion(serializers.Serializer):
    base_currency = serializers.CharField(max_length=3)
    data = serializers.DictField()
