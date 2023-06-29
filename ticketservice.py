from PySide6.QtWidgets import QLabel, QPushButton

from formwindow import BorrarFormularioWindow, AgregarFormularioWindow, ModificarFormularioWindow, \
    ConsultarFormularioWindow


class AgregarTicket(AgregarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 700)
        self.title_label.setText("Crear Ticket")
        self.table_name = 'ticket'
        self.campos = ["Estado del Ticket", "Código de Cliente", "Código de Empleado", "Código de Facturación",
                       "Código de Servicio", "Código de Repuesto"]
        self.columnas = ["cod_ticket", "state_ticket", "cod_customer", "cod_emp", "cod_fact", "cod_serv", "cod_rep"]
        self.field_list = []
        self.autoincrement = True
        self.create_fields(self.campos, self.campos_layout)
        self.campos_layout.setContentsMargins(60, 20, 60, 20)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
        self.clear_fields

    def create_and_exec(self):
        form = AgregarTicket()
        form.exec_()


class BorrarTicket(BorrarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.set_title_text("Eliminar Ticket")
        self.table_name = "ticket"
        self.table_widget.setColumnCount(7)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Código", "Estado", "Código de cliente", "Código de empleado", "Código de facturación",
                        "Código de Servicio", "Código de Repuesto"]
        self.columns = ["cod_ticket", "state_ticket", "cod_customer", "cod_emp", "cod_fact", "cod_serv", "cod_rep"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label = QLabel("Ingrese el código del ticket que desea eliminar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_borrar)
        self.layout.addWidget(self.borrar_button)

    def create_and_exec(self):
        form = BorrarTicket()
        form.exec_()


class ModificarTicket(ModificarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.set_title_text("Actualizar Ticket")
        self.table_name = "ticket"
        self.table_widget.setColumnCount(5)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Codigo", "Estado", "Código de cliente", "Código de empleado", "Código de facturación",
                        "Código de servicio", "Código de repuesto"]
        self.columns = ["cod_ticket", "state_ticket", "cod_customer", "cod_emp", "cod_fact", "cod_serv", "cod_rep"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label = QLabel("Ingrese el código de ticket que desea actualizar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_modificar)
        self.layout.addWidget(self.modificar_button)

    def create_and_exec(self):
        form = ModificarTicket()
        form.exec_()


class ConsultarTicket(ConsultarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.set_title_text("Buscar Ticket")
        self.table_name = "ticket"
        self.headers = ["Código", "Estado", "Código de cliente", "Código de Técnico asignado", "Código de facturación",
                        "Código de servicio", "Código de repuesto"]
        self.columns = ["cod_ticket", "state_ticket", "cod_customer", "cod_emp", "cod_fact", "cod_serv", "cod_rep"]
        self.columns_table = 5
        self.filter_combo.addItems(["Código", "Estado", "Técnico"])
        self.mapping_columns = {
            "Código": "cod_ticket",
            "Estado": "state_ticket",
            "Técnico": "cod_emp"}
        self.consultar_button = QPushButton("Consultar")
        self.consultar_button.clicked.connect(self.read_row)
        self.layout.addLayout(self.filter_layout)
        self.filter_layout.addWidget(self.filter_label)
        self.filter_layout.addWidget(self.filter_combo)
        self.filter_layout.addWidget(self.search_label)
        self.filter_layout.addWidget(self.search_field)
        self.filter_layout.addWidget(self.consultar_button)

    def create_and_exec(self):
        form = ConsultarTicket()
        form.exec_()