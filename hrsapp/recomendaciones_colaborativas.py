import numpy as np
from dateutil.relativedelta import relativedelta
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from hrsapp.models import Paciente, Diagnostico, HistorialContacto

# VARIABLES GLOBALES

# Fecha actual
FECHA_ACTUAL = datetime.now().date()
# Puntaje asignado a las recomendaciones
PUNTAJE_RECOMENDACIONES = [
    (0.5, "Baja relevancia"),
    (1, "Alta relevancia"),
]
# Tipo de motivo de las contactos que realiza un gestor
TIPO_MOTIVO_CHOICES = HistorialContacto.TIPO_MOTIVO_CHOICES

# FUNCIONES


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
    diagnosticos_recomendados = []
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
    n_pacientes_similares = 3
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

    # Descartar los diagnosticos cuya descripcion incluya la palabra "hombres" si el paciente es mujer
    if paciente_objetivo.sexo == "2":
        diagnosticos_recomendados = [
            diagnostico
            for diagnostico in diagnosticos_recomendados
            if "hombres" not in Diagnostico.objects.get(codigo=diagnostico).descripcion
        ]
    # Descartar los diagnosticos cuya descripcion incluya la palabra "mujeres" si el paciente es hombre
    elif paciente_objetivo.sexo == "1":
        diagnosticos_recomendados = [
            diagnostico
            for diagnostico in diagnosticos_recomendados
            if "mujeres" not in Diagnostico.objects.get(codigo=diagnostico).descripcion
        ]

    # Limitar el número de recomendaciones a 3
    diagnosticos_recomendados = list(diagnosticos_recomendados)[:3]

    # Generar recomendaciones
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
