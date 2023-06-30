from formwindow import Reporte


class ReporteCliente(Reporte):
    def create_and_exec(self):
        form = ReporteCliente()
        form.exec_()


class ReporteVenta(Reporte):
    def create_and_exec(self):
        form = ReporteVenta()
        form.exec_()


class ReporteServicioRepuesto(Reporte):
    def create_and_exec(self):
        form = ReporteServicioRepuesto()
        form.exec_()
