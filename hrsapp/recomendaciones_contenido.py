from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from hrsapp.models.paciente import Paciente
from hrsapp.models.historial_contacto import HistorialContacto
from hrsapp.models.seguimiento_medicamento import SeguimientoMedicamento
from hrsapp.models.asignacion_actividad import AsignacionActividad
from hrsapp.models.accion_gestor import AccionGestor

# CONSTANTES GLOBALES

# Fecha actual
FECHA_ACTUAL = datetime.now().date()
# Puntaje asignado a las recomendaciones
PUNTAJE_RECOMENDACIONES = [
    (0.5, "Baja relevancia"),
    (1, "Alta relevancia"),
]
# Resultados de contacto
RESULTADO_CONTACTO_CHOICES = HistorialContacto.RESULTADO_CONTACTO_CHOICES
# Tipo de motivo de las contactos que realiza un gestor
TIPO_MOTIVO_CHOICES = HistorialContacto.TIPO_MOTIVO_CHOICES
# Estados de las actividades
ESTADO_ACTIVIDAD_CHOICES = AsignacionActividad.ESTADO_CHOICES
# Tipos de acciones de gestor
CORROBORAR_ASISTENCIA_NAME = "Corroborar asistencia"
REPROGRAMAR_ACTIVIDAD_NAME = "Reprogramar actividad"
ALERTAR_SUPERVISOR_NAME = "Alertar a supervisor"
VERIFICAR_ESTADO_NAME = "Verificar estado del paciente"
RECORDAR_DESPACHO_NAME = "Recordar despacho"


# FUNCIONES

# RECOMENDACIONES BASADAS EN CONTENIDO

# RECOMENDACIONES ENFOCADAS EN CONTACTOS


# Recomendacion de "llamar mas tarde"
def generar_recomendacion_contenido_llamar_mas_tarde(gestor_id):
    # Variables
    recomendacion_data = []
    recomendaciones_llamar_mas_tarde = []

    # Obtener los pacientes del gestor
    pacientes = Paciente.objects.filter(gestor=gestor_id)

    for paciente in pacientes:
        # Obtener el historial de contacto con el paciente que esté dentro de los últimos 7 días y con resultado "Llamar más tarde"
        historial_contacto = HistorialContacto.objects.filter(
            paciente=paciente.id,
            fecha__gte=FECHA_ACTUAL - timedelta(days=7),
            resultado_contacto=RESULTADO_CONTACTO_CHOICES[1][0],
        )
        # Generar recomendaciones respecto a los contactos realizados
        for contacto in historial_contacto:
            print(contacto.tipo_motivo, contacto.motivo)
            # Filtra si existe contacto en los últimos 7 días con el motivo del contacto y resultado "Exitoso"
            existe_contacto = HistorialContacto.objects.filter(
                paciente=paciente.id,
                resultado_contacto=RESULTADO_CONTACTO_CHOICES[0][0],
                fecha__gte=FECHA_ACTUAL - timedelta(days=7),
                tipo_motivo=contacto.tipo_motivo,
                motivo=contacto.motivo,
            ).exists()
            # Si no existe contacto, se agrega la recomendacion a la lista
            if not existe_contacto:
                recomendacion_data = {
                    "fecha": contacto.fecha.strftime("%d-%m-%Y"),
                    "paciente": paciente.nombres
                    + " "
                    + paciente.apellido1
                    + " "
                    + paciente.apellido2,
                    "tipo_motivo": TIPO_MOTIVO_CHOICES[contacto.tipo_motivo - 1][1],
                    "motivo": contacto.motivo,
                    "puntaje": PUNTAJE_RECOMENDACIONES[0][0] * paciente.riesgo,
                    "accion_gestor": "Llamar más tarde",
                    "fecha_asignacion": "N/A",
                }
                recomendaciones_llamar_mas_tarde.append(recomendacion_data)

    if not recomendaciones_llamar_mas_tarde:
        print("No hay recomendaciones de llamar más tarde")
    return recomendaciones_llamar_mas_tarde


# RECOMENDACIONES ENFOCADAS EN ASIGNACIONES


