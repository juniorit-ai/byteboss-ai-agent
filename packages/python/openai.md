Name: openai
Verison: 1.36.0
home: https://github.com/openai/openai-python

Sampple code:
```python
import os
from openai import AsyncOpenAI

class LLM:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    async def inference(self, messages):
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during LLM inference: {e}")
            return ""

    async def get_embedding(self, text):
        try:
            response = await self.client.embeddings.create(
                input=text,
                model=self.embedding_model,
                encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return []

```