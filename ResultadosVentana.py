import tkinter as tk
from tkinter import ttk


class ResultadosVentana:
    def __init__(self, root, tabla, eventos, turnos, estados, proximos):
        self.root = root
        self.root.title("Resultados de la Simulación")

        # Frame principal
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)
        self.tabla = tabla
        self.eventos = eventos
        self.turnos = turnos
        self.estados = estados
        self.proximos = proximos
        # Treeview para mostrar los resultados
        self.tree = ttk.Treeview(
            self.frame,
            columns=(
                "id",
                "nombre_evento",
                "dia",
                "reloj",
                "estado_medico",
                "paciente",
                "tiempo_ocioso_medico",
                "tiempo_consultorio",
                "cantidad_atendidos",
            ),
            show="headings",
            height=20,
        )
        self.tree.pack(fill="both", expand=True)

        # Definir encabezados y tamaños de columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre_evento", text="Evento")
        self.tree.heading("dia", text="Día")
        self.tree.heading("reloj", text="Reloj")
        self.tree.heading("estado_medico", text="Estado Médico")
        self.tree.heading("paciente", text="Paciente")
        self.tree.heading("tiempo_ocioso_medico", text="Tiempo Ocioso")
        self.tree.heading("tiempo_consultorio", text="Tiempo Consultorio")
        self.tree.heading("cantidad_atendidos", text="Atendidos")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre_evento", width=150, anchor="w")
        self.tree.column("dia", width=50, anchor="center")
        self.tree.column("reloj", width=100, anchor="center")
        self.tree.column("estado_medico", width=100, anchor="center")
        self.tree.column("paciente", width=150, anchor="w")
        self.tree.column("tiempo_ocioso_medico", width=100, anchor="center")
        self.tree.column("tiempo_consultorio", width=100, anchor="center")
        self.tree.column("cantidad_atendidos", width=100, anchor="center")

    def mostrar_resultados(self, tabla, filas_a_mostrar, fila_inicio, eventos, turnos):
        # Insertar datos en el Treeview con límites de filas a mostrar
        fila_final = fila_inicio + filas_a_mostrar
        for fila_id in range(fila_inicio, min(fila_final, len(tabla))):
            fila = tabla[fila_id]
            self.tree.insert(
                "",
                "end",
                values=(
                    fila.id,
                    fila.nombre_evento,
                    fila.dia,
                    round(fila.reloj, 2),
                    fila.estado_medico,
                    # len(fila.turnos),
                    fila.paciente_actual,
                    round(fila.tiempo_ocioso_medico, 2),
                    round(fila.tiempo_consultorio, 2),
                    fila.cantidad_atendidos,
                ),
            )

        # Asociar evento de clic a una fila
        self.tree.bind("<Double-1>", self.mostrar_detalles)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar_y.set)

    def mostrar_detalles(self, event):
        # Obtener la fila seleccionada
        fila_id = None
        eventos = []
        objetos = []


        item_id = self.tree.selection()[0]
        valores = self.tree.item(item_id, "values")

        # Obtener el índice de la fila seleccionada
        fila_id = int(valores[0])

        # Obtener datos adicionales
        fila = self.tabla[fila_id]  # `tabla` debe ser accesible para esta función
        # eventos = fila.eventos
        eventos = self.eventos[fila.id]
        objetos = self.turnos[fila.id]
        estados = self.estados[fila.id]
        proximos = self.proximos[fila.id]
        # print(fila)
        print(self.eventos[1])
        # Crear ventana emergente para mostrar detalles
        detalles_window = tk.Toplevel(self.root)
        detalles_window.title(f"Detalles de la Fila {fila.id}")
        detalles_window.geometry("600x400")

        # Frame para los datos
        detalles_frame = tk.Frame(detalles_window, padx=10, pady=10)
        detalles_frame.pack(fill="both", expand=True)

        # Mostrar matriz de eventos
        eventos_label = tk.Label(detalles_frame, text="Matriz de Eventos", font=("Arial", 12, "bold"))
        eventos_label.pack(anchor="w")

        eventos_text = tk.Text(detalles_frame, height=10, wrap="none")
        eventos_text.pack(fill="both", expand=True)
        eventos_scroll = ttk.Scrollbar(detalles_frame, orient="vertical", command=eventos_text.yview)
        eventos_text.configure(yscrollcommand=eventos_scroll.set)
        eventos_scroll.pack(side="right", fill="y")
        i = 0
        for evento in eventos:
            if i == 0:
                eventos_text.insert("end", f"Nombre: {evento[0]}, Hora llegada:{proximos[i]}\n")
            else:
                eventos_text.insert("end", f"Nombre: {evento[0]}, ID:{evento[1]}, RND:{evento[2]}, Tiempo:{evento[3]}, Proxima:{proximos[i]}\n")
            i += 1

        # Mostrar lista de objetos
        objetos_label = tk.Label(detalles_frame, text="Lista de Objetos", font=("Arial", 12, "bold"))
        objetos_label.pack(anchor="w")

        objetos_text = tk.Text(detalles_frame, height=10, wrap="none")
        objetos_text.pack(fill="both", expand=True)
        objetos_scroll = ttk.Scrollbar(detalles_frame, orient="vertical", command=objetos_text.yview)
        objetos_text.configure(yscrollcommand=objetos_scroll.set)
        objetos_scroll.pack(side="right", fill="y")
        i = 0
        for objeto in objetos:
            objetos_text.insert("end", f"ID: {objeto['paciente'].id}, Estado: {estados[i]}, Hora Llegada: {objeto['hora']}\n")
            i += 1

        # Botón para cerrar la ventana
        close_button = tk.Button(detalles_window, text="Cerrar", command=detalles_window.destroy)
        close_button.pack(pady=10)