# Recomendaciones de "corroborar asistencia"
def generar_recomendaciones_corroborar_asistencia(gestor_id):
    # Listas
    recomendacion_data = []
    recomendaciones_corroborar_asistencia = []

    # Comprobar que existe la acción de gestor "Corroborar asistencia"
    try:
        corroborar_asistencia = AccionGestor.objects.get(
            nombre=CORROBORAR_ASISTENCIA_NAME
        )
    except ObjectDoesNotExist:
        return recomendaciones_corroborar_asistencia

    # Obtener los pacientes del gestor
    pacientes = Paciente.objects.filter(gestor=gestor_id)

    for paciente in pacientes:
        # Obtener las asignaciones de actividades del paciente
        asignaciones_actividades = AsignacionActividad.objects.filter(
            paciente=paciente.id
        )
        # Obtener las asignaciones de actividades del paciente que estén dentro de los próximos 7 días y con estado "Asignada"
        actividades_asignadas = asignaciones_actividades.filter(
            fecha_actividad__gte=FECHA_ACTUAL,
            fecha_actividad__lte=FECHA_ACTUAL + timedelta(days=7),
            estado=1,
        )
        # Generar recomendaciones respecto a las actividades asignadas
        for actividad in actividades_asignadas:
            # Filtra si existe contacto en los últimos 7 días con el motivo de la asignación
            # y la acción de gestor "Confirmar asistencia"
            existe_contacto = HistorialContacto.objects.filter(
                paciente=paciente.id,
                resultado_contacto=RESULTADO_CONTACTO_CHOICES[0][0],
                fecha__gte=FECHA_ACTUAL - timedelta(days=7),
                motivo=actividad.actividad_medica.nombre,
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
                    "motivo": actividad.actividad_medica.nombre,
                    "puntaje": PUNTAJE_RECOMENDACIONES[0][0] * paciente.riesgo,
                    "accion_gestor": corroborar_asistencia.nombre,
                    "fecha_asignacion": actividad.fecha_actividad.strftime("%d-%m-%Y"),
                }
                recomendaciones_corroborar_asistencia.append(recomendacion_data)

    if not recomendaciones_corroborar_asistencia:
        print("No hay recomendaciones de corroborar asistencia")
    return recomendaciones_corroborar_asistencia


# Recomendaciones de "reprogramar actividad"
def generar_recomendaciones_reprogramar_actividad(gestor_id):
    # Listas
    recomendacion_data = []
    recomendaciones_reprogramar_actividad = []

    # Comprobar que existe la acción de gestor "Reprogramar actividad"
    try:
        reprogramar_actividad = AccionGestor.objects.get(
            nombre=REPROGRAMAR_ACTIVIDAD_NAME
        )
    except ObjectDoesNotExist:
        return recomendaciones_reprogramar_actividad

    # Obtener los pacientes del gestor
    pacientes = Paciente.objects.filter(gestor=gestor_id)

    for paciente in pacientes:
        # Obtener las asignaciones de actividades del paciente
        asignaciones_actividades = AsignacionActividad.objects.filter(
            paciente=paciente.id
        )
        # Obtener las asignaciones de actividades del paciente que estén dentro de los últimos 7 días y con estado distinto a "Realizada"
        actividades_asignadas = asignaciones_actividades.filter(
            fecha_actividad__gte=FECHA_ACTUAL,
            fecha_actividad__lte=FECHA_ACTUAL - timedelta(days=7),
            estado=1,
        )
        # Generar recomendaciones respecto a las actividades asignadas
        for actividad in actividades_asignadas:
            # Filtra si existe contacto en los últimos 7 días con el motivo de la asignación
            # y la acción de gestor "Reprogramar actividad"
            existe_contacto = HistorialContacto.objects.filter(
                paciente=paciente.id,
                resultado_contacto=RESULTADO_CONTACTO_CHOICES[0][0],
                fecha__gte=FECHA_ACTUAL - timedelta(days=7),
                motivo=actividad.actividad_medica.nombre,
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
                    "motivo": actividad.actividad_medica.nombre,
                    "puntaje": PUNTAJE_RECOMENDACIONES[1][0] * paciente.riesgo,
                    "accion_gestor": reprogramar_actividad.nombre,
                    "fecha_asignacion": actividad.fecha_actividad.strftime("%d-%m-%Y"),
                }
                recomendaciones_reprogramar_actividad.append(recomendacion_data)

    if not recomendaciones_reprogramar_actividad:
        print("No hay recomendaciones de reprogramar actividad")
    return recomendaciones_reprogramar_actividad


