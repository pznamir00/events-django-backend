import uuid

                
class EventFileNameGenerator:
    def generate(instance, filename):
        extension = filename.split('.')[-1]
        return 'media/events/' + str(uuid.uuid4()) + '.' + extension