from rest_framework import serializers
from base.models import Room
from base.dtos import RoomDTO
from base.services import RoomService

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def create(self, validated_data):
        room_dto = RoomDTO(**validated_data)
        return RoomService.create_room(room_dto)
    
    def update(self, instance, validated_data):
        room_dto = RoomDTO(**validated_data)
        return RoomService.update_room(instance, room_dto)
