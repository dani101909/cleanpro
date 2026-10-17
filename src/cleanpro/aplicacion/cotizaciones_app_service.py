from ..dominio.errores import ErrorDeDominio, SinPermiso
from ..dominio.repositorios import CotizacionRepository, ServicioRepository
from ..dominio.servicio import Servicio
from .comandos import AceptarCotizacion
from .resultado import Resultado
from .unit_of_work import UnitOfWork


class CotizacionesAppService:
    """CU-01. Unica operacion con dos Aggregates (excepcion documentada en ADR-002)."""

    def __init__(self, cotizaciones: CotizacionRepository,
                 servicios: ServicioRepository, uow: UnitOfWork):
        self._cotizaciones = cotizaciones
        self._servicios = servicios
        self._uow = uow

    def aceptarCotizacion(self, comando: AceptarCotizacion) -> Resultado:
        try:
            cotizacion = self._cotizaciones.obtenerPorFolio(comando.folio)
            if cotizacion.cliente_id != comando.cliente_id:
                raise SinPermiso("Solo el cliente de la cotizacion puede aceptarla")
            cotizacion.aceptar()                                   # BR-01, C4
            servicio = Servicio.programarDesde(cotizacion, comando.fecha)   # S1
            eventos = cotizacion.extraerEventos() + servicio.extraerEventos()
            self._cotizaciones.guardar(cotizacion)
            self._servicios.guardar(servicio)
            self._uow.commit()
            return Resultado.exitoso(servicio.estado.value, eventos)
        except ErrorDeDominio as error:
            self._uow.rollback()
            return Resultado.fallido(error)
