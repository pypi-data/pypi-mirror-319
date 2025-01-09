import aiohttp

from pathlib import Path
from typing import Any

import base64
from io import BytesIO
from PIL import Image

from urllib.parse import urljoin

from . import classes


class Client:
    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        text_classification_model: str | None = None,
        profile_classification_model: str | None = None,
        image_classification_model: str | None = None,
    ):
        """
        Initialize the client

        Args:
            api_key (str): API key
            base_url (str | None): Base URL of the API
            text_classification_model (str | None): Text classification model
            profile_classification_model (str | None): Profile classification model
            image_classification_model (str | None): Image classification model
        """
        assert isinstance(api_key, str), "`api_key` must be a string"

        self._cfg = classes.Config(
            api_key=api_key,
        )

        if base_url:
            self._cfg.base_url = base_url
        if text_classification_model:
            self._cfg.text_classification_model = text_classification_model
        if profile_classification_model:
            self._cfg.profile_classification_model = profile_classification_model
        if image_classification_model:
            self._cfg.image_classification_model = image_classification_model

        self.session = aiohttp.ClientSession()

    async def __aenter__(self):
        async with self.session.post(self._cfg.base_url, json={}) as response:
            assert response.status == 200, "Failed to connect to the API"

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.close()

        del self.session
        del self._cfg

    def _url(self, path: str) -> str:
        """
        Get the full URL for the given path

        Args:
            path (str): Path to append to the base URL

        Returns:
            str: Full URL
        """
        return urljoin(self._cfg.base_url, path)

    def _json(self, **kwargs) -> dict:
        """
        Create a JSON payload for the API request

        Args:
            **kwargs: Keyword arguments to include in the JSON payload

        Returns:
            dict: JSON payload
        """
        return {"api_token": self._cfg.api_key, **kwargs}

    def _preprocess_response(self, response: dict, dataclass: Any) -> Any:
        """
        Preprocess the API response

        Args:
            response (dict): API response
            dataclass (Any): Dataclass to parse the response into

        Returns:
            Any: Parsed response
        """
        if "class" in response:
            response["label"] = response["class"]
            del response["class"]

        if "class_names" in response:
            response["class_names"] = {
                int(k): v for k, v in response["class_names"].items()
            }

        if "stats" in response:
            response["stats"] = [classes.Stat(**stat) for stat in response["stats"]]

        if dataclass == classes.PricesResponse:
            response["text_classification"] = [
                classes.Model(
                    name=model["name"],
                    price=model["price"],
                    class_names={int(k): v for k, v in model["class_names"].items()},
                )
                for model in response["text_classification"]
            ]
            response["image_classification"] = [
                classes.Model(
                    name=model["name"],
                    price=model["price"],
                    class_names={int(k): v for k, v in model["class_names"].items()},
                )
                for model in response["image_classification"]
            ]
            response["profile_classification"] = [
                classes.Model(
                    name=model["name"],
                    price=model["price"],
                    class_names={int(k): v for k, v in model["class_names"].items()},
                )
                for model in response["profile_classification"]
            ]

        assert response.get(
            "ok", False
        ), f"Failed to get response from the API ({response.get('message', 'Unknown error')})"

        try:
            return dataclass(**response)
        except Exception as e:
            raise ValueError(f"Failed to parse response from the API: {e}")

    async def get_text_class(self, text: str) -> classes.TextClassResponse:
        """
        Get the text classification

        Args:
            text (str): Text to classify

        Returns:
            classes.TextClassResponse: Text classification response
        """
        data = {"text": text, "model": self._cfg.text_classification_model}

        async with self.session.post(
            self._url("/api/v2/predict/text"), json=self._json(**data)
        ) as response:
            return self._preprocess_response(
                await response.json(), classes.TextClassResponse
            )

    async def get_profile_class(
        self,
        username: str,
        first_name: str,
        last_name: str | None = None,
        description: str | None = None,
        is_premium: bool = False,
    ) -> classes.TextClassResponse:
        """
        Get the profile classification

        Args:
            username (str): Username
            first_name (str): First name
            last_name (str | None): Last name
            description (str | None): Description
            is_premium (bool): Whether the user has Telegram Premium

        Returns:
            classes.TextClassResponse: Profile classification response
        """
        data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "description": description,
            "is_premium": is_premium,
            "model": self._cfg.profile_classification_model,
        }

        async with self.session.post(
            self._url("/api/v2/predict/profile"), json=self._json(**data)
        ) as response:
            return self._preprocess_response(
                await response.json(), classes.TextClassResponse
            )

    async def get_image_class(
        self, image: Image.Image | Path | str
    ) -> classes.ImageClassResponse:
        """
        Get the image classification

        Args:
            image (PIL.Image.Image | Path | str): Image or path to the image to classify

        Returns:
            classes.ImageClassResponse: Image classification response
        """
        if isinstance(image, Path | str):
            image = Image.open(image)

        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        data = {"image": img_str, "model": self._cfg.image_classification_model}

        buffered.close()

        async with self.session.post(
            self._url("/api/v2/predict/image"), json=self._json(**data)
        ) as response:
            return self._preprocess_response(
                await response.json(), classes.ImageClassResponse
            )

    async def get_stats(self, limit: int = 3) -> classes.StatsResponse:
        """
        Get the stats

        Args:
            limit (int): Number of hours to get stats for

        Returns:
            classes.StatsResponse: Stats response
        """
        data = {"limit": limit}

        async with self.session.get(
            self._url("/api/v2/stats"), json=self._json(**data)
        ) as response:
            return self._preprocess_response(
                await response.json(), classes.StatsResponse
            )

    async def get_key_info(self) -> classes.KeyInfoResponse:
        """
        Get the key info
        """
        async with self.session.get(
            self._url("/api/v2/key"), json=self._json()
        ) as response:
            return self._preprocess_response(
                await response.json(), classes.KeyInfoResponse
            )

    async def get_prediction(self, unique_id: str) -> classes.PredictionResponse:
        """
        Get the prediction

        Args:
            unique_id (str): Unique ID

        Returns:
            classes.PredictionResponse: Prediction response
        """
        async with self.session.get(
            self._url("/api/v2/prediction"), json=self._json(unique_id=unique_id)
        ) as response:
            return self._preprocess_response(
                await response.json(), classes.PredictionResponse
            )

    async def get_ips(self) -> classes.IpsResponse:
        """
        Get IPs who have used the API

        Returns:
            classes.IpsResponse: IPs response
        """
        async with self.session.get(
            self._url("/api/v2/ips"), json=self._json()
        ) as response:
            return self._preprocess_response(await response.json(), classes.IpsResponse)

    async def get_prices(self) -> classes.PricesResponse:
        """
        Get the prices
        """
        async with self.session.get(
            self._url("/api/v2/price"), json=self._json()
        ) as response:
            return self._preprocess_response(
                await response.json(), classes.PricesResponse
            )
