from formwindow import Eliminar, Crear, Actualizar, Buscar


class AgregarTicketRepuesto(Crear):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 700)
        self.title_label.setText("Crear Ticket")
        self.table_name = 'ticketrepuesto'
        self.campos = ["Estado del Ticket", "Código de Cliente", "Código de Facturación", "Código de Repuesto"]
        self.columnas = ["cod_ticket", "state_ticket", "cod_customer", "cod_fact", "cod_rep"]
        self.field_list = []
        self.autoincrement = True
        self.create_fields(self.campos, self.campos_layout)
        self.campos_layout.setContentsMargins(60, 20, 60, 20)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
        self.clear_fields()

    def create_and_exec(self):
        form = AgregarTicketRepuesto()
        form.exec_()


class BorrarTicketRepuesto(Eliminar):
    def __init__(self):
        super().__init__()
        self.set_title_text("Eliminar Ticket")
        self.table_name = "ticketrepuesto"
        self.table_widget.setColumnCount(5)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Código", "Estado", "Código de cliente", "Código de facturación", "Código de Repuesto"]
        self.columns = ["cod_ticket", "state_ticket", "cod_customer", "cod_fact", "cod_rep"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label.setText("Ingrese el código del ticket que desea eliminar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_borrar)
        self.layout.addWidget(self.borrar_button)

    def create_and_exec(self):
        form = BorrarTicketRepuesto()
        form.exec_()


class ModificarTicketRespuesto(Actualizar):
    def __init__(self):
        super().__init__()
        self.set_title_text("Actualizar Ticket")
        self.table_name = "ticketrepuesto"
        self.table_widget.setColumnCount(5)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Codigo", "Estado", "Código de cliente", "Código de facturación", "Código de repuesto"]
        self.columns = ["cod_ticket", "state_ticket", "cod_customer", "cod_fact", "cod_rep"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label.setText("Ingrese el código de ticket que desea actualizar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_modificar)
        self.layout.addWidget(self.modificar_button)

    def create_and_exec(self):
        form = ModificarTicketRespuesto()
        form.exec_()


class ConsultarTicketRepuesto(Buscar):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.set_title_text("Buscar Ticket")
        self.table_name = "ticketrepuesto"
        self.headers = ["Código", "Estado", "Código de cliente", "Código de facturación", "Código de repuesto"]
        self.columns = ["cod_ticket", "state_ticket", "cod_customer", "cod_fact", "cod_rep"]
        self.columns_table = 5
        self.filter_combo.addItems(["Código", "Estado", "Cliente"])
        self.mapping_columns = {
            "Código": "cod_ticket",
            "Estado": "state_ticket",
            "Cliente": "cod_customer"}
        self.consultar_button.clicked.connect(self.read_row)
        self.layout.addLayout(self.filter_layout)
        self.filter_layout.addWidget(self.filter_label)
        self.filter_layout.addWidget(self.filter_combo)
        self.filter_layout.addWidget(self.search_label)
        self.filter_layout.addWidget(self.search_field)
        self.filter_layout.addWidget(self.consultar_button)

    def create_and_exec(self):
        form = ConsultarTicketRepuesto()
        form.exec_()
