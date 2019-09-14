from Controller.controller import controller

class service:

    def __init__(self):
        self.error = None

    def monitor(self):
        #instanciando as classes

        con = controller()

        con.recuperaURL()
        #con.recuperaEventos()