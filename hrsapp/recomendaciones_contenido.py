from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from hrsapp.models.paciente import Paciente
from hrsapp.models.historial_contacto import HistorialContacto
from hrsapp.models.seguimiento_medicamento import SeguimientoMedicamento
from hrsapp.models.asignacion_actividad import AsignacionActividad
from hrsapp.models.accion_gestor import AccionGestor
from hrsapp.models.resultado_contacto import ResultadoContacto

# CONSTANTES GLOBALES

# Fecha actual
FECHA_ACTUAL = datetime.now().date()
# Puntaje asignado a las recomendaciones
PUNTAJE_RECOMENDACIONES = [
    (0.5, "Baja relevancia"),
    (1, "Alta relevancia"),
]
# Resultados de contacto
CONTACTO_EXITOSO_NAME = "Exitoso"
LLAMAR_MAS_TARDE_NAME = "Llamar más tarde"
# Tipo de motivo de las contactos que realiza un gestor
TIPO_MOTIVO_CHOICES = [
    (1, "Asignación"),
    (2, "Medicamento"),
    (3, "Diagnóstico"),
    (4, "Otro"),
]
# Tipos de acciones de gestor
CORROBORAR_ASISTENCIA_NAME = "Corroborar asistencia"
REPROGRAMAR_ACTIVIDAD_NAME = "Reprogramar actividad"
VERIFICAR_ESTADO_NAME = "Verificar estado del paciente"
RECORDAR_DESPACHO_NAME = "Recordar despacho"


# FUNCIONES DE RECOMENDACIONES

# RECOMENDACIONES BASADAS EN CONTENIDO


# Recomendacion de "llamar mas tarde"
def recomendacion_contenido_llamar_mas_tarde(gestor_id):
    # Variables
    recomendacion_data = []
    recomendaciones_llamar_mas_tarde = []

    # Obtener los pacientes del gestor
    pacientes = Paciente.objects.filter(gestor=gestor_id)

    try:
        contacto_exitoso = ResultadoContacto.objects.get(nombre=CONTACTO_EXITOSO_NAME)
        llamar_mas_tarde = ResultadoContacto.objects.get(nombre=LLAMAR_MAS_TARDE_NAME)
        accion_llamar_mas_tarde = AccionGestor.objects.get(
            nombre=LLAMAR_MAS_TARDE_NAME, estado=True
        )
    except ObjectDoesNotExist:
        # Si no se encuentra alguno de los resultados de contacto, retornar lista vacía
        return recomendaciones_llamar_mas_tarde

    for paciente in pacientes:
        # Obtener el historial de contacto con el paciente
        historialContacto = HistorialContacto.objects.filter(paciente=paciente.id)
        # Generar recomendaciones respecto a si hay que volver a llamar al paciente
        for contacto in historialContacto:
            # Si existe un contacto con resultado "llamar más tarde" en los últimos 7 días
            if contacto.resultado_contacto.id == llamar_mas_tarde.id and (
                0 <= (FECHA_ACTUAL - contacto.fecha).days <= 7
            ):
                # Filtra si existe contacto en los últimos 7 días con el motivo del contacto y resultado exitoso
                existe_contacto = HistorialContacto.objects.filter(
                    paciente=paciente.id,
                    resultado_contacto=contacto_exitoso.id,
                    tipo_motivo=contacto.tipo_motivo,
                    motivo=contacto.motivo,
                    fecha__gte=FECHA_ACTUAL - timedelta(days=7),
                ).exists()
                # Si no existe contacto, se agrega la recomendacion a la lista
                if not existe_contacto:
                    recomendacion_data = {
                        "fecha": FECHA_ACTUAL.strftime("%d-%m-%Y"),
                        "paciente": paciente.nombres
                        + " "
                        + paciente.apellido1
                        + " "
                        + paciente.apellido2,
                        "tipo_motivo": contacto.tipo_motivo,
                        "motivo": contacto.motivo,
                        "puntaje": PUNTAJE_RECOMENDACIONES[0][0] * paciente.riesgo,
                        "accion_gestor": accion_llamar_mas_tarde.nombre,
                        "fecha_asignacion": "N/A",
                    }
                    recomendaciones_llamar_mas_tarde.append(recomendacion_data)
    return recomendaciones_llamar_mas_tarde