# Recomendaciones respecto a las asignaciones no realizadas o canceladas
def generar_recomendaciones_asignaciones_no_completadas(gestor_id):
    # Listas
    recomendacion_data = []
    recomendaciones_asignaciones_no_completadas = []
    n_actividades_realizadas = 0
    n_actividades_no_realizadas_o_canceladas = 0

    # Comprobar que existe la acción de gestor "Alertar a supervisor"
    try:
        alertar_supervisor = AccionGestor.objects.get(nombre=ALERTAR_SUPERVISOR_NAME)
    except ObjectDoesNotExist:
        alertar_supervisor = None

    # Comprobar que existe la acción de gestor "Verificar estado del paciente"
    try:
        verificar_estado = AccionGestor.objects.get(nombre=VERIFICAR_ESTADO_NAME)
    except ObjectDoesNotExist:
        verificar_estado = None

    # Obtener los pacientes del gestor
    pacientes = Paciente.objects.filter(gestor=gestor_id)

    for paciente in pacientes:
        # Obtener las asignaciones de actividades del paciente
        asignaciones_actividades = AsignacionActividad.objects.filter(
            paciente=paciente.id
        )
        # Contar la cantidad de actividades realizadas
        n_actividades_realizadas = asignaciones_actividades.filter(estado=2).count()
        # Contar la cantidad de actividades no realizadas o canceladas
        n_actividades_no_realizadas_o_canceladas = asignaciones_actividades.filter(
            estado__in=[3, 4]
        ).count()
        # Si la cantidad de actividades no realizadas o canceladas es mayor a la cantidad de actividades realizadas
        if n_actividades_no_realizadas_o_canceladas > n_actividades_realizadas:
            # Si alertar_supervisor no es None y riesgo del paciente es 3
            if alertar_supervisor and paciente.riesgo == 3:
                recomendacion_data = {
                    "fecha": FECHA_ACTUAL.strftime("%d-%m-%Y"),
                    "paciente": paciente.nombres
                    + " "
                    + paciente.apellido1
                    + " "
                    + paciente.apellido2,
                    "tipo_motivo": TIPO_MOTIVO_CHOICES[0][1],
                    "motivo": "Actividades no realizadas",
                    "puntaje": PUNTAJE_RECOMENDACIONES[1][0] * paciente.riesgo,
                    "accion_gestor": alertar_supervisor.nombre,
                    "fecha_asignacion": "N/A",
                }
                recomendaciones_asignaciones_no_completadas.append(recomendacion_data)
            # Si verificar_estado no es None y riesgo del paciente es distinto de 3
            elif verificar_estado and paciente.riesgo != 3:
                recomendacion_data = {
                    "fecha": FECHA_ACTUAL.strftime("%d-%m-%Y"),
                    "paciente": paciente.nombres
                    + " "
                    + paciente.apellido1
                    + " "
                    + paciente.apellido2,
                    "tipo_motivo": TIPO_MOTIVO_CHOICES[0][1],
                    "motivo": "Actividades no realizadas",
                    "puntaje": PUNTAJE_RECOMENDACIONES[1][0] * paciente.riesgo,
                    "accion_gestor": verificar_estado.nombre,
                    "fecha_asignacion": "N/A",
                }
                recomendaciones_asignaciones_no_completadas.append(recomendacion_data)

    if not recomendaciones_asignaciones_no_completadas:
        print("No hay recomendaciones de alertar supervisor")
    return recomendaciones_asignaciones_no_completadas


# Recomendaciones sobre asignaciones de actividades
def generar_recomendaciones_asignacion(gestor_id):
    # Listas
    recomendaciones_asignacion = []

    # Obtener las recomendaciones de corroborar asistencia
    recomendaciones_corroborar_asistencia = (
        generar_recomendaciones_corroborar_asistencia(gestor_id)
    )
    # Obtener las recomendaciones de reprogramar actividad
    recomendaciones_reprogramar_actividad = (
        generar_recomendaciones_reprogramar_actividad(gestor_id)
    )
    # Obtener las recomendaciones por asignaciones no completadas
    recomendaciones_asignaciones_no_completadas = (
        generar_recomendaciones_asignaciones_no_completadas(gestor_id)
    )

    # Agregar las recomendaciones de corroborar asistencia a la lista de recomendaciones
    recomendaciones_asignacion = (
        recomendaciones_corroborar_asistencia
        + recomendaciones_reprogramar_actividad
        + recomendaciones_asignaciones_no_completadas
    )

    if not recomendaciones_asignacion:
        print("No hay recomendaciones de asignación")
    return recomendaciones_asignacion


# RECOMENDACIONES ENFOCADAS A MEDICAMENTOS


