from formwindow import ConsultarFormularioWindow, ModificarFormularioWindow, BorrarFormularioWindow, \
    AgregarFormularioWindow


class AgregarRepuesto(AgregarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 700)
        self.title_label.setText("Crear Repuesto")
        self.table_name = 'repuesto'
        self.campos = ["Código (sku)", "Nombre", "Descripción", "Precio", "Stock"]
        self.columnas = ["cod_rep", "name_rep", "desc_rep", "price_rep", "stock"]
        self.field_list = []
        self.create_fields(self.campos, self.campos_layout)
        self.campos_layout.setContentsMargins(60, 20, 60, 20)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
        self.clear_fields

    def create_and_exec(self):
        form = AgregarRepuesto()
        form.exec_()


class BorrarRepuesto(BorrarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.set_title_text("Eliminar Repuesto")
        self.table_name = "repuesto"
        self.table_widget.setColumnCount(5)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Código", "Nombre", "Descripción", "Precio", "Stock"]
        self.columns = ["cod_rep", "name_rep", "desc_rep", "price_rep", "stock"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label.setText("Ingrese el código del cliente que desea eliminar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_borrar)
        self.layout.addWidget(self.borrar_button)

    def create_and_exec(self):
        form = BorrarRepuesto()
        form.exec_()


class ModificarRepuesto(ModificarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.set_title_text("Actualizar Respuesto")
        self.table_name = "repuesto"
        self.table_widget.setColumnCount(5)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Codigo", "Nombre", "Descripción", "Precio", "Stock"]
        self.columns = ["cod_rep", "name_rep", "desc_rep", "price_rep", "stock"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label.setText("Ingrese el código de repuesto que desea actualizar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_modificar)
        self.layout.addWidget(self.modificar_button)

    def create_and_exec(self):
        form = ModificarRepuesto()
        form.exec_()


class ConsultarRepuesto(ConsultarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.set_title_text("Buscar Respuesto")
        self.table_name = "repuesto"
        self.headers = ["Código", "Nombre", "Descripción", "Precio", "Stock"]
        self.columns = ["cod_rep", "name_rep", "desc_rep", "price_rep", "stock"]
        self.columns_table = 5
        self.filter_combo.addItems(["Código"])
        self.mapping_columns = {
            "Código": "cod_rep"}
        self.consultar_button.clicked.connect(self.read_row)
        self.layout.addLayout(self.filter_layout)
        self.filter_layout.addWidget(self.filter_label)
        self.filter_layout.addWidget(self.filter_combo)
        self.filter_layout.addWidget(self.search_label)
        self.filter_layout.addWidget(self.search_field)
        self.filter_layout.addWidget(self.consultar_button)

    def create_and_exec(self):
        form = ConsultarRepuesto()
        form.exec_()
