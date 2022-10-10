import aiohttp
import asyncio
import time
import itertools

start_time = time.time()
async def get_json(session, url):
    async with session.get(url) as resp:
        ses = resp.status
        rjson = await resp.json()
        if (ses == 400 or ses == 500):
            print("error " + url, file=open('error.txt', 'a'))
        else:
            return rjson['customerId']
async def main(lb):
    connector = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i in lb:
            url = f'(your link)?knownId={i}&knownIdType=ACCOUNT_ID'
            tasks.append(asyncio.ensure_future(get_json(session, url)))
        output = await asyncio.gather(*tasks)
        for out in output:
            print(out, file=open('customerid1.txt', 'a'))
with open("accountid1.txt", "r") as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
l = len(lines)
while l > 0:
    top = itertools.islice(lines, 50)
    lines = lines[50:]
    l = len(lines)
    asyncio.run(main(top))
print("--- %s seconds ---" % (time.time() - start_time))
