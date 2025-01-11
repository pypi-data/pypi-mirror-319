from __future__ import annotations

__docformat__ = "restructuredtext"

from fitdataset import (
    constantes_parser_dataset as constante,
    interfaces,
    parser as _parserdataset,
    dataset as _processdataset
)


_ctx = _processdataset.Dataset()


def __get_meal_item(key: interfaces.LiteralMealNames):
    return _ctx[key]


def get(item: interfaces.LiteralMealNames):
    return __get_meal_item(item)


def ctx() -> _processdataset.Dataset:
    return _ctx


frame = _ctx.frame
meal = _ctx.meal
breakfast = _ctx.breakfast
lunch = _ctx.lunch
snack = _ctx.snack
dinner = _ctx.dinner
