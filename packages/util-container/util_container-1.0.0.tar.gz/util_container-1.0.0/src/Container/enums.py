from enum import Enum, IntEnum, unique


# region Clases
class EnumENTIDAD(Enum):

    @property
    def valor(self):
        return self.value[0]

    @property
    def texto(self):
        return self.value[1]

    @classmethod
    def get_texto(cls, valor: int) -> str:
        for k, v in cls.__members__.items():
            if v.valor == valor:
                return v.texto
        return ''

    @classmethod
    def buscar_miembro(cls, valor: int):
        for k, v in cls.__members__.items():
            if v.valor == valor:
                return cls.__members__[k]
        return None


@unique
class EchIntEnum(IntEnum):
    @classmethod
    def to_tuple_list(cls):
        return [(x.value, x.name.capitalize()) for x in cls]

    @classmethod
    def to_str_list(cls):
        return [x.name for x in cls]

    @classmethod
    def to_value_list(cls):
        return [x.value for x in cls]

    @classmethod
    def get_name(cls, value: int) -> str:
        for x in cls:
            if x.value == value:
                return x.name
        return ''


@unique
class EchStrEnum(Enum):
    def __repr__(self) -> str:
        return self.value


# endregion

@unique
class EnumAtrTipoDato(IntEnum):
    ANY = -1
    NONE = 0
    STRING = 1
    NUM = 2
    DATE = 4
    BOOL = 8
    ENUM = 16

    def __repr__(self) -> str:
        return f'{self.value}'


@unique
class EnumCampoModo(IntEnum):
    NORMAL = 1
    ATR_NO_ASIGNAR = 2
    SUMAR = 4
    RESTAR = 8
    NO_GUARDAR = 16
    NULL_SI_VACIO = 128
    ENCRIPTADO = 256
    FECHA_DEL_SERVER = 512
    FECHA_Y_HORA = 1024

    def __repr__(self) -> str:
        return f'{self.value}'


@unique
class EnumTipodato(Enum):
    ANY = 'Any'
    INT = 'int'
    STRING = 'string'
    BOOL = 'bool'
    DATE = 'date'

    def __repr__(self) -> str:
        return f'{self.value}'


@unique
class EnumFiltro(Enum):
    EXACTO = 'iexact'
    IGUAL = 'exact'
    CONTIENE = 'icontains'
    MAYOR = 'gt'
    MAYOR_IGUAL = 'gte'
    MENOR = 'lt'
    MENOR_IGUAL = 'lte'
    COMIENZA_CON = 'istartswith'
    TERMINA_CON = 'iendswith'

    @classmethod
    def lista(cls, tipo_dato: EnumTipodato) -> list[str]:
        # return [x.value for x in cls.__members__.values()]
        match tipo_dato:
            case EnumTipodato.INT:
                return [cls.IGUAL.value, cls.MAYOR.value,
                        cls.MAYOR_IGUAL.value, cls.MENOR.value, cls.MENOR_IGUAL.value]
            case EnumTipodato.STRING:
                return [cls.EXACTO.value, cls.CONTIENE.value, cls.COMIENZA_CON.value, cls.TERMINA_CON.value]
            case EnumTipodato.BOOL:
                return [cls.CONTIENE.value, ]
            case _:
                return [x.value for x in cls.__members__.values()]


@unique
class EnumSubSistema(IntEnum):
    COMPRAS = 1
    VENTAS = 2
    TESORERIA = 3
    BANCOS = 4

    VTASALUCONT = 9

    COBRANZAS = 21
    PAGOS = 22
    RECEPCIONES = 23

    GENERAL = 20
    STOCK = 30

    PRODUCCION = 70

    BANCOSADM1 = 90
    CEREALES = 91

    def __repr__(self) -> str:
        return f'{self.value}'


@unique
class EnumOrigen(IntEnum):
    ESTRATEGA = 1
    BACKEND = 2
    GENERICO = 4
    TIENDANUBE = 8
    MERCADOLIBRE = 16
    AFIP = 32

    def __repr__(self) -> str:
        return f'{self.value}'

    def __str__(self) -> str:
        return f'{self.name}: {self.value}'


@unique
class EnumComprobTipoEnum(IntEnum):
    Factura = 1
    NDebito = 2
    NCredito = 4
    Ajustes = 8
    Recibos = 16
    OrdPag = 32
    Remito = 64
    Presupuesto = 128
    Contado = 256
    CtaCorr = 512
    MovBanco = 1024
    Rendicion = 2048
    LiquidoProducto = 4096
    OrdPagProForma = 8192
    Tiendanube = 16384

    def __repr__(self) -> str:
        return f'{self.value}'


@unique
class EnumComprobModo(IntEnum):
    NONE = 0
    INGRESO = 1
    CONSULTA = 2
    ANULACION = 4
    AGREGASTOCK = 8
    RESTASTOCK = 16
    REIMPRESION = 2054
    INTERACTIVO = 2048

    def __repr__(self) -> str:
        return f'{self.value}'


@unique
class EnumTipoMovStk(IntEnum):
    SUMA_STK = 1
    RESTA_STK = -1
    NO_MODIFICA_STK = 0

    def __repr__(self) -> str:
        return f'{self.value}'


