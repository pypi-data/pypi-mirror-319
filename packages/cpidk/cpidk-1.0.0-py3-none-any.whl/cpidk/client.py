import hashlib
from typing import Optional

import requests
from pydantic import ValidationError
from requests import RequestException

from cpidk.exceptions import ServerError, UnknownError
from cpidk.model import ErrorResponse, Document


def check_driver_permissions(
        firstname: str,
        surname: str,
        serial_number: str,
) -> Optional[Document]:
    md5 = hashlib.md5()

    firstname = (firstname.upper()
               .replace("Ł", "L")
               .replace("Ą", "A")
               .replace("Ę", "E")
               .replace("Ś", "S")
               .replace("Ć", "C")
               .replace("Ń", "N")
               .replace("Ó", "O")
               .replace("Ż", "Z")
               .replace("Ź", "Z")
               .replace(" ", ""))

    surname = (surname.upper()
               .replace("Ł", "L")
               .replace("Ą", "A")
               .replace("Ę", "E")
               .replace("Ś", "S")
               .replace("Ć", "C")
               .replace("Ń", "N")
               .replace("Ó", "O")
               .replace("Ż", "Z")
               .replace("Ź", "Z")
               .replace(" ", ""))

    md5.update(firstname.encode())
    md5.update(surname.encode())
    md5.update(serial_number.upper().encode())

    digest = md5.hexdigest().upper()

    try:
        response = requests.get(
            "https://moj.gov.pl/nforms/api/UprawnieniaKierowcow/2.0.10/data/driver-permissions?hashDanychWyszukiwania=" + digest
        )
    except RequestException as e:
        raise ServerError(str(e))

    data = response.json()

    if not response.ok:
        try:
            data = ErrorResponse.model_validate(data)

            if len(data.errors) == 1 and data.errors[0].code == "DICT501_UKG_1": # No data found
                return None

            if len(data.errors) == 0:
                raise ServerError("Unknown error")

            raise ServerError(", ".join([f"{error.message} ({error.code})" for error in data.errors]))

        except ValidationError as e:
            raise UnknownError(e)

    try:
        data = Document.model_validate(data)
    except ValidationError as e:
        raise UnknownError(e)

    return data
