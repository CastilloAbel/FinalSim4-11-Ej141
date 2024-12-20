import random
from Paciente import Paciente

class Fila:
    def __init__(self, id, dia=1, reloj=0.0, eventos=None, estado_medico="Esperando Llegada", turnos=[], paciente=None, 
                 tiempo_ocioso_medico=0.0, tiempo_consultorio=0.0, cantidad_atendidos=0, acum_ocioso=0.0, acum_consultorio=0.0, acum_atendidos=0):
        """
        Constructor de la clase Fila. Inicializa los atributos con valores por defecto o asigna valores recibidos.
        """
        self.id = id
        self.nombre_evento = ""
        self.dia = dia
        self.reloj = reloj
        self.turnos = turnos
        self.eventos = eventos if eventos is not None else []  # Matriz inicializada vacía
        self.paciente_actual = paciente
        self.estado_medico = estado_medico
        # self.cola = cola if cola is not None else []  # Array inicializado vacío
        self.tiempo_ocioso_medico = tiempo_ocioso_medico
        self.tiempo_consultorio = tiempo_consultorio
        self.cantidad_atendidos = cantidad_atendidos
        self.horarios_pacientes = []
        self.acum_ocioso = acum_ocioso
        self.acum_consultorio = acum_consultorio
        self.acum_atendidos = acum_atendidos
        # self.objetos = objetos if objetos is not None else []  # Array inicializado vacío


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
        # Desempaquetar los datos del array recibido (siguiendo el orden del simulador)
        hora_medico, cant_pacientes, duracion_consulta, prob_15_temprano, prob_5_temprano, \
        prob_exacta, prob_10_tarde, prob_15_tarde, prob_no_presenta, prob_24_min, \
        prob_27_min, prob_30_min, prob_32_min, prob_35_min, prob_38_min, respetar_turnos, horarios_pacientes = datos



        if self.reloj ==0:
            self.nombre_evento = "Inicializacion"
            self.eventos = []
            self.estado_medico = "Esperando Llegada"
            self.turnos = []
            self.eventos.append(["llegada_medico", hora_medico])
            for i in range(cant_pacientes):
                rnd_llegada_paciente = random.random()
                llegada_paciente = horarios_pacientes[i]
                llegada = self.calcular_llegada(rnd_llegada_paciente, prob_15_tarde, prob_10_tarde, prob_exacta, prob_5_temprano, prob_15_temprano, prob_no_presenta)
                if llegada is not None:
                    paciente = Paciente(f"{self.dia}-{i+1}", "Esperando Llegada", llegada_paciente + llegada)
                    turno = {
                        "paciente": paciente,
                        "hora": llegada_paciente + llegada,
                        "estado": "Esperando Llegada"
                    }

                    self.eventos.append(["llegada_paciente",i+1, rnd_llegada_paciente, llegada_paciente, llegada_paciente + llegada])
                else:
                    paciente = Paciente(f"{self.dia}-{i+1}", "Ausente", None)
                    turno = {
                        "paciente": paciente,
                        "hora": None,
                        "estado": "Ausente"
                    }

                    self.eventos.append(["llegada_paciente", i+1, rnd_llegada_paciente, llegada_paciente, llegada])
                self.turnos.append(turno)
                if respetar_turnos:
                    pass
                else:
                    self.turnos = sorted(
                        self.turnos, 
                        key=lambda turno: turno["hora"] if turno["estado"] == "Esperando Llegada" and turno["hora"] is not None else float('inf')
                    )
                
            self.eventos.append(["fin_atencion", None, None, None])
            reloj = min((evento[-1] for evento in self.eventos if evento[-1] is not None), default=None)
            return [self.dia, reloj, self.eventos, self.estado_medico, self.turnos, self.paciente_actual, self.tiempo_ocioso_medico, self.tiempo_consultorio, self.cantidad_atendidos, self.acum_ocioso, self.acum_consultorio, self.acum_atendidos]
        else:
            anterior = self.reloj
            self.reloj = min((evento[-1] for evento in self.eventos if evento[-1] is not None), default=None)
            reloj = self.reloj
            eventos = self.eventos
            dia = self.dia
            for evento in eventos:
                if evento[0] == "llegada_medico" and evento[-1] == self.reloj:
                    self.nombre_evento = "llegada_medico"

                    self.estado_medico = "Libre"
                    self.eventos[0][-1] = None
                    # for i in self.turnos:
                    #     print(i)
                if evento[0] == "llegada_paciente" and self.reloj == evento[-1]:
                    self.nombre_evento = "llegada_paciente"
                    # print(self.reloj)
                    # print(self.turnos)
                    self.tiempo_consultorio = self.reloj - float(hora_medico)
                    self.acum_consultorio += self.tiempo_consultorio
                    for turno in self.turnos:
                        if turno["estado"] == "Esperando Llegada":
                            if self.estado_medico == "Libre":
                                turno["estado"] = "Siendo Atendido"
                                self.paciente_actual = turno["paciente"]
                                self.estado_medico = "Ocupado"
                                self.tiempo_ocioso_medico = self.tiempo_ocioso_medico + (self.reloj - anterior)
                                self.acum_ocioso = self.acum_ocioso + (self.reloj - anterior)
                                #Calcular fin de atencion de esa llegada
                                rnd_fin_atencion = random.random()
                                tiempo_atencion = self.calcular_atencion(rnd_fin_atencion, prob_24_min, prob_27_min, prob_30_min, prob_32_min, prob_35_min, prob_38_min)
                                proximo_fin_atencion = self.reloj + tiempo_atencion
                                self.eventos[evento[1]][-1] = None
                                self.eventos[-1] = ["fin_atencion", turno["paciente"].id ,rnd_fin_atencion, tiempo_atencion, proximo_fin_atencion]
                                break
                            else:
                                turno["estado"] = "Esperando Atencion"
                                self.eventos[evento[1]][-1] = None
                                break
                    break
                elif evento[0] == "fin_atencion" and self.reloj == evento[-1]:
                    self.nombre_evento = "fin_atencion"
                    self.cantidad_atendidos += 1
                    self.acum_atendidos += 1
                    self.tiempo_consultorio = self.reloj - hora_medico
                    self.acum_consultorio += self.tiempo_consultorio
                    # objetos = self.objetos
                    if self.paciente_actual:
                        for turno in self.turnos:
                            if turno["paciente"] == self.paciente_actual:
                                turno["estado"] = "Atendido"
                                self.eventos[-1] = ["fin_atencion", None, None, None, None]
                                break
                    self.paciente_actual = None
                    self.estado_medico = "Libre"
                    for turno in self.turnos:
                        if turno["estado"] == "Esperando Atencion":
                            turno["estado"] = "Siendo Atendido"
                            self.paciente_actual = turno["paciente"]
                            self.estado_medico = "Ocupado"
                            self.tiempo_ocioso_medico = self.tiempo_ocioso_medico + (self.reloj - anterior)
                            self.acum_ocioso = self.acum_ocioso + (self.reloj - anterior)
                            #Calcular fin de atencion de esa llegada
                            rnd_fin_atencion = random.random()
                            tiempo_atencion = self.calcular_atencion(rnd_fin_atencion, prob_24_min, prob_27_min, prob_30_min, prob_32_min, prob_35_min, prob_38_min)
                            proximo_fin_atencion = self.reloj + tiempo_atencion
                            codigo = evento[1]
                            str = codigo.split("-")
                            id = int(str[1])
                            self.eventos[id][-1] = None
                            self.eventos[-1] = ["fin_atencion", turno["paciente"].id, rnd_fin_atencion, tiempo_atencion, proximo_fin_atencion]
                            break
                        else:
                            self.eventos[-1] = ["fin_atencion", None, None, None, None]

                    for turno in self.turnos:
                        if turno["estado"] == "Esperando LLegada" or turno["estado"] == "Esperando Atencion" or turno["estado"] == "Siendo Atendido":
                            break
                        elif turno == self.turnos[-1] and (turno["estado"] == "Atendido" or turno["estado"] == "Ausente"):
                            dia = self.dia + 1
                            reloj = 0
                            self.tiempo_consultorio = 0.0
                            self.tiempo_ocioso_medico = 0.0
                            self.cantidad_atendidos = 0
                            self.eventos[-1] = ["fin_atencion", None, None, None, None]

                    #     self.eventos[-1] = ["fin_atencion", None, None, None]
            # reloj = min((evento[-1] for evento in self.eventos if evento[-1] is not None))
            return [dia, reloj, self.eventos, self.estado_medico, self.turnos ,self.paciente_actual, self.tiempo_ocioso_medico, self.tiempo_consultorio, self.cantidad_atendidos, self.acum_ocioso, self.acum_consultorio, self.acum_atendidos]


    def __str__(self):
        return f"Nombre del evento: {self.nombre_evento}, Reloj: {self.reloj}, Dia: {self.dia}, Eventos: {self.eventos}, Estado: {self.estado_medico}, Turnos: {self.turnos} TO: {self.tiempo_ocioso_medico}, TC: {self.tiempo_consultorio}, CA: {self.cantidad_atendidos}\n"
    # Objetos: { self.objetos},