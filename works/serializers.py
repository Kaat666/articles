from rest_framework import serializers
from works.models import Works


class WorksResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Works
        fields = '__all__'


class WorksRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Works
        fields = '__all__'


class WorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Works
        fields = '__all__'
