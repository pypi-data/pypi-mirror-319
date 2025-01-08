import json
from ..scripts import Scripted
#===========================================================================================

class InvalidToken(Exception):
    pass

#===========================================================================================

async def GErrors(errors):

    if errors.resp.get(Scripted.ERROR01, Scripted.ERROR00).startswith(Scripted.ERROR02):
        line01 = json.loads(errors.content)
        line02 = line01.get("error")
        line03 = line02.get("errors")[0]
        reason = line03.get("reason")
        return str(reason)
    else:
        return errors if errors else Scripted.ERROR00

#===========================================================================================
