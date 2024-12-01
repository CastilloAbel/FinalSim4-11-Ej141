import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ResultadosVentana:
    def __init__(self, root, tabla):
        self.root = root
        self.root.title("Resultados de la Simulación")

        # Frame principal
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)
        self.tabla = tabla
        # Treeview para mostrar los resultados
        self.tree = ttk.Treeview(self.frame, columns=(
            "id", "nombre_evento", "dia", "reloj", "estado_medico", 
            "cola", "tiempo_ocioso_medico", "tiempo_consultorio", "cantidad_atendidos"),
            show="headings", height=20
        )
        self.tree.pack(fill="both", expand=True)

        # Definir encabezados y tamaños de columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre_evento", text="Evento")
        self.tree.heading("dia", text="Día")
        self.tree.heading("reloj", text="Reloj")
        self.tree.heading("estado_medico", text="Estado Médico")
        self.tree.heading("cola", text="Cola")
        self.tree.heading("tiempo_ocioso_medico", text="Tiempo Ocioso")
        self.tree.heading("tiempo_consultorio", text="Tiempo Consultorio")
        self.tree.heading("cantidad_atendidos", text="Atendidos")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre_evento", width=150, anchor="w")
        self.tree.column("dia", width=50, anchor="center")
        self.tree.column("reloj", width=100, anchor="center")
        self.tree.column("estado_medico", width=100, anchor="center")
        self.tree.column("cola", width=150, anchor="w")
        self.tree.column("tiempo_ocioso_medico", width=100, anchor="center")
        self.tree.column("tiempo_consultorio", width=100, anchor="center")
        self.tree.column("cantidad_atendidos", width=100, anchor="center")

        # Insertar datos en el Treeview
        for fila in tabla:
            self.tree.insert("", "end", values=(
                fila.id, fila.nombre_evento, fila.dia, round(fila.reloj, 2), 
                fila.estado_medico, len(fila.cola), round(fila.tiempo_ocioso_medico, 2), 
                round(fila.tiempo_consultorio, 2), fila.cantidad_atendidos
            ))

        # Asociar evento de clic a una fila
        self.tree.bind("<Double-1>", self.mostrar_detalles)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar_y.set)

    def mostrar_detalles(self, event):
        # Obtener la fila seleccionada
        item_id = self.tree.selection()[0]
        valores = self.tree.item(item_id, "values")

        # Obtener el índice de la fila seleccionada
        fila_id = int(valores[0]) - 1

        # Obtener datos adicionales
        fila = self.tabla[fila_id]  # `tabla` debe ser accesible para esta función
        eventos = fila.eventos
        objetos = fila.objetos

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

        for evento in eventos:
            eventos_text.insert("end", f"{evento}\n")

        # Mostrar lista de objetos
        objetos_label = tk.Label(detalles_frame, text="Lista de Objetos", font=("Arial", 12, "bold"))
        objetos_label.pack(anchor="w")

        objetos_text = tk.Text(detalles_frame, height=10, wrap="none")
        objetos_text.pack(fill="both", expand=True)
        objetos_scroll = ttk.Scrollbar(detalles_frame, orient="vertical", command=objetos_text.yview)
        objetos_text.configure(yscrollcommand=objetos_scroll.set)
        objetos_scroll.pack(side="right", fill="y")

        for objeto in objetos:
            objetos_text.insert("end", f"ID: {objeto.id}, Estado: {objeto.estado}, Hora Llegada: {objeto.hora_llegada}\n")

        # Botón para cerrar la ventana
        close_button = tk.Button(detalles_window, text="Cerrar", command=detalles_window.destroy)
        close_button.pack(pady=10)

# Uso de ResultadosVentana para pruebas
# if __name__ == "__main__":
#     root = tk.Tk()
#     tabla = []  # Simular datos aquí o pasar la tabla generada en la simulación
#     app = ResultadosVentana(root, tabla)
#     root.mainloop()
