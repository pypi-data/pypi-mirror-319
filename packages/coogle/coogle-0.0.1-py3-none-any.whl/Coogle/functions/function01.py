import re
from urllib.parse import urlparse
from urllib.parse import parse_qs
from .exceptions import InvalidToken
#======================================================================

async def checktok(token):
    tokens = token.split()[-1]
    if len(tokens) == 73 and tokens[1] == "/":
        raise InvalidToken()

#======================================================================

async def get_uid(link: str, pattern=None):
    if ("folders" in link) or ("file" in link):
        resous = re.search(pattern, link)
        moonus = resous.group(3) if resourcs else None
        return moonus
    else:
        resous = urlparse(link)
        moonus = parse_qs(resous.query)['id'][0]
        return moonus

#======================================================================
