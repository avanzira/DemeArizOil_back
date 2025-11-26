# file: src/app/core/enums/stock_enums.py

from enum import Enum


class StockLocationType(str, Enum):
    COMPANY = "COMPANY"
    CUSTOMER = "CUSTOMER"


class StockMoveType(str, Enum):
    PURCHASE = "PURCHASE"
    SALE = "SALE"
    TRANSFER = "TRANSFER"
    ADJUSTMENT = "ADJUSTMENT"

# end file: src/app/core/enums/stock_enums.py