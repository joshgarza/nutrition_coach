import myfitnesspal
import requests
import datetime


class NoPasswordClient(myfitnesspal.Client):

    def __init__(self, username, password=None, login=False, unit_aware=False):
        self.provided_username = username
        self.__password = password
        self.unit_aware = unit_aware

        self._user_metadata = {}
        self._auth_data = {}

        self.session = requests.Session()


class FriendClient(myfitnesspal.Client):

    def __init__(self, friend_username, app_username, app_password, login=False, unit_aware=False):
        self.provided_username = app_username
        self.__password = app_password
        self.friend_username = friend_username
        super().__init__(self.provided_username, password=self.__password)

    def get_date(self, *args, **kwargs):

        return super().get_date(*args, username=self.friend_username)
        