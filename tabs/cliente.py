from formwindow import Buscar, Actualizar, Eliminar, \
    Crear


class AgregarCliente(Crear):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 700)
        self.title_label.setText("Crear Cliente")
        self.table_name = 'cliente'
        self.campos = ["Nombre", "Apellido", "Rut", "Dirección", "Email", "Teléfono"]
        self.columnas = ["cod_customer", "name_customer", "lastname_customer", "rut_customer", "address_customer",
                         "email_customer", "phone_customer"]
        self.field_list = []
        self.autoincrement = True
        self.create_fields(self.campos, self.campos_layout)
        self.campos_layout.setContentsMargins(60, 30, 60, 30)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
        self.clear_fields

    def create_and_exec(self):
        form = AgregarCliente()
        form.exec_()


class BorrarCliente(Eliminar):
    def __init__(self):
        super().__init__()
        self.set_title_text("Eliminar Cliente")
        self.table_name = "cliente"
        self.table_widget.setColumnCount(7)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Código", "Nombre", "Apellido", "Rut", "Dirección", "Email", "Teléfono"]
        self.columns = ["cod_customer", "name_customer", "lastname_customer", "rut_customer", "address_customer",
                        "email_customer", "phone_customer"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label.setText("Ingrese el código del cliente que desea eliminar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_borrar)
        self.layout.addWidget(self.borrar_button)

    def create_and_exec(self):
        form = BorrarCliente()
        form.exec_()


class ModificarCliente(Actualizar):
    def __init__(self):
        super().__init__()
        self.set_title_text("Actualizar Cliente")
        self.table_name = "cliente"
        self.table_widget.setColumnCount(7)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Codigo", "Nombre", "Apellido", "Rut", "Dirección", "Email", "Teléfono"]
        self.columns = ["cod_customer", "name_customer", "lastname_customer", "rut_customer", "address_customer",
                        "email_customer", "phone_customer"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label.setText("Ingrese el código de cliente que desea actualizar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_modificar)
        self.layout.addWidget(self.modificar_button)

    def create_and_exec(self):
        form = ModificarCliente()
        form.exec_()


class ConsultarCliente(Buscar):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.set_title_text("Buscar Cliente")
        self.table_name = "cliente"
        self.headers = ["Código", "Nombre", "Apellido", "Rut", "Dirección", "Email", "Teléfono"]
        self.columns = ["cod_customer", "name_customer", "lastname_customer", "rut_customer", "address_customer",
                        "email_customer", "phone_customer"]
        self.columns_table = 7
        self.filter_combo.addItems(["Código", "Rut", "Email"])
        self.mapping_columns = {
            "Código": "cod_customer",
            "Rut": "rut_customer",
            "Email": "email_customer"}
        self.consultar_button.clicked.connect(self.read_row)
        self.layout.addLayout(self.filter_layout)
        self.filter_layout.addWidget(self.filter_label)
        self.filter_layout.addWidget(self.filter_combo)
        self.filter_layout.addWidget(self.search_label)
        self.filter_layout.addWidget(self.search_field)
        self.filter_layout.addWidget(self.consultar_button)

    def create_and_exec(self):
        form = ConsultarCliente()
        form.exec_()
