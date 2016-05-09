"""
Open Graph Protocol. Серверная часть.
"""
import re
import asyncio
import argparse
from bs4 import BeautifulSoup
from urllib.request import urlopen
from aiohttp import web


ogp_regex = re.compile(r'^og:(title|type|url|image)$')


def _parse_url(data):
    soup = BeautifulSoup(data, "html.parser")
    meta_tags = soup.findAll('meta', property=ogp_regex)
    print(meta_tags)
    return soup


# TODO: проверять валидность url
async def get_ogp_metadata(request):
    url = request.GET['url']
    data = urlopen(url)

    metadata = _parse_url(data)

    return web.Response()


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, help='Server port', default=8080)

    args = parser.parse_args()
    return args


async def init(loop, port):
    app = web.Application()
    app.router.add_route('GET', '/', get_ogp_metadata)
    srv = await loop.create_server(app.make_handler(), '0.0.0.0', port)
    return srv


def main():
    args = _get_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop, args.port))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
