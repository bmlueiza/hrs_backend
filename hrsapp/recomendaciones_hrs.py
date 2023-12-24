from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from hrsapp.models.recomendacion import Recomendacion
from hrsapp.models.paciente import Paciente
from hrsapp.models.historial_contacto import HistorialContacto
from hrsapp.models.historial_medicamento import HistorialMedicamento
from hrsapp.models.asignacion_actividad import AsignacionActividad
from hrsapp.models.diagnostico import Diagnostico
from hrsapp.models.gestor import Gestor
from hrsapp.models.accion_gestor import AccionGestor
from hrsapp.models.actividad_medica import ActividadMedica
from hrsapp.models.medicamento import Medicamento
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
CONTACTO_EXITOSO = ResultadoContacto.objects.get(nombre="Exitoso")
LLAMAR_MAS_TARDE = ResultadoContacto.objects.get(nombre="Llamar más tarde")
# Tipo de motivo de las contactos que realiza un gestor
TIPO_MOTIVO_CHOICES = [
    (1, "Asignación"),
    (2, "Medicamento"),
    (3, "Diagnóstico"),
    (4, "Otro"),
]
# Tipos de acciones de gestor
CORROBORAR_ASISTENCIA = AccionGestor.objects.get(nombre="Corroborar asistencia")
REPROGRAMAR_ACTIVIDAD = AccionGestor.objects.get(nombre="Reprogramar actividad")


# FUNCIONES DE RECOMENDACIONES

# RECOMENDACIONES BASADAS EN CONTENIDO


