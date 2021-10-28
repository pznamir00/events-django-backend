
class CheckEmailProvidedIfNotAuthenticated:
    requires_context = True
    
    def __call__(self, value, serializer_field):
        print(serializer_field.context)