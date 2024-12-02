class Paciente:
    def __init__(self, id, estado, hora):
        self.id = id
        self.estado = estado
        self.hora_llegada = hora

    def __str__(self):
        return f"ID: {self.id}, Estado: {self.estado}, Hora: {self.hora_llegada}"