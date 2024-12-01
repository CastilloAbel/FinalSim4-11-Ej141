class Paciente:
    def __init__(self, id, estado, hora):
        self.id = id
        self.estado = estado
        self.hora = hora

    def setEstado(self, estado):
        self.estado = estado