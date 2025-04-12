import aiohttp
import os
from typing import Optional

async def translate_text(text: str, source: str, target: str) -> Optional[str]:
    api_key = os.getenv('BHASHINI_API_KEY')
    api_url = os.getenv('BHASHINI_API_URL')

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{api_url}/translate",
            json={
                "text": text,
                "source_language": source,
                "target_language": target
            },
            headers={"Authorization": f"Bearer {api_key}"}
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("translated_text")
            return None