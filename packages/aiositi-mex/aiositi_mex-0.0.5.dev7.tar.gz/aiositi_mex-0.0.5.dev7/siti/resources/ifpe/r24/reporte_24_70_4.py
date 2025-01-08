from typing import List

from pydantic import Field, conlist

from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class Monto(int):
    '''
    Multiplica el valor recibido en centavos por 100 para
    que se pueda representar en 4 decimales.
    Ej 100_00 -> 100_0000
    Es una particularidad de este reporte.
    '''

    def __str__(self) -> str:
        return str(self * 100)

    def __repr__(self) -> str:
        return str(self * 100)


class ComisionesCobradas(Resource):
    '''
    Sección catalogo cuentas 4.1
    '''

    clave_comision: int = Field(ge=1, le=15)
    monto_comision: Monto
    tasa_comision: float
    numero_cobros: int
    monto_total_cobrado: Monto
    monto_total_pendiente: Monto


class InformacionSolicitada(Resource):
    '''
    Sección catalogo cuentas 4
    '''

    identificador_cuenta: int
    tipo_cuenta: int
    numero_cuenta: str
    tipo_moneda: int = 484
    tipo_cambio: float = 1.0
    clave_casfim: int
    saldo_total_inicio: Monto
    saldo_total_fin: Monto
    intereses_generados: Monto
    saldo_intereses_generados: Monto
    # sección 4.1
    comisiones_cobradas: List[ComisionesCobradas]


class Reporte2470_4(ReportIFPE, Sendable, Updateable, Resendable):
    """
    Este reporte contiene información operativa de las Instituciones
    de Fondos de Pago Electrónico
    respecto a clientes, cuentas, sobregiros, y movimientos de recursos.
    https://github.com/cuenca-mx/siti-python/wiki/Reporte-R24
    """

    informacion_solicitada: conlist(  # type: ignore[valid-type]
        InformacionSolicitada, min_items=1
    )
