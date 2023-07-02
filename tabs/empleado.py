from formwindow import Buscar, Actualizar, Eliminar, \
    Crear


class AgregarEmpleado(Crear):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 700)
        self.title_label.setText("Crear Empleado")
        self.table_name = 'empleado'
        self.campos = ["Nombre", "Apellido", "Cargo", "Rut", "Fecha de ingreso"]
        self.columnas = ["cod_emp", "name_emp", "lastname_emp", "job_title", "rut_emp", "hire_date"]
        self.field_list = []
        self.autoincrement = True
        self.create_fields(self.campos, self.campos_layout)
        self.campos_layout.setContentsMargins(60, 20, 60, 20)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
        self.clear_fields()

    def create_and_exec(self):
        form = AgregarEmpleado()
        form.exec_()


class BorrarEmpleado(Eliminar):
    def __init__(self):
        super().__init__()
        self.set_title_text("Eliminar Empleado")
        self.table_name = "empleado"
        self.table_widget.setColumnCount(7)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Código", "Nombre", "Apellido", "Cargo", "Rut", "Fecha de contratación", "Fecha de retiro"]
        self.columns = ["cod_emp", "name_emp", "lastname_emp", "job_title", "rut_emp", "hire_date", "dep_date"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label.setText("Ingrese el código del empleado que desea eliminar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_borrar)
        self.layout.addWidget(self.borrar_button)

    def create_and_exec(self):
        form = BorrarEmpleado()
        form.exec_()


class ModificarEmpleado(Actualizar):
    def __init__(self):
        super().__init__()
        self.set_title_text("Actualizar Empleado")
        self.table_name = "empleado"
        self.table_widget.setColumnCount(7)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Codigo", "Nombre", "Apellido", "Cargo", "Rut", "Fecha de contratación", "Fecha de retiro"]
        self.columns = ["cod_emp", "name_emp", "lastname_emp", "job_title", "rut_emp", "hire_date", "dep_date"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label.setText("Ingrese el código de empleado que desea actualizar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_modificar)
        self.layout.addWidget(self.modificar_button)

    def create_and_exec(self):
        form = ModificarEmpleado()
        form.exec_()


class ConsultarEmpleado(Buscar):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.set_title_text("Buscar Empleado")
        self.table_name = "empleado"
        self.headers = ["Código", "Nombre", "Apellido", "Cargo", "Rut", "Fecha de contratación", "Fecha de retiro"]
        self.columns = ["cod_emp", "name_emp", "lastname_emp", "job_title", "rut_emp", "hire_date", "dep_date"]
        self.columns_table = 7
        self.filter_combo.addItems(["Código", "Rut", "Cargo"])
        self.mapping_columns = {
            "Código": "cod_emp",
            "Rut": "rut_emp",
            "Cargo": "job_title"}
        self.consultar_button.clicked.connect(self.read_row)
        self.layout.addLayout(self.filter_layout)
        self.filter_layout.addWidget(self.filter_label)
        self.filter_layout.addWidget(self.filter_combo)
        self.filter_layout.addWidget(self.search_label)
        self.filter_layout.addWidget(self.search_field)
        self.filter_layout.addWidget(self.consultar_button)

    def create_and_exec(self):
        form = ConsultarEmpleado()
        form.exec_()
