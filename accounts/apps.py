from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        # 👇 THIS IS THE MAGIC LINE 👇
        # By importing your file here, Django is forced to run it!
        import config.firebase