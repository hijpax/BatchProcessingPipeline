import json
import typing
from datetime import datetime


class CommonLog(typing.NamedTuple):
    ip: str
    user_id: str
    lat: float
    lng: float
    ts: str
    http_request: str
    http_response: int
    num_bytes: int
    user_agent: str


def parse_json(element):
    row = json.loads(element)
    row['ts'] = row['timestamp']
    row.pop('timestamp')
    return CommonLog(**row)


def format_timestamp(element):
    ts = datetime.strptime(element.ts[:-8], "%Y-%m-%dT%H:%M:%S")
    ts = datetime.strftime(ts, "%Y-%m-%d %H:%M:%S")
    temp_dict = z._asdict()
    temp_dict['ts'] = ts
    return CommonLog(**temp_dict)


def to_dict(row):
    return {'page_views' : row.page_views,
            'start_time' : row.start_time}