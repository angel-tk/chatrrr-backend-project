from dataclasses import dataclass

@dataclass
class RoomDTO:
    def __init__(self, host, topic, name, description):
        self.host = host
        self.topic = topic
        self.name = name
        self.description = description

    @property
    def host_id(self):
        return self.host.id if self.host else None

    @property
    def topic_id(self):
        return self.topic.id if self.topic else None