import asyncio

from client.client import LLMClient


async def main():
    client = LLMClient()
    messages = [{"role": "user", "content": "What's up?"}]
    async for event in client.chat_completition(messages, True):
        print(event)
    print("done")


asyncio.run(main())
