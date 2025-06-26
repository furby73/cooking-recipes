from flask_login import UserMixin

class AdminUser(UserMixin):
    def __init__(self, id='admin'):
        self.id = id

    @property
    def is_active(self):
        return True

    def get_id(self):
        return self.id