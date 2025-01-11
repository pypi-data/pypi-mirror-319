import re
import secrets
import string
from dataclasses import asdict
from decimal import Decimal

from .dataclasses import *


def update_dataclass_from_dict(data_class: Any, data: dict) -> Any:
    """Toma una dataclass modelo y actualiza sus propiedades tomandolas desde las claves de un diccionario.

    Args:
        data_class (Any): Clase modelo.
        data (dict): Diccionario a utilizar.

    #// Returns:
    #//    dataclass: _description_
    """
    for key, value in data.items():
        if key in asdict(data_class):
            setattr(data_class, key, value)
    # return dataclass


def lmap(*args, **kwargs):
    return list(map(*args, **kwargs))


def fx_list(new: list, fx, old: list, preserve: bool = False) -> None:
    """Genera una lista donde cada elemento es el resultado de la función proporcionada
    como parámetro por cada elemento de la lista de referencia.

    Args: new (list): Lista que contendrá los nuevos valores obtenidos por la función. fx (function): Función que
    regresa el valor de interés a almacenar en la lista nueva. old (list): Lista de referencia sobre la cual se va a
    iterar la función. preserve (bool) (Default: False): Indica si la lista de valores nuevos debe preservar su
    contenido previo en caso de existir.
    """
    if not preserve:
        new.clear()
    new.extend(map(fx, old))


def filter_none_in_list_dict(data: list[dict]):
    return [
        {
            k: v
            for k, v in d.items()
            if v is not None}
        for d in data
    ]


def filter_none_in_dict(data: dict) -> dict:
    return {
        k: v
        for k, v in data.items()
        if v is not None
    }


def dcFields(cls):
    fields = []
    for x in cls._meta.get_fields():
        if not x.blank and not x.null:
            match x.get_internal_type:
                case 'BooleanField':
                    tipo = bool
                case 'CharField':
                    tipo = str
                case 'IntegerField':
                    tipo = int
                case _:
                    tipo = None
            field = (x.name, tipo)
            fields.append(field)

    return fields


def identificar_tipo(x: Any) -> EnumAtrTipoDato:
    if str(x).find('str') == 0:
        tipo = EnumAtrTipoDato.STRING
    elif str(x).find('int') == 0 or str(x).find('float') == 0:
        tipo = EnumAtrTipoDato.NUM
    elif str(x).find('bool') == 0:
        tipo = EnumAtrTipoDato.BOOL
    elif str(x).find('date') == 0 or str(x).find('datetime') == 0:
        tipo = EnumAtrTipoDato.DATE
    else:
        tipo = EnumAtrTipoDato.ANY
    return tipo


def param_search_str(queryset, filtros: list[FiltroSearch]) -> Any:
    """Filtra según los parámetros indicados."""
    filtro = None
    for i, f in enumerate(filtros):
        if i == 0:
            filtro = f.filtro
        else:
            filtro |= f.filtro
    return queryset.filter(filtro)


def save_to_debug_file(text: str, path: str | None = None):
    file_path = 'C:/ech/debug.log' if path is None else path
    with open(file_path, '+a') as error_file:
        error_file.write(datetime.now().strftime(
            "%d/%m/%Y, %H:%M:%S") + ":\t" + text + "\n")


def save_version_file(text: str, path: str | None = None):
    file_path = 'C:/ech/version.log' if path is None else path
    with open(file_path, 'a') as error_file:
        error_file.write(datetime.now().strftime(
            "%d/%m/%Y, %H:%M:%S") + ":\t" + 'Version ejecutada: ' + text + "\n")


def get_fecha_actual_str() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def validar_claves_dict(diccionario: dict, lista_claves: list[str]) -> tuple[bool, str]:
    claves_no_encontradas: list[str] = []
    for clave in lista_claves:
        if clave not in diccionario.keys():
            claves_no_encontradas.append(clave)
    if claves_no_encontradas:
        return False, ', '.join(claves_no_encontradas)
    return True, ''


def validar_email(email: str) -> bool:
    if email is None:
        return False
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    else:
        return False


def parse_txt_date(fecha_str) -> datetime | None:
    try:
        fecha = datetime.strptime(fecha_str, '%d%m%Y')
        return fecha
    except ValueError:
        # print("Formato de fecha incorrecto. Debe ser 'ddmmaaaa'. ")
        return None


def to_decimal(numero: str | int | float) -> Decimal:
    if isinstance(numero, str):
        # noinspection PyBroadException
        try:
            return Decimal(numero)
        except:
            return Decimal(0)
    return Decimal(str(numero))  # -> Para garantizar la precisión.


