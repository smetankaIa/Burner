from django.apps import AppConfig



class AProfileConfig(AppConfig):
    name = 'a_profile'
    
    def ready(self):
        import a_profile.signals