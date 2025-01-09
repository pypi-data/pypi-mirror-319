# RuModeratorAI

Библиотека для использования RuModeratorAI API (https://moderator.pysols.ru).

## Установка

```bash
pip install rumoderatorai
```

## Пример использования

```python
from rumoderatorai import Client

import asyncio

from PIL import Image

import os
from pathlib import Path


async def main():
    async with Client(
        api_key=os.getenv("RUMODERATORAI_API_KEY")
    ) as client:
        text_response = await client.get_text_class("Hello, world!")
        print(text_response)

        profile_response = await client.get_profile_class(
            username="test",
            first_name="test",
            last_name="test",
            description="test",
            is_premium=False,
        )
        print(profile_response)

        image = Image.open("tests/image.png")
        image_response = await client.get_image_class(image)
        print(image_response)

        stats_response = await client.get_stats()
        print(stats_response)

        key_info_response = await client.get_key_info()
        print(key_info_response)

        prediction_response = await client.get_prediction(unique_id=text_response.unique_id)
        print(prediction_response)

        ips_response = await client.get_ips()
        print(ips_response)

        prices_response = await client.get_prices()
        print(prices_response)


asyncio.run(main())
```

**Примечание:** Не забудьте установить переменную окружения `RUMODERATORAI_API_KEY` перед запуском кода.
