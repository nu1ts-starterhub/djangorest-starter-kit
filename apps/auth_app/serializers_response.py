from rest_framework import serializers

class RegisterResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class ErrorResponseSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    status = serializers.IntegerField()
    error = serializers.CharField()
    message = serializers.CharField()
    path = serializers.CharField()