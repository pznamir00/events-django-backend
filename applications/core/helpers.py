import uuid


class EventFileNameGenerator:
    @staticmethod
    def generate(_, filename: str):
        extension = filename.split(".")[-1]
        return "media/events/" + str(uuid.uuid4()) + "." + extension
