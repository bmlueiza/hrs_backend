from rest_framework import generics
from rest_framework.response import Response
from hrsapp.models.paciente import Paciente
from hrsapp.recomendaciones_hrs import recomendaciones_contenido
from hrsapp.recomendaciones_hrs import recomendaciones_colaborativas


# Leer Recomendaciones de un gestor en específico
class RecomendacionGestorListView(generics.ListAPIView):
    def get(self, request, gestor_id, *args, **kwargs):
        try:
            # Llama a tu función de recomendaciones_contenido con el gestor_id proporcionado
            recomendaciones = recomendaciones_contenido(gestor_id)

            # Crea un diccionario con la lista de recomendaciones
            response_data = {
                "recomendaciones": recomendaciones,
            }

            return Response(response_data, status=200)

        except Exception as e:
            # Manejo de errores
            error_message = f"Error al obtener recomendaciones: {str(e)}"
            return Response({"error": error_message}, status=500)


# Leer Recomendaciones de un paciente en específico
class RecomendacionPacienteListView(generics.ListAPIView):
    def get(self, request, paciente_id, *args, **kwargs):
        try:
            # Llama a funcion recomendciones_colaborativas con el paciente_id proporcionado
            recomendaciones = recomendaciones_colaborativas(paciente_id)
            paciente = Paciente.objects.get(id=paciente_id)
            # Crea un diccionario con la lista de recomendaciones
            response_data = {
                "recomendaciones": recomendaciones,
            }

            return Response(response_data, status=200)

        except Paciente.DoesNotExist:
            return Response({"error": "No existe un paciente con ese ID"}, status=404)

        except Exception as e:
            # Manejo de errores
            error_message = f"Error al obtener recomendaciones: {str(e)}"
            return Response({"error": error_message}, status=500)