# Recomendaciones de "recordar despacho de medicamentos"
def generar_recomendaciones_recordar_despacho(gestor_id):
    # Listas
    recomendacion_data = []
    recomendaciones_recordar_despacho = []

    # Comprobar que existe la acción de gestor "Recordar despacho de medicamentos"
    try:
        recordar_despacho = AccionGestor.objects.get(nombre=RECORDAR_DESPACHO_NAME)
    except ObjectDoesNotExist:
        return recomendaciones_recordar_despacho

    # Obtener los pacientes del gestor
    pacientes = Paciente.objects.filter(gestor=gestor_id)

    for paciente in pacientes:
        # Obtener el seguimiento de medicamento del paciente que esté con fecha de despacho dentro de los próximos 7 días y estado "Al día"
        seguimiento_medicamento = SeguimientoMedicamento.objects.filter(
            paciente=paciente.id,
            proximo_despacho__gte=FECHA_ACTUAL,
            proximo_despacho__lte=FECHA_ACTUAL + timedelta(days=7),
            estado=1,
        )
        # Generar recomendaciones respecto a los medicamentos asignados
        for medicamento in seguimiento_medicamento:
            # Filtra si existe contacto en los últimos 7 días con el motivo del medicamento
            # y la acción de gestor "Recordar despacho de medicamentos"
            existe_contacto = HistorialContacto.objects.filter(
                paciente=paciente.id,
                resultado_contacto=RESULTADO_CONTACTO_CHOICES[0][0],
                fecha__gte=FECHA_ACTUAL - timedelta(days=7),
                tipo_motivo=TIPO_MOTIVO_CHOICES[1][0],
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
                recomendaciones_recordar_despacho.append(recomendacion_data)

    if not recomendaciones_recordar_despacho:
        print("No hay recomendaciones de recordar despacho")
    return recomendaciones_recordar_despacho


# Recomendaciones de "verificar estado del paciente"
def generar_recomendaciones_verificar_estado(gestor_id):
    # Listas
    recomendacion_data = []
    recomendaciones_verificar_estado = []

    # Comprobar que existe la acción de gestor "Verificar estado del paciente"
    try:
        verificar_estado = AccionGestor.objects.get(nombre=VERIFICAR_ESTADO_NAME)
    except ObjectDoesNotExist:
        return recomendaciones_verificar_estado

    # Obtener los pacientes del gestor
    pacientes = Paciente.objects.filter(gestor=gestor_id)

    for paciente in pacientes:
        # Obtener el seguimiento de medicamento del paciente que esté con fecha de despacho dentro de los últimos 7 días y estado "Al día"
        seguimiento_medicamento = SeguimientoMedicamento.objects.filter(
            paciente=paciente.id,
            proximo_despacho__gte=FECHA_ACTUAL - timedelta(days=7),
            proximo_despacho__lte=FECHA_ACTUAL,
            estado=1,
        )
        # Generar recomendaciones respecto a los medicamentos asignados
        for medicamento in seguimiento_medicamento:
            # Filtra si existe contacto en los últimos 7 días con el motivo del medicamento
            # y la acción de gestor "Verificar estado del paciente"
            existe_contacto = HistorialContacto.objects.filter(
                paciente=paciente.id,
                resultado_contacto=RESULTADO_CONTACTO_CHOICES[0][0],
                fecha__gte=FECHA_ACTUAL - timedelta(days=7),
                tipo_motivo=TIPO_MOTIVO_CHOICES[1][0],
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
                recomendaciones_verificar_estado.append(recomendacion_data)

    if not recomendaciones_verificar_estado:
        print("No hay recomendaciones de verificar estado")
    return recomendaciones_verificar_estado


# Recomendaciones sobre medicamentos
def generar_recomendaciones_medicamento(gestor_id):
    # Listas
    recomendaciones_medicamento = []

    # Obtener las recomendaciones de recordar despacho
    recomendaciones_recordar_despacho = generar_recomendaciones_recordar_despacho(
        gestor_id
    )
    # Obtener las recomendaciones de verificar estado
    recomendaciones_verificar_estado = generar_recomendaciones_verificar_estado(
        gestor_id
    )

    # Agregar las recomendaciones de recordar despacho a la lista de recomendaciones
    recomendaciones_medicamento = (
        recomendaciones_recordar_despacho + recomendaciones_verificar_estado
    )

    if not recomendaciones_medicamento:
        print("No hay recomendaciones de medicamento")
    return recomendaciones_medicamento


# Unión de recomendaciones de asignación y medicamento
def recomendaciones_contenido(gestor_id):
    # Listas
    recomendaciones = []

    # Obtener las recomendaciones de llamar más tarde
    recomendaciones_llamar_mas_tarde = generar_recomendacion_contenido_llamar_mas_tarde(
        gestor_id
    )
    # Obtener las recomendaciones de asignación
    recomendaciones_asignacion = generar_recomendaciones_asignacion(gestor_id)
    # Obtener las recomendaciones de medicamento
    recomendaciones_medicamento = generar_recomendaciones_medicamento(gestor_id)

    # Agregar las recomendaciones de asignación y medicamento a la lista de recomendaciones
    recomendaciones = (
        recomendaciones_llamar_mas_tarde
        + recomendaciones_asignacion
        + recomendaciones_medicamento
    )

    if not recomendaciones:
        print("No hay recomendaciones de contenido")
    else:
        # Ordenar la lista de recomendaciones por el campo "puntaje" en orden descendente
        recomendaciones = sorted(
            recomendaciones, key=lambda i: i["puntaje"], reverse=True
        )
    return recomendaciones
