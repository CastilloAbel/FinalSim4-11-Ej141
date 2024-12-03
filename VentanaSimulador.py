import tkinter as tk
from tkinter import ttk
from ResultadosVentana import ResultadosVentana
from Fila import Fila

class VentanaSimulador:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Consultas Médicas")

        # Crear frame principal con padding
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        # Crear labels y entradas con espaciado y alineación
        self.parameters = [
            ("Cantidad de tiempo a simular (días):", "1000"),
            ("Hora de llegada del médico (hs):", "8"),
            ("Cantidad de pacientes:", "16"),
            ("Duración de la consulta (min):", "30"),
            ("Probabilidad de que el paciente llegue 15 min temprano:", "0.15"),
            ("Probabilidad de que el paciente llegue 5 min temprano:", "0.3"),
            ("Probabilidad de que el paciente llegue a la hora exacta:", "0.4"),
            ("Probabilidad de que el paciente llegue 10 min tarde:", "0.1"),
            ("Probabilidad de que el paciente llegue 15 min tarde:", "0.05"),
            ("Probabilidad de que el paciente no se presente:", "0.05"),
            ("Probabilidad de que el médico tarde 24 min en atender:", "0.2"),
            ("Probabilidad de que el médico tarde 27 min en atender:", "0.25"),
            ("Probabilidad de que el médico tarde 30 min en atender:", "0.2"),
            ("Probabilidad de que el médico tarde 32 min en atender:", "0.15"),
            ("Probabilidad de que el médico tarde 35 min en atender:", "0.15"),
            ("Probabilidad de que el médico tarde 38 min en atender:", "0.05"),
            ("Cantidad de filas a mostrar (I):", "100"),
            ("ID específico a mostrar (J):", "1")
        ]

        self.entries = []

        for i, (label_text, default_value) in enumerate(self.parameters):
            label = tk.Label(self.frame, text=label_text, anchor="w", width=50)
            label.grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(self.frame, width=15)
            entry.insert(0, default_value)
            entry.grid(row=i, column=1, sticky="e", pady=5)
            self.entries.append(entry)

        # Asignar las entradas a variables para un acceso más legible
        (self.entry_dias_simular, self.entry_hora_medico, self.entry_cant_pacientes, self.entry_duracion_consulta,
         self.entry_prob_15_temprano, self.entry_prob_5_temprano, self.entry_prob_exacta,
         self.entry_prob_10_tarde, self.entry_prob_15_tarde, self.entry_prob_no_presenta,
         self.entry_prob_24_min, self.entry_prob_27_min, self.entry_prob_30_min,
         self.entry_prob_32_min, self.entry_prob_35_min, self.entry_prob_38_min,
         self.entry_filas_mostrar, self.entry_dia_especifico) = self.entries

        # Combobox para la alternativa
        label_respetar_turnos = tk.Label(self.frame, text="Orden de turnos:", anchor="w", width=50)
        label_respetar_turnos.grid(row=len(self.parameters), column=0, sticky="w", pady=5)
        self.combobox_respetar_turnos = ttk.Combobox(self.frame, 
                                                     values=["Respetar el orden de los turnos", "No respetar el orden de los turnos"], 
                                                     width=27)
        self.combobox_respetar_turnos.set("Respetar el orden de los turnos")
        self.combobox_respetar_turnos.grid(row=len(self.parameters), column=1, sticky="e", pady=5)

        # Botón Simular
        boton_simular = tk.Button(self.frame, text="Simular", command=self.simular, width=20)
        boton_simular.grid(row=len(self.parameters) + 1, column=0, columnspan=2, pady=15)

    def simular(self):
        # Recolectar valores de entrada
        dias_simular = int(self.entry_dias_simular.get())
        hora_medico = int(self.entry_hora_medico.get())
        cant_pacientes = int(self.entry_cant_pacientes.get())
        duracion_consulta = int(self.entry_duracion_consulta.get())
        prob_15_temprano = float(self.entry_prob_15_temprano.get())
        prob_5_temprano = float(self.entry_prob_5_temprano.get())
        prob_exacta = float(self.entry_prob_exacta.get())
        prob_10_tarde = float(self.entry_prob_10_tarde.get())
        prob_15_tarde = float(self.entry_prob_15_tarde.get())
        prob_no_presenta = float(self.entry_prob_no_presenta.get())
        prob_24_min = float(self.entry_prob_24_min.get())
        prob_27_min = float(self.entry_prob_27_min.get())
        prob_30_min = float(self.entry_prob_30_min.get())
        prob_32_min = float(self.entry_prob_32_min.get())
        prob_35_min = float(self.entry_prob_35_min.get())
        prob_38_min = float(self.entry_prob_38_min.get())
        filas_mostrar = int(self.entry_filas_mostrar.get())
        dia_especifico = int(self.entry_dia_especifico.get())
        respetar_turnos = self.combobox_respetar_turnos.get() == "Respetar el orden de los turnos"
        horarios_pacientes = []
        horario = hora_medico + 15/60
        for i in range(cant_pacientes):
            horarios_pacientes.append(horario)
            horario = horario + duracion_consulta/60

        datos = [hora_medico, cant_pacientes, duracion_consulta, prob_15_temprano, prob_5_temprano, \
        prob_exacta, prob_10_tarde, prob_15_tarde, prob_no_presenta, prob_24_min, \
        prob_27_min, prob_30_min, prob_32_min, prob_35_min, prob_38_min, respetar_turnos, horarios_pacientes]
        # Mostrar valores recogidos


        print("Simulación iniciada...")
        tabla = []
        eventos = dict()
        turnos = dict()
        estados = dict()
        proximos = dict()
        for i in range(100000):
            if i == 0:
                prox = []
                estado = []
                fila = Fila(i+1)
                lista = fila.simular(datos)
                tabla.append(fila)
                eventos[fila.id] = [*fila.eventos]
                turnos[fila.id] = [*fila.turnos]
                for est in fila.turnos:
                    estado.append(est["estado"])
                estados[fila.id] = [*estado]
                for p in fila.eventos:
                    prox.append(p[-1])
                proximos[fila.id] = [*prox]
                # tabla.append(fila)
                # print(fila)
            else:
                if fila.dia >= dias_simular:
                    tabla.pop()
                    break
                else:
                    estado = []
                    prox = []
                    fila = Fila(i+1, lista[0], lista[1], lista[2], lista[3], lista[4], lista[5], lista[6], lista[7], lista[8], lista[9], lista[10], lista[11])
                    lista = fila.simular(datos)
                    tabla.append(fila)
                    eventos[fila.id] = [*fila.eventos]
                    turnos[fila.id] = [*fila.turnos]
                    for est in fila.turnos:
                        estado.append(est["estado"])
                    estados[fila.id] = [*estado]
                    for p in fila.eventos:
                        prox.append(p[-1])
                    proximos[fila.id] = [*prox]
                # tabla.append(fila)
        # print(turnos[7])
        # print(turnos[8])
        # print(turnos[9])
        # for fila in tabla:
        #     print(fila)
        root = tk.Tk()
        resultados = ResultadosVentana(root, tabla, eventos, turnos, estados, proximos)
        # root.mainloop()
        resultados.mostrar_resultados(tabla, filas_mostrar, dia_especifico, eventos, turnos)
# Crear instancia de la ventana
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaSimulador(root)
    root.mainloop()
