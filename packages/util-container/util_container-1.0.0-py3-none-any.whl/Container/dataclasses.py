import json
from typing import Any
from pydantic import BaseModel
from dataclasses import dataclass
from datetime import datetime
from .enums import *


# noinspection PyUnresolvedReferences
class DataClassNecesarios(BaseModel):
    @classmethod
    def listado(cls) -> list[str]:
        return [x for x in cls.__fields__.keys()]

    @classmethod
    def defaults_dict(cls) -> dict:
        return {k: v.default for k, v in cls.__fields__.items()}


@dataclass
class DescError:
    valor: str = ''
    fx_o_class: str = ''
    modulo_o_archivo: str = ''
    status: int = 500


class Busqueda(BaseModel):
    vacia: bool = True
    tipo_resultado: Any
    resultado: Any = None


@dataclass
class Resp:
    status: int
    message: str

    @property
    def json(self) -> str:
        return json.dumps(
            {
                'status': self.status,
                'message': self.message
            }
        )


@dataclass
class FiltroSearch:
    filtro: Any
    tipo: EnumTipodato


# * ------------------------------------------------------------
# * STOCK


class DcStkMovdet(BaseModel):
    talle: str
    cantidad: int
    secsec: int


class DcStkMovart(BaseModel):
    artcod: str
    depcod: int = 0
    cant: int
    stkmovdets: list[DcStkMovdet]
    sec: int


class DcStkmov(BaseModel):
    cbtnro: int
    fecha: datetime
    cbtcod: int = 80
    tipo: int = 27
    deposito: int = 0
    moneda: int = 1
    sucursal: int = 0
    sucursal_transmisiones: int = 0
    centro_emisor = 0
    usuario: str = 'sa'
    estacion: str = 'back'
    stkmovarts: list[DcStkMovart]