# Recomendaciones basadas en contenido de tipo_motivo "asignación"
def recomendaciones_contenido_asignacion(gestor_id):
    # Variables
    recomendacion_data = []
    recomendaciones_asignacion = []

    # Obtener los pacientes del gestor
    pacientes = Paciente.objects.filter(gestor=gestor_id)
    try:
        contacto_exitoso = ResultadoContacto.objects.get(nombre=CONTACTO_EXITOSO_NAME)
        corroborar_asistencia = AccionGestor.objects.get(
            nombre=CORROBORAR_ASISTENCIA_NAME
        )
        reprogramar_actividad = AccionGestor.objects.get(
            nombre=REPROGRAMAR_ACTIVIDAD_NAME
        )
    except ObjectDoesNotExist:
        # Si no se encuentra alguno de los resultados de contacto, retornar lista vacía
        return recomendaciones_asignacion

    for paciente in pacientes:
        # Obtener las asignaciones de actividades del paciente
        asignacionesActividades = AsignacionActividad.objects.filter(
            paciente=paciente.id
        )
        # Generar recomendaciones respecto a las actividades asignadas
        for asignacion in asignacionesActividades:
            # Recomendaciones para confirmar asistencia

            # Si la actividad asignada es dentro de los próximos 7 días
            if 1 <= (asignacion.fecha_actividad - FECHA_ACTUAL).days <= 7 and (
                asignacion.estado == 1
            ):
                # Filtra si existe contacto en los últimos 7 días con el motivo de la asignación
                # y la acción de gestor "Confirmar asistencia"
                existe_contacto = HistorialContacto.objects.filter(
                    paciente=paciente.id,
                    resultado_contacto=contacto_exitoso.id,
                    fecha__gte=FECHA_ACTUAL - timedelta(days=7),
                    motivo=asignacion.actividad_medica.nombre,
                    accion_gestor=corroborar_asistencia.id,
                ).exists()
                # Si no existe contacto, se agrega la recomendacion a la lista
                if not existe_contacto:
                    recomendacion_data = {
                        "fecha": FECHA_ACTUAL.strftime("%d-%m-%Y"),
                        "paciente": paciente.nombres
                        + " "
                        + paciente.apellido1
                        + " "
                        + paciente.apellido2,
                        "tipo_motivo": TIPO_MOTIVO_CHOICES[0][1],
                        "motivo": asignacion.actividad_medica.nombre,
                        "puntaje": PUNTAJE_RECOMENDACIONES[0][0] * paciente.riesgo,
                        "accion_gestor": corroborar_asistencia.nombre,
                        "fecha_asignacion": asignacion.fecha_actividad.strftime(
                            "%d-%m-%Y"
                        ),
                    }
                    recomendaciones_asignacion.append(recomendacion_data)

            # Recomendaciones por actividades canceladas

            # Si la actividad asignada era dentro de los últimos 7 días
            if 1 <= (FECHA_ACTUAL - asignacion.fecha_actividad).days <= 7 and (
                asignacion.estado == 1 or asignacion.estado == 4
            ):
                # Filtra si existe contacto en los últimos 7 días con el motivo de la asignación
                # y la acción de gestor "Reprogramar actividad"
                existe_contacto = HistorialContacto.objects.filter(
                    paciente=paciente.id,
                    resultado_contacto=contacto_exitoso.id,
                    fecha__gte=FECHA_ACTUAL - timedelta(days=7),
                    motivo=asignacion.actividad_medica.nombre,
                    accion_gestor=reprogramar_actividad.id,
                ).exists()
                # Si no existe contacto, se agrega la recomendacion a la lista
                if not existe_contacto:
                    recomendacion_data = {
                        "fecha": FECHA_ACTUAL.strftime("%d-%m-%Y"),
                        "paciente": paciente.nombres
                        + " "
                        + paciente.apellido1
                        + " "
                        + paciente.apellido2,
                        "tipo_motivo": TIPO_MOTIVO_CHOICES[0][1],
                        "motivo": asignacion.actividad_medica.nombre,
                        "puntaje": PUNTAJE_RECOMENDACIONES[1][0] * paciente.riesgo,
                        "accion_gestor": reprogramar_actividad.nombre,
                        "fecha_asignacion": asignacion.fecha_actividad.strftime(
                            "%d-%m-%Y"
                        ),
                    }
                    recomendaciones_asignacion.append(recomendacion_data)

    # Si las recomendaciones de asignacion es una lista vacía
    if not recomendaciones_asignacion:
        # Mostrar mensaje en consola
        print("No hay recomendaciones de asignación")
    # Entrega las recomendaciones de asignación
    return recomendaciones_asignacion


