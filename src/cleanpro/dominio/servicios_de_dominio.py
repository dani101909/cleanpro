"""Domain Services: reglas que no pertenecen a una sola entidad."""
from .configuracion import ConfiguracionDePoliticas
from .cuadrilla import Cuadrilla
from .repositorios import ServicioRepository
from .valores import FechaDeServicio


class AsignadorDeCuadrilla:
    """Verifica que la cuadrilla este libre ese dia (US-04, US-05, Q1).

    Compromiso documentado en la revision SOLID: consulta una abstraccion
    (ServicioRepository), no SQL.
    """

    def __init__(self, servicios: ServicioRepository):
        self._servicios = servicios

    def estaLibre(self, cuadrilla: Cuadrilla, fecha: FechaDeServicio) -> bool:
        confirmados = self._servicios.obtenerConfirmadosPorFecha(fecha)
        return all(s.cuadrilla_id != cuadrilla.id for s in confirmados)


class PoliticaDeExtras:
    """Decide si un extra requiere confirmacion del coordinador (BR-04).

    Por ahora aplica solo el criterio de catalogo (US-10). El umbral de
    "precio significativo" sigue pendiente y vive en la configuracion.
    """

    def requiereConfirmacion(self, descripcion: str,
                             politicas: ConfiguracionDePoliticas) -> bool:
        return descripcion not in politicas.catalogo_de_extras
