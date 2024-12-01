import random
from Paciente import Paciente

class Fila:
    def __init__(self, id, dia=1, reloj=0.0, eventos=None, estado_medico="EL", turnos=[], 
                 tiempo_ocioso_medico=0.0, tiempo_consultorio=0.0, cantidad_atendidos=0, objetos=None):
        """
        Constructor de la clase Fila. Inicializa los atributos con valores por defecto o asigna valores recibidos.
        """
        self.id = id
        self.nombre_evento = ""
        self.dia = dia
        self.reloj = reloj
        self.turnos = turnos
        self.eventos = eventos if eventos is not None else []  # Matriz inicializada vacía
        self.estado_medico = estado_medico

        self.tiempo_ocioso_medico = tiempo_ocioso_medico
        self.tiempo_consultorio = tiempo_consultorio
        self.cantidad_atendidos = cantidad_atendidos
        self.horarios_pacientes = []
        self.objetos = objetos if objetos is not None else []  # Array inicializado vacío


    def calcular_llegada(self, rnd, prob_15_tarde, prob_10_tarde, prob_exacta, prob_5_temprano, prob_15_temprano, prob_no_presenta):
        if 0 <= rnd < prob_15_temprano:
            return -15/60
        elif prob_15_temprano <= rnd < prob_15_temprano + prob_5_temprano:
            return -5/60
        elif prob_15_temprano + prob_5_temprano <= rnd < prob_15_temprano + prob_5_temprano + prob_exacta:
            return 0
        elif  prob_15_temprano + prob_5_temprano + prob_exacta <= rnd <  prob_15_temprano + prob_5_temprano + prob_exacta + prob_10_tarde:
            return 10/60
        elif prob_15_temprano + prob_5_temprano + prob_exacta + prob_10_tarde <= rnd < prob_15_temprano + prob_5_temprano + prob_exacta + prob_10_tarde + prob_15_tarde:
            return 15/60
        else:
            return None


    def calcular_atencion(self, rnd,prob_24_min, prob_27_min, prob_30_min, prob_32_min, prob_35_min, prob_38_min):
        if 0 <= rnd < prob_24_min:
            return 24/60
        elif prob_24_min <= rnd < prob_24_min + prob_27_min:
            return 27/60
        elif prob_24_min + prob_27_min <= rnd < prob_24_min + prob_27_min + prob_30_min:
            return 30/60
        elif prob_24_min + prob_27_min + prob_30_min <= rnd < prob_24_min + prob_27_min + prob_30_min + prob_32_min:
            return 32/60
        elif prob_24_min + prob_27_min + prob_30_min + prob_32_min <= rnd < prob_24_min + prob_27_min + prob_30_min + prob_32_min + prob_35_min:
            return 35/60
        else:
            return 38/60


    def simular(self, datos):
        """
        Simula el comportamiento de la fila basado en los parámetros recibidos.

        :param datos: Array con los parámetros enviados desde VentanaSimulador.py.
        """
        # Desempaquetar los datos del array recibido
        hora_medico, cant_pacientes, duracion_consulta, prob_15_temprano, prob_5_temprano, \
        prob_exacta, prob_10_tarde, prob_15_tarde, prob_no_presenta, prob_24_min, \
        prob_27_min, prob_30_min, prob_32_min, prob_35_min, prob_38_min, respetar_turnos, horarios_pacientes = datos

        if self.reloj == 0:  # Inicialización de la simulación
            self.nombre_evento = "Inicializacion"
            self.eventos = []
            self.estado_medico = "EL"
            self.objetos = []
            self.turnos = []
            self.eventos.append(["llegada_medico", hora_medico])

            for i in range(cant_pacientes):
                rnd_llegada_paciente = random.random()
                llegada_paciente = horarios_pacientes[i]
                llegada = self.calcular_llegada(rnd_llegada_paciente, prob_15_tarde, prob_10_tarde, prob_exacta, prob_5_temprano, prob_15_temprano, prob_no_presenta)
                estado_inicial = "EL" if llegada is not None else "NP"
                paciente = Paciente(f"{self.dia}-{i+1}", estado_inicial, llegada_paciente + (llegada if llegada is not None else 0))
                self.eventos.append(["llegada_paciente",i+1, rnd_llegada_paciente, llegada_paciente, llegada_paciente + llegada])
                self.turnos.append(paciente)
                self.objetos.append(paciente)

            self.turnos.sort(key=lambda x: x.hora)  # Ordenar los turnos por hora
            self.eventos.append(["fin_atencion",None, None, None, None])
            # Actualizar reloj al primer evento válido
            reloj = min((evento[-1] for evento in self.eventos if evento[-1] is not None), default=hora_medico)

            return [self.dia, reloj, self.eventos, self.estado_medico, self.turnos, self.tiempo_ocioso_medico, self.tiempo_consultorio, self.cantidad_atendidos, self.objetos]

        else:  # Simulación en curso
            anterior = self.reloj
            # Actualizar reloj al siguiente evento válido
            self.reloj = min((evento[-1] for evento in self.eventos if evento[-1] is not None), default=None)
            reloj = self.reloj
            if self.reloj is None:
                raise ValueError("El reloj no puede ser None durante la simulación.")

            dia = self.dia
            for evento in self.eventos:
                if evento[0] == "llegada_medico" and evento[-1] == self.reloj:
                    self.nombre_evento = "llegada_medico"
                    self.estado_medico = "L"
                    self.eventos[0][-1] = None

                elif evento[0] == "llegada_paciente" and self.reloj == evento[-1]:
                    self.nombre_evento = "llegada_paciente"
                    for p in self.turnos:
                        if p.id == f"{self.dia}-{evento[1]}":
                            p.setEstado("EA")  # Actualizar el estado del paciente en la cola
                            break
                    for p in self.objetos:
                        if p.id == f"{self.dia}-{evento[1]}":
                            p.setEstado("EA")  # Actualizar el estado del paciente en la lista de objetos
                            break

                    if self.estado_medico == "L":
                        self.estado_medico = "O"
                        for p in self.turnos:
                            if p.id == f"{self.dia}-{evento[1]}":
                                p.setEstado("SA")  # Cambiar el estado del paciente siendo atendido
                                break
                        for p in self.objetos:
                            if p.id == f"{self.dia}-{evento[1]}":
                                p.setEstado("SA")  # Cambiar el estado en la lista de objetos
                                break
                        rnd_fin_atencion = random.random()
                        tiempo_atencion = self.calcular_atencion(rnd_fin_atencion, prob_24_min, prob_27_min, prob_30_min, prob_32_min, prob_35_min, prob_38_min)
                        proximo_fin_atencion = self.reloj + tiempo_atencion
                        self.eventos[-1] = ["fin_atencion", evento[1], rnd_fin_atencion, tiempo_atencion, proximo_fin_atencion]

                elif evento[0] == "fin_atencion" and self.reloj == evento[-1]:
                    self.nombre_evento = "fin_atencion"
                    self.cantidad_atendidos += 1
                    self.tiempo_consultorio += self.reloj - hora_medico  # Acumular tiempo de atención

                    # Procesar el paciente en la cola de turnos
                    if self.turnos:
                        paciente_atendido = self.turnos.pop(0)  # Remover el primer turno
                        paciente_atendido.setEstado("A")  # Cambiar el estado a Atendido

                        # Actualizar el estado en la lista de objetos
                        for p in self.objetos:
                            if p.id == paciente_atendido.id:
                                p.setEstado("A")

                        # Preparar el siguiente evento de atención si hay más turnos
                        if self.turnos:
                            self.estado_medico = "O"
                            siguiente_paciente = self.turnos[0]
                            siguiente_paciente.setEstado("SA")  # Cambiar el estado del siguiente paciente
                            rnd_fin_atencion = random.random()
                            tiempo_atencion = self.calcular_atencion(rnd_fin_atencion, prob_24_min, prob_27_min, prob_30_min, prob_32_min, prob_35_min, prob_38_min)
                            proximo_fin_atencion = self.reloj + tiempo_atencion
                            self.eventos[-1] = ["fin_atencion", siguiente_paciente.id, rnd_fin_atencion, tiempo_atencion, proximo_fin_atencion]
                        else:
                            # Si no hay más turnos, el médico queda libre y avanza al siguiente día
                            self.estado_medico = "L"
                            self.eventos[-1][-1] = None
                            self.dia += 1  # Incrementar el día
                            reloj = 0  # Reiniciar el reloj
                            return self.simular(datos)  # Reiniciar el proceso para el nuevo día

            return [dia, reloj, self.eventos, self.estado_medico, self.turnos, self.tiempo_ocioso_medico, self.tiempo_consultorio, self.cantidad_atendidos, self.objetos]


    def __str__(self):
        return f"Nombre del evento: {self.nombre_evento}, Reloj: {self.reloj}, Dia: {self.dia}, Eventos: {self.eventos}, Estado: {self.estado_medico}, Cola: {self.turnos} TO: {self.tiempo_ocioso_medico}, TC: {self.tiempo_consultorio}, CA: {self.cantidad_atendidos}\n"
    # Objetos: { self.objetos},