@unique
class EnumPrecioRedondeo(Enum):
    NO = 0
    CERO_UNO = 0.1
    CERO_CINCO = 0.5
    UNO = 1
    CERO_CERO_UNO = 0.01
    CERO_CERO_CINCO = 0.05

    def __repr__(self) -> str:
        return f'{self.value}'


@unique
class EnumTriState(IntEnum):
    FALSE = 0
    TRUE = 1
    USE_DEFAULT = -2

    def __repr__(self) -> str:
        return f'{self.value}'


@unique
class EnumTipResBusqueda(IntEnum):
    GENERICO = -1
    NONE = 0
    INT = 1
    STR = 2
    FLOAT = 4
    LIST = 8
    DICT = 16
    TUPLE = 32
    QUERYSET = 64

    def __repr__(self) -> str:
        return f'{self.value}'


@unique
class EnumDefaults(Enum):
    ORIGEN = EnumOrigen.BACKEND

    def __repr__(self) -> str:
        return f'{self.value}'


@unique
class EnumCbtcod(IntEnum):
    INF_RECEPC = 60
    MOV_STOCK = 80

    def __repr__(self) -> str:
        return f'{self.value}'


@unique
class EnumTmscod(IntEnum):
    COMPRAS = 2
    INF_RECEP = 11
    MOV_INTERDEP = 23
    REMITOS = 50
    FACTURA = 51
    ENTRADA = 66
    SALIDA = 77


# noinspection PyNestedDecorators,PyPropertyDefinition
@unique
class EnumTransmisionTipo(IntEnum):
    NONE = 0
    TIENDANUBE = 1
    MERCADOLIBRE = 2
    SHOPIFY = 4

    @property
    @classmethod
    def listado_valores(cls):
        return [(x.value, x.name.capitalize()) for x in cls]

    @property
    @classmethod
    def listado_nombres(cls):
        return [(x.name.lower(), x.name.capitalize()) for x in cls]


# noinspection PyNestedDecorators,PyPropertyDefinition
@unique
class EnumTransmisionOperacion(IntEnum):
    NONE = 0
    STKMOV = 1
    VTAPED = 2

    def __str__(self) -> str:
        return f'{self.name}'

    @property
    @classmethod
    def listado_valores(cls):
        return [(x.value, x.name.capitalize()) for x in cls]

    @property
    @classmethod
    def listado_nombres(cls):
        return [(x.name.lower(), x.name.capitalize()) for x in cls]


@unique
class EnumPedEstado(IntEnum):
    SIN_MOVIMIENTOS = 0
    HABILITADO = 1
    PREPARADO = 2
    ENTREGADO = 4
    FACTURADO = 8
    ORDENADO = 16
    RESERVA_LOTE = 32


@unique
class EnumStkComoMover(IntEnum):
    NO_MUEVE = 1
    GRANEL = 2
    LOTE = 4
    SERIE = 8


@unique
class EnumUsoCta(IntEnum):
    VENTAS = 2
    VENTAS_DTO = 4
    COBRANZAS = 16
    COMPRAS = 32
    COSTOS = 64
    DIS_GASTOS = 128
    STOCK = 256
    VENTAS_RECARGO = 512
    COMPRAS_DTO = 1024
    COMPRAS_RECARGO = 2048
    COMPRAS_PROVISION = 4096
    COBRAN_TESOR = 8192


@unique
class EnumImpueParent(Enum):
    NONE = "null"
    CLIENTE = "CCTClien"
    ARTICULO = ""
    IVA_SUJETO = "FSMCTIva"
    CAT_IIBB = "CCTCatIB"
    PROVEEDOR = "CCTProv"


@unique
class EnumJOIN(Enum):
    INNER = 'INNER'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    OUTER = 'OUTER'


@unique
class EnumDias(EchIntEnum):
    _ = 0
    DOMINGO = 1
    LUNES = 2
    MARTES = 3
    MIERCOLES = 4
    JUEVES = 5
    VIERNES = 6
    SABADO = 7


class TablaCodigosErroresLoginConexion(Enum):
    """Referencia adicional para los errores, para que pueda manejar el detalle desde el front."""
    DESCONOCIDO = (0, "Desconocido")
    FALTAN_DATOS = (1, "Faltan datos")
    CONEXION = (2, "Problema de conexión")
    NO_LOGIN = (3, "Usuario no logeado")
    PWD_INCORRECTO = (4, "Contraseña incorrecta")
    PWD_NO_GEN = (5, "Contraseña no generada")
    USER_NO_ENCONTRADO = (6, "Usuario no encontrado o inexistente")
    USER_EXISTENTE = (7, "Usuario existente")
    CONFIGURACION = (8, "Problema de configuración")

    @property
    def code(self) -> int:
        return self.value[0]

    @property
    def txt(self) -> str:
        return self.value[1]

    @classmethod
    def get_referencias(cls) -> dict:
        return {
            "Referencias": {x.value[0]: x.value[1] for x in cls}
        }

class EnumErrorCode(IntEnum):
    NONE = 0
    CLAVES_DUPLICADAS = 1
    VALOR_NULO = 2
