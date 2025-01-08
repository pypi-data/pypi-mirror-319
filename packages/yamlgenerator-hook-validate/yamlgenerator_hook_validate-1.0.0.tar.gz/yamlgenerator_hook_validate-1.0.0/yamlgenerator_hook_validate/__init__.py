from gameyamlspiderandgenerator.hook import BaseHook, HookLoadingSequence
from gameyamlspiderandgenerator.util.spider import get_text
from jsonschema import validate
from yaml import safe_load
from loguru import logger


class Verify(BaseHook):
    CHANGED = None
    ORDER = HookLoadingSequence.LAST

    def setup(self, data: dict):
        try:
            validate({**data, 'thumbnail': 'thumbnail.png'},
                     safe_load(get_text('https://raw.githubusercontent.com/FurryGamesIndex/games/master/schemas'
                                        '/game.schema.yaml')))
            logger.success("verification complete")
        except Exception as e:
            logger.error(e)
        return data
