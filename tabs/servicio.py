from formwindow import Buscar, Actualizar, Crear, \
    Eliminar


class AgregarServicio(Crear):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 700)
        self.title_label.setText("Crear Servicio")
        self.table_name = 'servicio'
        self.campos = ["Código", "Nombre", "Descripción", "Precio"]
        self.columnas = ["cod_serv", "name_serv", "desc_serv", "price_serv"]
        self.field_list = []
        self.create_fields(self.campos, self.campos_layout)
        self.campos_layout.setContentsMargins(60, 20, 60, 20)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
        self.clear_fields

    def create_and_exec(self):
        form = AgregarServicio()
        form.exec_()


class BorrarServicio(Eliminar):
    def __init__(self):
        super().__init__()
        self.set_title_text("Eliminar Servicio")
        self.table_name = "servicio"
        self.table_widget.setColumnCount(4)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Código", "Nombre", "Descripción", "Precio"]
        self.columns = ["cod_serv", "name_serv", "desc_serv", "price_serv"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label.setText("Ingrese el código del servicio que desea eliminar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_borrar)
        self.layout.addWidget(self.borrar_button)

    def create_and_exec(self):
        form = BorrarServicio()
        form.exec_()


class ModificarServicio(Actualizar):
    def __init__(self):
        super().__init__()
        self.set_title_text("Actualizar Servicio")
        self.table_name = "servicio"
        self.table_widget.setColumnCount(4)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Codigo", "Nombre", "Descripción", "Precio"]
        self.columns = ["cod_serv", "name_serv", "desc_serv", "price_serv"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label.setText("Ingrese el código de servicio que desea actualizar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_modificar)
        self.layout.addWidget(self.modificar_button)

    def create_and_exec(self):
        form = ModificarServicio()
        form.exec_()


class ConsultarServicio(Buscar):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.set_title_text("Buscar Servicio")
        self.table_name = "servicio"
        self.headers = ["Código", "Nombre", "Descripción", "Precio"]
        self.columns = ["cod_serv", "name_serv", "desc_serv", "price_serv"]
        self.columns_table = 4
        self.filter_combo.addItems(["Código"])
        self.mapping_columns = {
            "Código": "cod_serv"}
        self.consultar_button.clicked.connect(self.read_row)
        self.layout.addLayout(self.filter_layout)
        self.filter_layout.addWidget(self.filter_label)
        self.filter_layout.addWidget(self.filter_combo)
        self.filter_layout.addWidget(self.search_label)
        self.filter_layout.addWidget(self.search_field)
        self.filter_layout.addWidget(self.consultar_button)

    def create_and_exec(self):
        form = ConsultarServicio()
        form.exec_()
