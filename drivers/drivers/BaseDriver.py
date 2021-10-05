import abc


class BaseDriver:
    """
    This class describe the rules of inserting new offer to external system.
    Especially it provides a logic of this behaviour.
    Each system will be executing according to the same schema:
    - login
    - insert
    - logout
    Every new system has to get new class that provides the rules for it.
    Objects of Driver classes have data prop where they can store additional data.
    """
    data = {}
    
    @staticmethod
    def get_required_fields():
        return []
        
    @abc.abstractmethod
    def login(self, **kwargs):
        """
        Login method for authoriza to platform that user want to store any offers.
        This method will be sending login data to external server or scraping it.
        It is dependent on the destination.
        """
        pass
    
    @abc.abstractmethod
    def logout(self, **kwargs):
        """
        Logout method from external system.
        It's triggered when main action is finished.
        """
        pass
    
    @abc.abstractmethod
    def insert(self, **kwargs):
        """
        Logic of inserting new offer to external system.
        Is this place backend retrieves data from client and attempt
        to store them to destination.
        """
        pass