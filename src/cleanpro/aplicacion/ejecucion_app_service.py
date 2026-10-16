from ..dominio.errores import ErrorDeDominio
from ..dominio.repositorios import ConfiguracionRepository, ServicioRepository
from ..dominio.servicios_de_dominio import PoliticaDeExtras
from ..dominio.valores import Actor, Rol
from .comandos import ConfirmarExtra, RegistrarExtra
from .resultado import Resultado
from .unit_of_work import UnitOfWork


class EjecucionAppService:
    """CU-04. La politica decide si hay catalogo; el Servicio registra el extra."""

    def __init__(self, servicios: ServicioRepository, politica: PoliticaDeExtras,
                 configuraciones: ConfiguracionRepository, uow: UnitOfWork):
        self._servicios = servicios
        self._politica = politica
        self._configuraciones = configuraciones
        self._uow = uow

    def registrarExtra(self, comando: RegistrarExtra) -> Resultado:
        try:
            servicio = self._servicios.obtenerPorFolio(comando.folio)
            politicas = self._configuraciones.obtenerPoliticasVigentes()
            requiere = self._politica.requiereConfirmacion(comando.descripcion, politicas)
            actor = Actor(comando.supervisor_id, Rol.SUPERVISOR)
            extra = servicio.registrarExtra(comando.descripcion, requiere, actor)
            eventos = servicio.extraerEventos()
            self._servicios.guardar(servicio)
            self._uow.commit()
            return Resultado.exitoso(extra.estado.value, eventos)
        except ErrorDeDominio as error:
            self._uow.rollback()
            return Resultado.fallido(error)

    def confirmarExtra(self, comando: ConfirmarExtra) -> Resultado:
        try:
            servicio = self._servicios.obtenerPorFolio(comando.folio)
            servicio.confirmarExtra(comando.extra_id,
                                    Actor(comando.coordinador_id, Rol.COORDINADOR))
            eventos = servicio.extraerEventos()
            self._servicios.guardar(servicio)
            self._uow.commit()
            return Resultado.exitoso("Confirmado", eventos)
        except ErrorDeDominio as error:
            self._uow.rollback()
            return Resultado.fallido(error)
