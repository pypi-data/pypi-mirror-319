# SoyleApp

SoyleApp is a Python library for interacting with the Soyle Translation API, available at [soyle.nu.edu.kz](https://soyle.nu.edu.kz/). Before using this library, you must register on the website and obtain an API token. The resources consumed by the library will be tied to your account.

## Features
- Translate text between multiple languages.
- Retrieve translations as audio with a choice of male or female voices.

## Installation
Once the library is published, install it via pip:

```bash
pip install SoyleApp
```

## Usage
Here's how to use the library:

```python
from SoyleApp import SoyleApp 

# Create an instance of the library
app = SoyleApp()

# Activate the library with your API token
app.activate("YOUR_API_TOKEN")

# Translate text
translated_text = app.translate_text(
    source_language="eng",
    target_language="kaz",
    text="Hello, how are you?"
)
print("Translated Text:", translated_text)

```

## Note
- You need to register at [soyle.nu.edu.kz](https://soyle.nu.edu.kz/) to get an API token.
- All resource usage is tied to your account, so use your token responsibly.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

