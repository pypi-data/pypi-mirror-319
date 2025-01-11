import datetime as dt
from typing import List, Optional

import cbor2
from pydantic import Field

from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class Monto(int):
    def __init__(cls, value):
        if not isinstance(value, int):
            raise TypeError("El valor debe ser un entero.")
        return super().__init__(cls, value * 100)


class ModificacionRegistroCliente(Resource):
    '''
    Sección clientes 2.1
    '''

    tipo_modificacion: int = Field(ge=1, le=6)
    fecha_modificacion: dt.datetime = Field(
        json_schema_extra={"format": "%Y-%m-%dT%H:%M:%S.000Z"}
    )


class EventoCuenta(Resource):
    '''
    Sección clientes 2.3.1
    '''

    tipo_evento: int = Field(ge=1, le=10)
    fecha_evento: dt.datetime = Field(
        json_schema_extra={"format": "%Y-%m-%dT%H:%M:%S.000Z"}
    )
    identificador_cuenta_manejo_recursos: Optional[int]


class Movimientos(Resource):
    '''
    Sección clientes 2.3.2.1
    '''

    tipo: int
    total_movimientos: int
    total_monto: Monto


class InformacionAdicional(Resource):
    '''
    Sección clientes 2.3.3
    '''

    forma_fondeo_cuenta: int
    clave_institucion_fondeo: Optional[int]
    tarjetas_asociadas: int
    tarjetas_virtuales_asociadas: int
    clasificacion_cuenta: int = 1


class MovimientoCuenta(Resource):
    '''
    Sección clientes 2.3.2
    '''

    saldo_inicio_periodo: Monto
    saldo_final_periodo: Monto
    importe_minimo_cargo: Monto
    importe_maximo_cargo: Monto
    importe_minimo_abono: Monto
    importe_maximo_abono: Monto
    total_comisiones_por_cobrar: Monto
    total_comisiones_cobradas: Monto
    total_sobregiros: Monto = Monto(0)
    # sección 2.3.2.1
    movimientos: Optional[List[Movimientos]]


class CuentaCliente(Resource):
    '''
    Sección clientes 2.3
    '''

    numero_cuenta_alfanumerico: str
    # sección 2.3.1
    eventos_cuenta: Optional[List[EventoCuenta]]
    # sección 2.3.2
    movimientos_cuenta: Optional[MovimientoCuenta]
    # sección 2.3.3
    informacion_adicional: Optional[InformacionAdicional]


class DatosCliente(Resource):
    '''
    Sección clientes 2.2
    '''

    nombres: str
    primer_apellido: Optional[str]
    segundo_apellido: Optional[str]
    tipo_cliente: int = 1
    rfc: Optional[str]
    curp: Optional[str]
    nacionalidad: int = 484
    ocupacion: int = Field(ge=0, le=9)
    actividad_economica: Optional[int]
    sexo: Optional[int]
    fecha_nacimiento: dt.date = Field(json_schema_extra={"format": "YYYYMMDD"})
    # Catálogo de siti
    localidad_residencia: Optional[int]


class IdentificacionCliente(Resource):
    """
    Sección clientes 2.0
    """

    numero_cliente_alfanumerico: Optional[str]
    # Sección clientes 2.1
    modificaciones_cliente: Optional[List[ModificacionRegistroCliente]]
    # Sección clientes 2.2
    datos_cliente: Optional[DatosCliente]
    # Sección clientes 2.3
    cuentas_cliente: Optional[List[CuentaCliente]]


class Sobregiros(Resource):
    '''
    Sección sobregiros 3
    '''

    maximo: Monto = Monto(0)
    minimo: Monto = Monto(0)


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


class CatalogoCuentas(Resource):
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


class InformacionSolicitada(Resource):

    # Secciónn clientes 2
    identificacion_cliente: Optional[List[IdentificacionCliente]] = None
    # Sección sobregiros 3
    sobregiros: Optional[Sobregiros] = Sobregiros()
    # Sección catalogo cuentas 4
    catalogo_cuentas: Optional[List[CatalogoCuentas]]


class Reporte2470(ReportIFPE, Sendable, Updateable, Resendable):
    """
    Este reporte contiene información operativa de las Instituciones
    de Fondos de Pago Electrónico
    respecto a clientes, cuentas, sobregiros, y movimientos de recursos.
    https://github.com/cuenca-mx/siti-python/wiki/Reporte-R24
    """

    _resource = '/IFPE/R24/G2470'
    informacion_solicitada: InformacionSolicitada

    def to_cbor(self) -> str:
        return cbor2.dumps(self.json_to_cbnv_structure()).hex()

    def json_to_cbnv_structure(self, start_index=3):
        keys = ["_keys", "_defaults", "_data"]
        defaults = {}
        data = {}
        key_mapping = {}
        current_index = start_index
        input_json = self.dict(to_camel_case=True, exclude_none=True)

        def process_object(obj, current_path=""):
            nonlocal current_index
            if isinstance(obj, dict):
                result = {}
                for key, value in obj.items():
                    full_key = f"{current_path}.{key}" if current_path else key
                    if full_key not in key_mapping:
                        key_mapping[full_key] = current_index
                        keys.append(full_key)
                        current_index += 1
                    result[key_mapping[full_key]] = process_object(
                        value, full_key
                    )
                return result
            elif isinstance(obj, list):
                return [process_object(item, current_path) for item in obj]
            else:
                key_idx = key_mapping[current_path]
                if key_idx not in defaults:
                    defaults[key_idx] = obj
                return obj

        # Procesar el JSON de entrada
        data = process_object(input_json)

        # Estructura final
        cbor_structure = {
            0: keys,
            1: defaults,
            2: data,
        }

        return cbor_structure
