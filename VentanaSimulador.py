import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ResultadosVentana import ResultadosVentana
from Fila import Fila
from codecarbon import EmissionsTracker
import time
import json
import os
from datetime import datetime


class VentanaSimulador:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Consultas Médicas")
        self.tracker = None
        self.simulation_start_time = None

        # Crear frame principal con padding
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        # Crear labels y entradas con espaciado y alineación
        self.parameters = [
            ("Cantidad de tiempo a simular (días):", "1000"),
            ("Hora de llegada del médico (hs):", "8"),
            ("Cantidad de pacientes:", "16"),
            ("Duración de la consulta (min):", "30"),
            ("Probabilidad de que el paciente llegue 15 min temprano:", "0.1"),
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
            ("ID específico a mostrar (J):", "0")
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
        # Iniciar tracking de emisiones específicamente para la simulación
        self.tracker = EmissionsTracker(
            project_name="simulacion_medica",
            experiment_name=f"simulacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            output_dir="./carbon_tracking",
            log_level="INFO"
        )
        self.tracker.start()
        self.simulation_start_time = time.time()
        
        try:
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

            # Verificar probabilidades (código existente)
            suma_probabilidades = prob_15_temprano + prob_5_temprano + prob_exacta + prob_10_tarde + prob_15_tarde + prob_no_presenta
            suma = prob_24_min + prob_27_min + prob_30_min + prob_32_min + prob_35_min + prob_38_min 
            
            if not abs(suma_probabilidades - 1.0) < 1e-6:
                messagebox.showwarning(
                    "Advertencia",
                    f"La suma de las probabilidades debe ser igual a 1. Actualmente es {suma_probabilidades:.3f}."
                )
                self.tracker.stop()
                return
            elif not abs(suma - 1.0) < 1e-6:
                messagebox.showwarning(
                    "Advertencia",
                    f"La suma de las probabilidades debe ser igual a 1. Actualmente es {suma:.3f}."
                )
                self.tracker.stop()
                return

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
            
            # Ejecutar simulación (código existente)
            tabla = []
            eventos = dict()
            turnos = dict()
            estados = dict()
            proximos = dict()
            
            for i in range(100000000):
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
                    if fila.dia >= dias_simular+1:
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
            
            # Finalizar tracking y mostrar resultados
            simulation_time = time.time() - self.simulation_start_time
            emissions = self.tracker.stop()
            
            # Mostrar estadísticas de emisiones
            self.mostrar_estadisticas_carbon(emissions, simulation_time)
            
        except Exception as e:
            if self.tracker:
                self.tracker.stop()
            messagebox.showerror("Error", f"Error durante la simulación: {str(e)}")

    def mostrar_estadisticas_carbon(self, emissions, simulation_time):
        """Muestra estadísticas detalladas de emisiones de carbono"""
        
        # Calcular compensación por árboles
        arbol_joven_kg_ano = 30  # kg CO2 por año
        arbol_adulto_kg_ano = 300  # kg CO2 por año
        
        # Convertir a emisiones por hora
        emissions_per_hour = emissions / (simulation_time / 3600) if simulation_time > 0 else 0
        
        # Calcular horas de procesamiento que compensaría cada tipo de árbol
        horas_arbol_joven = arbol_joven_kg_ano / (emissions_per_hour * 24 * 365) if emissions_per_hour > 0 else float('inf')
        horas_arbol_adulto = arbol_adulto_kg_ano / (emissions_per_hour * 24 * 365) if emissions_per_hour > 0 else float('inf')
        
        # Crear ventana de estadísticas
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Estadísticas de Huella de Carbono")
        stats_window.geometry("600x400")
        
        stats_frame = tk.Frame(stats_window, padx=20, pady=20)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(stats_frame, text="Análisis de Huella de Carbono", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Estadísticas básicas
        stats_text = f"""
EMISIONES DE LA SIMULACIÓN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Emisiones totales: {emissions:.6f} kg CO2eq
• Tiempo de simulación: {simulation_time:.2f} segundos
• Emisiones por hora: {emissions_per_hour:.6f} kg CO2eq/hora

COMPENSACIÓN POR ÁRBOLES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌱 ÁRBOL JOVEN (30 kg CO2/año):
   Puede compensar: {horas_arbol_joven:.0f} horas de procesamiento por año

🌳 ÁRBOL ADULTO (300 kg CO2/año):
   Puede compensar: {horas_arbol_adulto:.0f} horas de procesamiento por año

ANÁLISIS DE IMPACTO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Para compensar esta simulación se necesitarían:
  - {emissions/30:.6f} árboles jóvenes trabajando un año completo
  - {emissions/300:.6f} árboles adultos trabajando un año completo

• Esta simulación equivale a:
  - {emissions*1000:.3f} gramos de CO2eq
  - {emissions/0.000411:.1f} km en auto promedio (411g CO2/km)
        """
        
        text_widget = tk.Text(stats_frame, wrap=tk.WORD, font=("Courier", 10))
        text_widget.insert(tk.END, stats_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Botón para guardar reporte
        save_button = tk.Button(stats_frame, text="Guardar Reporte", 
                               command=lambda: self.guardar_reporte_carbon(emissions, simulation_time))
        save_button.pack(pady=(10, 0))
        
        print(f"\n{'='*50}")
        print("ESTADÍSTICAS DE HUELLA DE CARBONO")
        print(f"{'='*50}")
        print(f"Emisiones totales: {emissions:.6f} kg CO2eq")
        print(f"Tiempo de simulación: {simulation_time:.2f} segundos")
        print(f"Emisiones por hora: {emissions_per_hour:.6f} kg CO2eq/hora")
        print(f"Compensación árbol joven: {horas_arbol_joven:.0f} horas/año")
        print(f"Compensación árbol adulto: {horas_arbol_adulto:.0f} horas/año")
        print(f"{'='*50}\n")

    def guardar_reporte_carbon(self, emissions, simulation_time):
        """Guarda un reporte detallado de las emisiones"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_carbon_{timestamp}.json"
        
        emissions_per_hour = emissions / (simulation_time / 3600) if simulation_time > 0 else 0
        arbol_joven_horas = 30 / (emissions_per_hour * 24 * 365) if emissions_per_hour > 0 else float('inf')
        arbol_adulto_horas = 300 / (emissions_per_hour * 24 * 365) if emissions_per_hour > 0 else float('inf')
        
        reporte = {
            "timestamp": datetime.now().isoformat(),
            "simulacion": {
                "emisiones_kg_co2eq": emissions,
                "tiempo_simulacion_segundos": simulation_time,
                "emisiones_por_hora": emissions_per_hour
            },
            "compensacion_arboles": {
                "arbol_joven_30kg_ano": {
                    "horas_compensadas_por_ano": arbol_joven_horas,
                    "arboles_necesarios_ano_completo": emissions / 30
                },
                "arbol_adulto_300kg_ano": {
                    "horas_compensadas_por_ano": arbol_adulto_horas,
                    "arboles_necesarios_ano_completo": emissions / 300
                }
            },
            "equivalencias": {
                "gramos_co2": emissions * 1000,
                "kilometros_auto_promedio": emissions / 0.000411
            }
        }
        
        try:
            os.makedirs("./carbon_reports", exist_ok=True)
            filepath = os.path.join("./carbon_reports", filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(reporte, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Reporte Guardado", f"Reporte guardado en: {filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar reporte: {str(e)}")

# Crear instancia de la ventana
if __name__ == "__main__":
    # Tracker global para toda la aplicación
    tracker_global = EmissionsTracker(
        project_name="app_simulacion_completa",
        experiment_name=f"sesion_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        output_dir="./carbon_tracking"
    )
    tracker_global.start()
    
    try:
        root = tk.Tk()
        app = VentanaSimulador(root)
        root.mainloop()
        
    finally:
        emision_total = tracker_global.stop()
        print(f"\n{'='*60}")
        print("RESUMEN FINAL DE EMISIONES")
        print(f"{'='*60}")
        print(f"Emisiones totales de la aplicación: {emision_total:.6f} kg CO2eq")
        print(f"{'='*60}\n")