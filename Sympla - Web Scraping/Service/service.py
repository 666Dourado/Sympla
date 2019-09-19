from Controller.controller import controller

class service:

    def __init__(self):
        self.error = None

    def monitor(self):
        while True:
             #instanciando as classes
            con = controller()
            con.recuperaURL()
