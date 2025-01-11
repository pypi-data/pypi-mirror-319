from __future__ import annotations
import logging
from copy import deepcopy
from .generales import *


class ContainerException(Exception):
    error_code: EnumErrorCode = EnumErrorCode.NONE

    def __init__(self, err: str, origen: str = '', *args: object,
                 error_code: EnumErrorCode = EnumErrorCode.NONE) -> None:
        self.error_code = error_code
        msg = err
        if origen:
            msg = f'{origen}: {err}'
        super().__init__(msg, *args)


class Container:
    # region init
    def __init__(self, data=None, objeto: Any | None = None) -> None:
        if not data:
            data = {}
        self.__data: dict = {**data}
        self.__desc_error: DescError = DescError()
        self.__lista_errores: list[str] = []
        self.__warnings: str | None = None
        self.__lista_warnings: list[str] = []
        self.__info: str | None = None
        self.__raw_queryset = []
        self.__callers: list = []
        self.__objeto: Any | None = objeto

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.clear()

    def __getitem__(self, item):
        return deepcopy(self.data.get(item, None))

    # endregion

    # region Properties
    @property
    def data(self) -> dict:
        return self.__data

    @data.setter
    def data(self, x: Any) -> None:
        self.__data = x

    @data.deleter
    def data(self) -> None:
        self.__data = {}

    @property
    def err(self) -> str:
        """Cadena formateada con la información de todos los errores."""
        if self.lista_errores:
            return ' -- '.join(self.lista_errores)
        return ''

    @err.setter
    def err(self, x: str) -> None:
        if x.strip():
            self.__desc_error.valor = x.strip()
            self.__lista_errores.append(x.strip())

    @property
    def lista_errores(self) -> list[str]:
        return self.__lista_errores

    @lista_errores.setter
    def lista_errores(self, x: list[str]) -> None:
        if x:
            self.__lista_errores = x

    @property
    def not_errors(self) -> bool:
        """Devuelve False si hay errores, de lo contario True."""
        return bool(not self.lista_errores)

    @property
    def desc_error(self) -> DescError:
        return self.__desc_error

    @desc_error.setter
    def desc_error(self, x: DescError) -> None:
        self.__desc_error = x

    @property
    def lista_warnings(self) -> list[str]:
        return self.__lista_warnings

    @lista_warnings.setter
    def lista_warnings(self, x: list[str]) -> None:
        if x:
            self.__lista_warnings = x

    @property
    def warnings(self) -> str:
        """Cadena formateada con la información de todos los errores."""
        if self.lista_warnings:
            return ' -- '.join(self.lista_warnings)
        return ''

    @warnings.setter
    def warnings(self, x: str) -> None:
        if x.strip():
            self.__lista_warnings.append(x.strip())

    @property
    def info(self) -> str:
        return self.__info or ''

    @info.setter
    def info(self, x: str) -> None:
        self.__info = x

    @property
    def callers(self) -> str:
        return str(self.__callers)

    @callers.setter
    def callers(self, x: str) -> None:
        if x:
            self.__callers.append(x)

    @property
    def objeto(self) -> Any:
        return self.__objeto

    @objeto.setter
    def objeto(self, x: Any) -> None:
        self.__objeto = x

    # endregion

    # region Métodos
    def result(self, strict: bool = False, critic: bool = False, log=False,
               error_code: EnumErrorCode = EnumErrorCode.NONE) -> bool:
        """Verifica si hay errores y advertencias en el container y registra en el log.

        Args:

            strict (bool, optional): Si es False, ignora los errores si hay advertencias. Si es True, los errores
            y las advertencias siempre harán que devuelva False.

            critic (bool, optional): Si es True lanza una excepción al encontrar un error. Ignora el valor de
            "estricto".

            log (bool, optional): Si es True registra en el archivo .log la información, advertencias o errores.

            error_code (EnumErrorCode, optional: Código a utilizar en caso de lanzar excepción.
        """
        if log:
            self.__registrar_log()

        if critic and self.not_errors is False:
            raise ContainerException(err=self.err, error_code=error_code)

        # Prioridad en las advertencias.
        if strict is False:
            if self.warnings or self.not_errors:
                return True
            return False

        # Prioridad en los errores
        if not self.not_errors or self.warnings:
            return False
        return True

    def clone(self, ctn: Container):
        """Realiza la copia profunda de toda la información del container, data, errores y advertencias."""
        self.data = deepcopy(ctn.data)
        self.err = deepcopy(ctn.err)
        self.warnings = deepcopy(ctn.warnings)
        self.info = deepcopy(ctn.info)

    # region clean/clear
    def clean(self) -> None:
        """Elimina los errores y mensajes del contenedor. Mantiene la data."""
        self.clean_errors()
        self.clean_warnings()

    def clean_warnings(self) -> None:
        self.__lista_warnings.clear()

    def clean_errors(self) -> None:
        self.__lista_errores.clear()
        self.__desc_error = DescError()

    def clear(self) -> None:
        """Elimina toda la información de la instancia del contenedor."""
        self.clean()
        self.data.clear()

    def clear_data(self) -> None:
        self.data.clear()

    def clear_last_warning(self) -> None:
        if len(self.__lista_warnings) > 0:
            self.__lista_warnings.pop()

    def clear_last_error(self) -> None:
        if len(self.__lista_errores) > 0:
            self.__lista_errores.pop()

    # endregion clean/clear

    # region add
    def add(self, key: str, value: Any, override: bool = False) -> None:
        """Agrega un par "key:value" al diccionario "data" del container. """
        if not key:
            self.warnings = 'Se intentó agregar data con una clave vacía. No se realizó modificación.'
        elif not value:
            if key not in self.data.keys():
                self.__data.update({key: value})
                self.warnings = 'Se agregó una clave sin datos.'
            elif not override:
                self.warnings = ('Se intentó pasar datos vacíos a una clave que ya contenía información. No se realizó '
                                 'modificación.')
            else:
                self.__data.update(deepcopy({key: value}))
        else:
            self.__data.update(deepcopy({key: value}))

    def multi_add(self, data: dict) -> None:
        for k, v in data:
            self.add(k, v)

    # endregion add

    # region copy
    def copy_from_key(self, destino: str, origen: str, override: bool = False):
        """Copia el valor de una clave en otra."""
        valor = deepcopy(self.data.get(origen))
        self.add(destino, valor, override)

    # endregion copy

    def __registrar_log(self) -> None:
        logging.basicConfig(
            level=logging.WARNING,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename='C:/ech/internal.log'
        )
        # : Hay errores
        if not self.not_errors:
            logging.error(self.err)

        # : Hay advertencias
        if self.warnings:
            logging.warning(self.warnings)

        # : Hay información
        if self.info:
            logging.info(self.warnings)

    def __set_desc_error(self, err: str, status: int) -> None:
        self.__desc_error.valor = err.strip()
        self.__desc_error.status = status

    # endregion
