import time
import asyncio


# Your synchronous and asynchronous functions
def synchronous_function(message: str):
    print(f"Synchronous Job: {message}")
    return message.upper()


async def asynchronous_function(message: str):
    print(f"Asynchronous Job: {message}")
    raise Exception("Something went wrong!")
    await asyncio.sleep(2)  # Simulate some asynchronous operation
    return message.lower()



