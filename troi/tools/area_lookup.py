import sys
import uuid
from urllib.parse import quote

import requests
import ujson

from troi import Element, Artist, Recording, PipelineError

def area_lookup(area_name):
    '''
        Given an area name, lookup the area_id and return it. Return None if area not found.
    '''

    SERVER_URL = "http://bono.metabrainz.org:8000/area-lookup/json"
    data = [ { '[area]': area_name } ]
    r = requests.post(SERVER_URL, json=data)
    if r.status_code != 200:
        raise PipelineError("Cannot lookup area name. " + str(r.text))

    try:
        rows = ujson.loads(r.text)
    except ValueError as err:
        raise PipelineError("Cannot lookup area name, invalid JSON returned: " + str(err))

    if len(rows) == 0:
        raise RuntimeError("Cannot find area name. Must be spelled exactly as in MusicBrainz.")

    return rows[0]['area_id']
