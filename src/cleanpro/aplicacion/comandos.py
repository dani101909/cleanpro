"""Commands (CQRS): cada uno expresa la intencion completa de un caso de uso."""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AceptarCotizacion:                 # CU-01
    folio: object
    cliente_id: str
    fecha: object = None                 # FechaDeServicio; origen no definido en U2


@dataclass(frozen=True)
class ConfirmarCuadrilla:                # CU-02
    folio: object
    cuadrilla_id: str
    coordinador_id: str


@dataclass(frozen=True)
class ReportarAusencia:                  # CU-03
    folio: object
    empleado_id: str
    supervisor_id: str


@dataclass(frozen=True)
class ReasignarPersonal:                 # CU-03
    folio: object
    empleado_id: str
    sustituto_id: str                    # None si no hay reemplazo disponible
    admin_id: str


@dataclass(frozen=True)
class RegistrarExtra:                    # CU-04
    folio: object
    descripcion: str
    supervisor_id: str


@dataclass(frozen=True)
class ConfirmarExtra:                    # CU-04 (extra fuera de catalogo)
    folio: object
    extra_id: str
    coordinador_id: str


@dataclass(frozen=True)
class RevisarIncidencia:                 # prepara CU-05
    folio: object
    incidencia_id: str
    admin_id: str


@dataclass(frozen=True)
class CerrarParaFacturacion:             # CU-05
    folio: object
    admin_id: str
