from base.models import Room
from .dtos import RoomDTO

class RoomService:
    @staticmethod
    def create_room(room_dto: RoomDTO) -> Room:
        room = Room(
            host_id=room_dto.host_id,
            topic_id=room_dto.topic_id,
            name=room_dto.name,
            description=room_dto.description
        )
        room.save()
        return room

    @staticmethod
    def update_room(room: Room, room_dto: RoomDTO) -> Room:
        room.name = room_dto.name
        room.description = room_dto.description
        room.topic_id = room_dto.topic_id
        room.save()
        return room
