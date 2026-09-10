from .descriptions import SENSORS
from bs4 import BeautifulSoup
import re


class RielloParser:

    def _converti_valore(self, testo):
        """
        Converte:
            '355.0 kWh' -> 355.0
            '81 %'      -> 81
            '0 W'       -> 0
            '-'         -> None
            '- kWh'     -> None
            '- W'       -> None
            'OFF'       -> 'OFF'
        """

        testo = testo.strip()

        # Valori temporaneamente assenti restituiti dal portale Riello
        if testo == "-" or testo.startswith("- "):
            return None

        m = re.search(r"[-+]?\d+(?:[.,]\d+)?", testo)

        if not m:
            return testo

        numero = m.group(0).replace(",", ".")

        valore = float(numero)

        if valore.is_integer():
            return int(valore)

        return valore

    def parse(self, html, usa_descrizioni=True):

        soup = BeautifulSoup(html, "html.parser")

        dati = {}

        #
        # Informazioni dispositivo
        #

        serial = soup.find("span", class_="radio-container__sn-number")

        if serial:
            dati["serial_number"] = serial.get_text(strip=True)

        modello = soup.find("span", class_="radio-container__model-name")

        if modello:
            dati["modello"] = modello.get_text(strip=True)

        #
        # Proprietario
        #
        # Il portale Riello mostra il proprietario nel selettore
        # dell'impianto, nel <p> che richiama choose_plants().
        proprietario = soup.find("p", onclick="choose_plants()")

        if proprietario:
            nome_proprietario = proprietario.get_text(" ", strip=True)
            if nome_proprietario:
                dati["proprietario"] = nome_proprietario

        #
        # Ultimo aggiornamento
        #

        ultimo_aggiornamento = None

        for h5 in soup.find_all("h5"):
            testo = h5.get_text(" ", strip=True)
            if testo.startswith("Ultimo Aggiornamento:"):
                ultimo_aggiornamento = testo.split(":", 1)[1].strip()
                break

        if ultimo_aggiornamento:
            match = re.match(
                r"^(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2}(?::\d{2})?)$",
                ultimo_aggiornamento,
            )

            if match:
                dati["ultimo_aggiornamento_data"] = match.group(1)
                dati["ultimo_aggiornamento_ora"] = match.group(2)

        #
        # Sensori
        #

        for h5 in soup.find_all("h5"):

            testo = h5.get_text(" ", strip=True)

            if ":" not in testo:
                continue

            parametro, valore = testo.split(":", 1)

            parametro = parametro.strip()
            valore = valore.strip()

            valore = self._converti_valore(valore)

            # Modalità sviluppo
            if not usa_descrizioni:

                dati[parametro] = valore
                continue

            # Modalità Home Assistant
            if parametro not in SENSORS:
                continue

            info = SENSORS[parametro]

            dati[info["id"]] = valore

        return dati