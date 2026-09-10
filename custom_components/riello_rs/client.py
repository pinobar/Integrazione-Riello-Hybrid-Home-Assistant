import requests

from .parser import RielloParser

from .exceptions import (
    LoginError,
    ConnectionError,
)


class RielloClient:

    def __init__(self, username, password):

        self.username = username
        self.password = password

        self.parser = RielloParser()

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "it-IT,it;q=0.9"
        })

        self.login_url = "https://www.riello-rsmonitoring.com/index.php"
        self.home_url = "https://www.riello-rsmonitoring.com/home_hyd.php"
        self.data_url = "https://www.riello-rsmonitoring.com/dataInfo_hyd.php"

    def login(self):
        """Effettua il login sul portale Riello."""

        payload = {
            "username": self.username,
            "password": self.password,
            "submit": "Log In",
        }

        r = self.session.post(
            self.login_url,
            data=payload,
            timeout=60,
        )

        if r.status_code != 200:
            raise ConnectionError(
                f"Errore HTTP {r.status_code}"
            )

        if "Username and/or Password not correct" in r.text:
            raise LoginError(
                "Username o password non validi"
            )

        return True

    def select_plant(self):

        self.session.get(
            self.home_url,
            timeout=60
        )

    def download(self):

        r = self.session.get(
            self.data_url,
            timeout=60
        )

        return r.text

    def update(self):

        self.login()

        self.select_plant()

        html = self.download()

        return self.parser.parse(html)