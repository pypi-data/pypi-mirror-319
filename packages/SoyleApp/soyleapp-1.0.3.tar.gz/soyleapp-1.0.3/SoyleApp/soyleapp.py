import requests

class SoyleApp:
    """
    A Python library to interact with the Translation API.
    """
    BASE_URL = "https://soyle.nu.edu.kz/external-api/v1/translate/text/"

    def __init__(self):
        """
        Initialize the SoyleApp client.
        The user must activate the library with a token.
        """
        self.headers = {}
        self.token = None

    def activate(self, token):
        """
        Activate the library by providing the API authorization token.

        Args:
            token (str): The API authorization token.
        """
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def translate_text(self, source_language, target_language, text):
        """
        Translate the given text from one language to another.

        Args:
            source_language (str): The initial language of the input text (e.g., "kaz", "eng", "tur", "rus").
            target_language (str): The target language for translation (e.g., "kaz", "eng", "tur", "rus").
            text (str): The text to be translated.

        Returns:
            str: The translated text.

        Raises:
            ValueError: If the API response indicates an error.
        """
        self._check_activation()

        payload = {
            "source_language": source_language,
            "target_language": target_language,
            "text": text,
            "output_format": "text",
        }

        response = requests.post(self.BASE_URL, json=payload, headers=self.headers)

        if response.status_code == 200:
            return response.json().get("text")
        else:
            raise ValueError(f"Error {response.status_code}: {response.text}")

    def _check_activation(self):
        """
        Ensure the library is activated with a token before making requests.

        Raises:
            RuntimeError: If the library is not activated.
        """
        if not self.token:
            raise RuntimeError("SoyleApp is not activated. Please call `activate(token)` with a valid token.")
