from formwindow import Eliminar, Crear, Actualizar, \
    Buscar


class AgregarTicketServicio(Crear):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 700)
        self.title_label.setText("Crear Ticket de Servicio")
        self.table_name = 'ticketservicio'
        self.campos = ["Estado del Ticket", "Código de Cliente", "Código de Empleado", "Código de Servicio",
                       "Código de Facturación"]
        self.columnas = ["cod_ticket", "state_ticket", "cod_customer", "cod_emp", "cod_serv", "cod_fact"]
        self.field_list = []
        self.autoincrement = True
        self.create_fields(self.campos, self.campos_layout)
        self.campos_layout.setContentsMargins(60, 20, 60, 20)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
        self.clear_fields()

    def create_and_exec(self):
        form = AgregarTicketServicio()
        form.exec_()


class BorrarTicketServicio(Eliminar):
    def __init__(self):
        super().__init__()
        self.set_title_text("Eliminar Ticket de Servicio")
        self.table_name = "ticketservicio"
        self.table_widget.setColumnCount(6)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Código", "Estado del Ticket", "Código de Cliente", "Código de Empleado", "Código de Facturación",
                        "Código de Servicio"]
        self.columns = ["cod_ticket", "state_ticket", "cod_customer", "cod_emp", "cod_fact", "cod_serv"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label.setText("Ingrese el código del ticket que desea eliminar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_borrar)
        self.layout.addWidget(self.borrar_button)

    def create_and_exec(self):
        form = BorrarTicketServicio()
        form.exec_()


class ModificarTicketServicio(Actualizar):
    def __init__(self):
        super().__init__()
        self.set_title_text("Actualizar Ticket de Servicio")
        self.table_name = "ticketservicio"
        self.table_widget.setColumnCount(6)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Codigo", "Estado del Ticket", "Código de Cliente", "Código de Empleado", "Código de Facturación",
                        "Código de Servicio"]
        self.columns = ["cod_ticket", "state_ticket", "cod_customer", "cod_emp", "cod_fact", "cod_serv"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label.setText("Ingrese el código de ticket que desea actualizar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_modificar)
        self.layout.addWidget(self.modificar_button)

    def create_and_exec(self):
        form = ModificarTicketServicio()
        form.exec_()


class ConsultarTicketServicio(Buscar):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.set_title_text("Buscar Ticket de Servicio")
        self.table_name = "ticketservicio"
        self.headers = ["Código", "Estado del Ticket", "Código de Cliente", "Código de Técnico Asignado", "Código de Facturación",
                        "Código de Servicio", "Código de Repuesto"]
        self.columns = ["cod_ticket", "state_ticket", "cod_customer", "cod_emp", "cod_fact", "cod_serv"]
        self.columns_table = 6
        self.filter_combo.addItems(["Código", "Estado", "Técnico"])
        self.mapping_columns = {
            "Código": "cod_ticket",
            "Estado": "state_ticket",
            "Técnico": "cod_emp"}
        self.consultar_button.clicked.connect(self.read_row)
        self.layout.addLayout(self.filter_layout)
        self.filter_layout.addWidget(self.filter_label)
        self.filter_layout.addWidget(self.filter_combo)
        self.filter_layout.addWidget(self.search_label)
        self.filter_layout.addWidget(self.search_field)
        self.filter_layout.addWidget(self.consultar_button)

    def create_and_exec(self):
        form = ConsultarTicketServicio()
        form.exec_()
