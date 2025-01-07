from typing import cast

import uvicorn
from fastapi import FastAPI

from .models import capitals, CepData
from .system import get_data, get_capital, get_capital_weather


def run():
    """Serve a local API to test the script on http://127.0.0.1:8000/docs"""
    print("You can access through http://127.0.0.1:8000/docs")
    app = FastAPI(
        title="CEP & Weather API",
        description="Local server to test the script of this API",
        version="1.0",
        contact={
            "name": "João Marcionilo",
            "email": "marcionilojob@gmail.com",
        },
        license_info={
            "name": "MIT License",
            "url": "https://github.com/Joao-Marcionilo/cep-weather/blob/main/LICENSE",
        }
    )

    @app.get("/get_data")
    async def app_get_data(cep: str) -> CepData:
        """
        Fetch a capital's data from another API.\n
        Caution: massive use for validation of local databases may block your access for an indefinite period.
        """
        return cast(CepData, get_data(cep))

    @app.get("/get_capital")
    async def app_get_capital(cep: str) -> capitals:
        """
        Try to find the capital of a given CEP connecting to another API.\n
        Caution: massive use for validation of local databases may block your access for an indefinite period.
        """
        return cast(capitals, get_capital(cep))

    @app.get("/get_capital_weather")
    async def app_get_capital_weather(capital: capitals) -> str:
        """Scrape for the weather of a capital"""
        return get_capital_weather(capital)

    uvicorn.run(app, port=8000)