# Recomendacion de "llamar mas tarde"
def recomendacion_contenido_llamar_mas_tarde(gestor_id):
    # Variables
    recomendacion_data = []
    recomendaciones_llamar_mas_tarde = []

    # Obtener los pacientes del gestor
    pacientes = Paciente.objects.filter(gestor=gestor_id)

    for paciente in pacientes:
        # Obtener el historial de contacto con el paciente
        historialContacto = HistorialContacto.objects.filter(paciente=paciente.id)
        # Generar recomendaciones respecto a si hay que volver a llamar al paciente
        for contacto in historialContacto:
            # Si existe un contacto con resultado "llamar más tarde" en los últimos 7 días
            if contacto.resultado_contacto.id == LLAMAR_MAS_TARDE.id and (
                0 <= (FECHA_ACTUAL - contacto.fecha).days <= 7
            ):
                # Filtra si existe contacto en los últimos 7 días con el motivo del contacto y resultado exitoso
                existe_contacto = HistorialContacto.objects.filter(
                    paciente=paciente.id,
                    resultado_contacto=CONTACTO_EXITOSO.id,
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
                        "accion_gestor": LLAMAR_MAS_TARDE.nombre,
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
                    resultado_contacto=CONTACTO_EXITOSO.id,
                    fecha__gte=FECHA_ACTUAL - timedelta(days=7),
                    motivo=asignacion.actividad_medica.nombre,
                    accion_gestor=CORROBORAR_ASISTENCIA.id,
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
                        "accion_gestor": CORROBORAR_ASISTENCIA.nombre,
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
                    resultado_contacto=CONTACTO_EXITOSO.id,
                    fecha__gte=FECHA_ACTUAL - timedelta(days=7),
                    motivo=asignacion.actividad_medica.nombre,
                    accion_gestor=REPROGRAMAR_ACTIVIDAD.id,
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
                        "accion_gestor": REPROGRAMAR_ACTIVIDAD.nombre,
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


# Recomendaciones basadas en contenido de tipo_motivo "medicamento"
def recomendaciones_contenido_medicamento(gestor_id):
    # Variables
    recomendacion_data = []
    recomendaciones_medicamento = []

    # Obtener los pacientes del gestor
    pacientes = Paciente.objects.filter(gestor=gestor_id)

    for paciente in pacientes:
        # Obtener el historial de recomendaciones sobre el paciente
        recomendaciones_actuales = Recomendacion.objects.filter(paciente=paciente.id)
        # Obtener el historial de contacto del paciente
        historialContacto = HistorialContacto.objects.filter(paciente=paciente.id)

        # Obtener el historial de medicamentos del paciente
        historialMedicamentos = HistorialMedicamento.objects.filter(
            paciente=paciente.id
        )
        # Generar recomendaciones respecto a los medicamentos asignados
        for medicamento in historialMedicamentos:
            # Recomendaciones para recordar despacho de medicamentos
            accion_gestor = AccionGestor.objects.get(nombre="Recordar despacho")
            # Si el medicamento se debe despachar dentro de los próximos 7 días
            if 1 < (medicamento.proximo_despacho - FECHA_ACTUAL).days < 7:
                # Filtra si existe contacto en los últimos 7 días con el motivo del medicamento
                # y la acción de gestor "Recordar despacho de medicamentos"
                existe_contacto = HistorialContacto.objects.filter(
                    paciente=paciente.id,
                    resultado_contacto=CONTACTO_EXITOSO.id,
                    fecha__gte=FECHA_ACTUAL - timedelta(days=7),
                    motivo=medicamento.medicamento.nombre,
                    accion_gestor=accion_gestor.id,
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
                        "accion_gestor": accion_gestor.nombre,
                        "fecha_asignacion": "N/A",
                    }
                    recomendaciones_medicamento.append(recomendacion_data)
            # Recomendaciones por medicamento no retirado
            accion_gestor = AccionGestor.objects.get(
                nombre="Verificar estado del paciente"
            )
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
                    resultado_contacto=CONTACTO_EXITOSO.id,
                    fecha__gte=FECHA_ACTUAL - timedelta(days=7),
                    motivo=medicamento.medicamento.nombre,
                    accion_gestor=accion_gestor.id,
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
                        "accion_gestor": accion_gestor.nombre,
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


# RECOMENDACIONES COLABORATIVAS

# Recomendaciones basadas en colaboración de tipo_motivo "diagnóstico"


# Generar un vector con caracteristicas de un paciente
def get_vector_paciente(paciente_id):
    # Obtener el objeto paciente según su id
    paciente = Paciente.objects.get(id=paciente_id)

    # Calcular edad del paciente respecto a su fecha de nacimiento
    edad = relativedelta(FECHA_ACTUAL, paciente.fecha_nacimiento).years

    # Obtener todos los diagnosticos
    diagnosticos = Diagnostico.objects.all()

    # Obtener los códigos de los diagnosticos del paciente como una lista de codigos
    diagnosticos_paciente = set(paciente.diagnosticos.values_list("codigo", flat=True))

    # Vector de paciente
    vector_paciente = [
        paciente.sexo,
        paciente.riesgo,
        edad,
    ]

    # Agregar 1 si el paciente tiene el diagnostico, 0 si no lo tiene
    for diagnostico in diagnosticos:
        if diagnostico.codigo in diagnosticos_paciente:
            vector_paciente.append(1)
        else:
            vector_paciente.append(0)

    return vector_paciente


# Recomendaciones de prevención basadas en diagnósticos de pacientes con perfiles similares
def recomendaciones_colaborativas(paciente_id):
    # Variables
    similitudes = []
    recomendaciones = []
    recomendacion_data = []
    paciente_objetivo = Paciente.objects.get(id=paciente_id)
    # Obtener el vector con caracteristicas del paciente
    vector_paciente = np.array(get_vector_paciente(paciente_id))
    # Obtener el resto de pacientes
    pacientes = Paciente.objects.exclude(id=paciente_id)
    # Lista con similitudes de pacientes
    similitudes = []
    # Calcular la similitud entre el paciente y el resto de pacientes
    for paciente in pacientes:
        # Obtener el vector con caracteristicas del paciente
        vector_paciente2 = np.array(get_vector_paciente(paciente.id))
        # Calcular la similitud entre el paciente y el resto de pacientes
        similitud = cosine_similarity([vector_paciente], [vector_paciente2])
        # Agregar la similitud a la lista de similitudes
        similitudes.append((similitud[0][0], paciente.id))

    # Ordenar la lista de similitudes por el campo "similitud" en orden descendente
    similitudes_ordenadas = sorted(similitudes, reverse=True)
    # Obtener n pacientes más similares
    n_pacientes_similares = 5
    pacientes_similares = similitudes_ordenadas[:n_pacientes_similares]

    # Obtener los diagnosticos del paciente
    diagnosticos_paciente = Paciente.objects.get(id=paciente_id).diagnosticos.all()
    # Obtener los diagnosticos de los pacientes similares
    diagnosticos_pacientes_similares = set(
        Paciente.objects.filter(
            id__in=[paciente[1] for paciente in pacientes_similares]
        ).values_list("diagnosticos__codigo", flat=True)
    )
    # Obtener los diagnosticos que no tiene el paciente
    if diagnosticos_pacientes_similares and diagnosticos_paciente:
        diagnosticos_recomendados = diagnosticos_pacientes_similares.difference(
            set(diagnosticos_paciente.values_list("codigo", flat=True))
        )
    for diagnostico in diagnosticos_recomendados:
        recomendacion_data = {
            "fecha": FECHA_ACTUAL.strftime("%d-%m-%Y"),
            "paciente": paciente_objetivo.nombres
            + " "
            + paciente_objetivo.apellido1
            + " "
            + paciente_objetivo.apellido2,
            "tipo_motivo": TIPO_MOTIVO_CHOICES[2][1],
            "motivo": Diagnostico.objects.get(codigo=diagnostico).codigo,
            "puntaje": PUNTAJE_RECOMENDACIONES[1][0] * paciente_objetivo.riesgo,
            "accion_gestor": "Acciones preventivas",
            "fecha_asignacion": "N/A",
        }
        recomendaciones.append(recomendacion_data)

    return recomendaciones
