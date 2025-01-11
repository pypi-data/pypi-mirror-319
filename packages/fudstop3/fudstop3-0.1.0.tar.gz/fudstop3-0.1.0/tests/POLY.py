import sys
from pathlib import Path



project_dir = str(Path(__file__).resolve().parents[1])
if project_dir not in sys.path:
    sys.path.append(project_dir)

from fudstop3.apis.polygonio.async_polygon_sdk import Polygon
from fudstop3.apis.polygonio.polygon_options import PolygonOptions
poly = Polygon()
opts = PolygonOptions()
import requests
import aiohttp
from urllib.parse import urlencode
import asyncio
from fudstop3.apis.polygonio.polygon_options import PolygonOptions


opts_ = PolygonOptions()
async def main():

    opts = await opts_.get_option_chain_all('SPY')

    print(opts)



asyncio.run(main())

