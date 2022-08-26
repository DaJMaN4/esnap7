import asyncio

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():

    await say_after(2, 'hello')
    await say_after(1, 'world')

    print("  ")

    task1 = asyncio.create_task(
        say_after(2, 'hello'))

    task2 = asyncio.create_task(
        say_after(1, 'world'))

    await task1
    await task2

asyncio.run(main())