def bool_to_int(x: bool) -> int:
    return 1 if x else 0


def dict_merge_Nones(dict_con_nulos: dict, dict_con_valores: dict) -> dict:
    """Devuelve un diccionario con los valores del primer diccionario reemplazando las claves con valores nulos por
    los valores de la mismas claves del segundo diccionario (si no son nulos).
    Por ejemplo:
    dict_con_nulos = {'clave1': None, 'clave2': 'algo'}
    dict_con_valores = {'clave1': 'valor', 'clave3': 1000}
    Resultado -> {'clave1': 'valor, 'clave2': 'algo'}
    """
    new_dict = {}
    for k, v in dict_con_nulos.items():
        if v:
            new_dict.update({k: v})
        elif v is None and (new_val := dict_con_valores.get(k, None)):
            new_dict.update({k: new_val})
    return new_dict


def try_parse_int(value: str, default=None):
    """Devuelve el valor proporcionado convertido a 'int'. En caso de no poder devuelve el valor indicado por
    defecto."""
    try:
        return int(value)
    except ValueError:
        return default


def generar_password(longitud_pwd: int = 12) -> str:
    letras = string.ascii_letters
    digitos = string.digits
    especiales = '!#$%&()*+,-./:;=<>?@[]_{}'
    caracteres = letras + digitos + especiales
    pwd = ''
    for i in range(longitud_pwd):
        pwd += ''.join(secrets.choice(caracteres))
    return pwd

import calendar
from datetime import datetime
from .enums import *


# ---------------------------------------------------------------------------------------------------------------


def getID(ss: EnumSubSistema,
          cbtnro: int,
          procuit: str,
          cemcod: int = 0,
          cbtcod: int = 80,
          hojcod: int = 0,
          procod: int = 0,
          succod: int = 1,
          tmscod: int = 27,
          borrando: bool = False,
          cbtfec: datetime | None = None,
          origen: EnumOrigen = EnumOrigen.ESTRATEGA,
          **kwargs
          ) -> str:
    resultado: str = ""

    # : Hago distinción según origen con un prefijo
    prefijo: str = get_prefix(origen)
    _cbtnro = cbtnro or ''
    _procuit = procuit or ''
    _cemcod = cemcod or ''
    _cbtcod = cbtcod or ''
    _hojcod = hojcod or ''
    _procod = procod or ''
    _succod = succod or ''
    _tmscod = tmscod or ''
    match ss:
        case EnumSubSistema.STOCK:
            resultado += f'{_succod:03}{_tmscod:02}{_procod:05}{_hojcod:02}'
        case EnumSubSistema.COMPRAS | EnumSubSistema.PAGOS:
            resultado += f'{_procod:05}' + procuit.strip().ljust(11)[11]

    resultado = f'{prefijo}{ss.value:02}{_cbtcod:02}{_cemcod:04}{_cbtnro:08}{resultado}' + \
                ('*' if borrando else '')

    return resultado.strip()


def get_prefix(origen: EnumOrigen) -> str:
    if not origen:
        return 'I'
    match origen.name:
        case 'ESTRATEGA':
            prefijo = 'I'
        case 'TIENDANUBE':
            prefijo = 'TNUB'
        case 'AFIP':
            prefijo = 'AFIP'
        case 'MERCADOLIBRE':
            prefijo = 'MELI'
        case 'BACKEND':
            # prefijo = 'BACK'
            prefijo = 'I'  # -> Lo  necesito para no generar problemas
        case _:
            prefijo = 'API'
    return prefijo


# ---------------------------------------------------------------------------------------------------------------


def vta_bonificacion_armar(bonificaciones: list[int | float]) -> int | float:
    valor = 100
    for b in bonificaciones:
        valor *= 1 - b / 100
    resultado = 100 - valor
    return round(resultado, 2)


# ---------------------------------------------------------------------------------------------------------------


def ultimo_dia_del_mes(anio, mes):
    ultimo_dia = calendar.monthrange(anio, mes)[1]
    fecha = datetime(anio, mes, ultimo_dia)
    return fecha


# ---------------------------------------------------------------------------------------------------------------


def precios_vta_redondear(precio: float, opcion_redondeo: EnumPrecioRedondeo) -> float:
    _precio: float
    match opcion_redondeo.value:
        case 0.1:
            _precio = round(precio, 1)
        case 0.01:
            _precio = round(precio, 2)
        case 0.5:
            _precio = round(2 * precio, 0) / 2
        case 0.05:
            _precio = round(20 * precio, 0) / 20
        case 1:
            _precio = round(precio, 0)
        case _:
            _precio = precio
    return _precio