def recomendaciones_contenido_medicamento(gestor_id):
    # Variables
    recomendacion_data = []
    recomendaciones_medicamento = []

    # Obtener los pacientes del gestor
    pacientes = Paciente.objects.filter(gestor=gestor_id)
    try:
        contacto_exitoso = ResultadoContacto.objects.get(nombre=CONTACTO_EXITOSO_NAME)
        recordar_despacho = AccionGestor.objects.get(nombre=RECORDAR_DESPACHO_NAME)
        verificar_estado = AccionGestor.objects.get(nombre=VERIFICAR_ESTADO_NAME)
    except ObjectDoesNotExist:
        # Si no se encuentra alguno de los resultados de contacto, retornar lista vacía
        return recomendaciones_medicamento

    for paciente in pacientes:
        # Obtener el seguimiento de medicamentos del paciente
        seguimientoMedicamentos = SeguimientoMedicamento.objects.filter(
            paciente=paciente.id
        )
        # Generar recomendaciones respecto a los medicamentos asignados
        for medicamento in seguimientoMedicamentos:
            # Recomendaciones para recordar despacho de medicamentos

            # Si el medicamento se debe despachar dentro de los próximos 7 días
            if 1 < (medicamento.proximo_despacho - FECHA_ACTUAL).days < 7:
                # Filtra si existe contacto en los últimos 7 días con el motivo del medicamento
                # y la acción de gestor "Recordar despacho de medicamentos"
                existe_contacto = HistorialContacto.objects.filter(
                    paciente=paciente.id,
                    resultado_contacto=contacto_exitoso.id,
                    fecha__gte=FECHA_ACTUAL - timedelta(days=7),
                    motivo=medicamento.medicamento.nombre,
                    accion_gestor=recordar_despacho.id,
                ).exists()
                # Si no existe contacto, se agrega la recomendacion a la lista
                if not existe_contacto:
                    recomendacion_data = {
                        "fecha": FECHA_ACTUAL.strftime("%d-%m-%Y"),
                        "paciente": paciente.nombres
                        + " "
                        + paciente.apellido1
                        + " "
                        + paciente.apellido2,
                        "tipo_motivo": TIPO_MOTIVO_CHOICES[1][1],
                        "motivo": medicamento.medicamento.nombre,
                        "puntaje": PUNTAJE_RECOMENDACIONES[0][0] * paciente.riesgo,
                        "accion_gestor": recordar_despacho.nombre,
                        "fecha_asignacion": "N/A",
                    }
                    recomendaciones_medicamento.append(recomendacion_data)

            # Recomendaciones por medicamento no retirado

            # Si el medicamento fue despachado dentro de los últimos 7 días
            # y no ha sido retirado
            if (
                1 <= (FECHA_ACTUAL - medicamento.proximo_despacho).days <= 7
                and medicamento.estado == 2
            ):
                # Filtra si existe contacto en los últimos 7 días con el motivo del medicamento
                # y la acción de gestor "Verificar estado del paciente"
                existe_contacto = HistorialContacto.objects.filter(
                    paciente=paciente.id,
                    resultado_contacto=contacto_exitoso.id,
                    fecha__gte=FECHA_ACTUAL - timedelta(days=7),
                    motivo=medicamento.medicamento.nombre,
                    accion_gestor=verificar_estado.id,
                ).exists()
                # Si no existe contacto, se agrega la recomendacion a la lista
                if not existe_contacto:
                    recomendacion_data = {
                        "fecha": FECHA_ACTUAL.strftime("%d-%m-%Y"),
                        "paciente": paciente.nombres
                        + " "
                        + paciente.apellido1
                        + " "
                        + paciente.apellido2,
                        "tipo_motivo": TIPO_MOTIVO_CHOICES[1][1],
                        "motivo": medicamento.medicamento.nombre,
                        "puntaje": PUNTAJE_RECOMENDACIONES[1][0] * paciente.riesgo,
                        "accion_gestor": verificar_estado.nombre,
                        "fecha_asignacion": "N/A",
                    }
                    recomendaciones_medicamento.append(recomendacion_data)

    # Si las recomendaciones de medicamento es una lista vacía
    if not recomendaciones_medicamento:
        # Mostrar mensaje en consola
        print("No hay recomendaciones de medicamento")

    # Entrega las recomendaciones de medicamento
    return recomendaciones_medicamento


# Unión de recomendaciones de asignación y medicamento
def recomendaciones_contenido(gestor_id):
    recomendaciones_asignacion = recomendaciones_contenido_asignacion(gestor_id)
    recomendaciones_medicamento = recomendaciones_contenido_medicamento(gestor_id)
    recomendacion_llamar_mas_tarde = recomendacion_contenido_llamar_mas_tarde(gestor_id)
    recomendaciones_contenido = (
        recomendaciones_asignacion
        + recomendaciones_medicamento
        + recomendacion_llamar_mas_tarde
    )
    # Ordenar la lista de recomendaciones por el campo "puntaje" en orden descendente
    recomendaciones_contenido_ordenadas = sorted(
        recomendaciones_contenido, key=lambda x: x.get("puntaje", 0), reverse=True
    )
    return recomendaciones_contenido_ordenadas
