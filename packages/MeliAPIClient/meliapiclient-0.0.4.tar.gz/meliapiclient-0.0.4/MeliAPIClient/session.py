from datetime import datetime, timedelta
from requests import request
from typing import Union
import json
import os
from dotenv import load_dotenv

# Cargar las variables desde el archivo .env
load_dotenv()

class Session:
    def __init__(
        self,
        keys: Union[dict, str] = None,
        token: Union[dict, str] = None,
        user: Union[dict, str] = None,
    ) -> None:
        self.headers: dict = {"Authorization": "", "format-new": "true"}

        # Si no se proporcionan parámetros, usar las variables de entorno
        self.ml_keys = read(keys) if keys else self.load_env_keys()
        self.ml_token = read(token) if token else self.load_env_token()
        self.ml_user = read(user) if user else {}

        self.access()

    def access(self) -> dict:
        """Actualiza el token de acceso si ha expirado."""
        time_flag = timedelta(hours=5, minutes=59, seconds=0.0)
        date_token = datetime.fromisoformat(self.ml_token["date"])
        token_time = datetime.now() - date_token

        if time_flag > token_time:
            self.headers["Authorization"] = f'Bearer {self.ml_token["access_token"]}'
            return self.ml_token

        self.ml_token = self.refresh()
        self.headers["Authorization"] = f'Bearer {self.ml_token["access_token"]}'
        return self.ml_token

    def refresh(self) -> dict:
        """Obtiene un nuevo token de acceso usando el refresh token."""
        url = "https://api.mercadolibre.com/oauth/token"

        payload: dict = {
            "grant_type": "refresh_token",
            "client_id": self.ml_keys["client_id"],
            "client_secret": self.ml_keys["client_secret"],
            "refresh_token": self.ml_token["refresh_token"],
        }

        headers: dict = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
        }

        response = request("POST", url, headers=headers, data=payload)

        if response.status_code != 200:
            raise ValueError(f"Error refreshing token: {response.text}")

        ml_response: dict = json.loads(response.text)
        ml_response["date"] = datetime.isoformat(datetime.now())

        write("ml_token.json", ml_response)  # Guardar token actualizado en archivo
        return ml_response

    def load_env_keys(self) -> dict:
        """Carga las credenciales de Mercado Libre desde las variables de entorno."""
        return {
            "client_id": os.getenv("ML_CLIENT_ID"),
            "client_secret": os.getenv("ML_CLIENT_SECRET"),
        }

    def load_env_token(self) -> dict:
        """Carga el token desde las variables de entorno."""
        return {
            "access_token": os.getenv("ML_ACCESS_TOKEN"),
            "refresh_token": os.getenv("ML_REFRESH_TOKEN"),
            "date": os.getenv("ML_TOKEN_DATE", datetime.isoformat(datetime.now())),
        }


def read(file_name: Union[dict, str]) -> dict:
    """Lee un archivo JSON o retorna directamente el diccionario proporcionado."""
    if isinstance(file_name, str) and file_name.endswith(".json"):
        with open(file_name, "r") as content:
            return json.load(content)
    return file_name


def write(file_name: str, data: dict) -> None:
    """Escribe un diccionario en un archivo JSON."""
    with open(file_name, "w") as content:
        json.dump(data, content, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    session = Session()  # Usará las variables del entorno por defecto
    print(session.ml_user)  # Si tienes datos en el usuario
