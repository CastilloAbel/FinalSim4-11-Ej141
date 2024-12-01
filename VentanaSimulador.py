import tkinter as tk
from tkinter import ttk

class VentanaSimulador:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Consultas Médicas")

        # Crear frame principal con padding
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        # Crear labels y entradas con espaciado y alineación
        self.parameters = [
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
        (self.entry_hora_medico, self.entry_cant_pacientes, self.entry_duracion_consulta,
         self.entry_prob_15_temprano, self.entry_prob_5_temprano, self.entry_prob_exacta,
         self.entry_prob_10_tarde, self.entry_prob_15_tarde, self.entry_prob_no_presenta,
         self.entry_prob_24_min, self.entry_prob_27_min, self.entry_prob_30_min,
         self.entry_prob_32_min, self.entry_prob_35_min, self.entry_prob_38_min) = self.entries

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
        respetar_turnos = self.combobox_respetar_turnos.get() == "Respetar el orden de los turnos"

        # Mostrar valores recogidos
        print(f"Simulación con parámetros: hora_medico={hora_medico}, cant_pacientes={cant_pacientes}, "
              f"duracion_consulta={duracion_consulta}, respetar_turnos={respetar_turnos}")
        print("Simulación iniciada...")

# Crear instancia de la ventana
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaSimulador(root)
    root.mainloop()
