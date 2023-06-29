from PySide6.QtWidgets import QPushButton, QLabel

from formwindow import ConsultarFormularioWindow, ModificarFormularioWindow, BorrarFormularioWindow, \
    AgregarFormularioWindow


class AgregarCuenta(AgregarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 700)
        self.title_label.setText("Crear Cuenta")
        self.table_name = 'cuenta'
        self.campos = ["Nombre de usuario", "Contraseña", "Rol", "Código de empleado"]
        self.columnas = ["cod_user", "clave_user", "rol", "cod_emp"]
        self.field_list = []
        self.create_fields(self.campos, self.campos_layout)
        self.campos_layout.setContentsMargins(60, 20, 60, 20)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
        self.clear_fields

    def create_and_exec(self):
        form = AgregarCuenta()
        form.exec_()


class BorrarCuenta(BorrarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.set_title_text("Eliminar Usuario")
        self.table_name = "cuenta"
        self.table_widget.setColumnCount(4)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Nombre de Usuario", "Contraseña", "Rol", "Código de Empleado"]
        self.columns = ["cod_user", "clave_user", "rol", "cod_emp"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label = QLabel("Ingrese el nombre de usuario de la cuenta que desea eliminar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_borrar)
        self.layout.addWidget(self.borrar_button)

    def create_and_exec(self):
        form = BorrarCuenta()
        form.exec_()


class ModificarCuenta(ModificarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.set_title_text("Actualizar Cuenta")
        self.table_name = "cuenta"
        self.table_widget.setColumnCount(4)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Codigo", "Contraseña", "Rol", "Código de empleado"]
        self.columns = ["cod_user", "clave_user", "rol", "cod_emp"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label = QLabel("Ingrese el código de cuenta que desea actualizar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_modificar)
        self.layout.addWidget(self.modificar_button)

    def create_and_exec(self):
        form = ModificarCuenta()
        form.exec_()


class ConsultarCuenta(ConsultarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.set_title_text("Buscar Cuenta")
        self.table_name = "cuenta"
        self.headers = ["Nombre de Usuario", "Contraseña", "Rol", "Código de empleado"]
        self.columns = ["cod_user", "clave_user", "rol", "cod_emp"]
        self.columns_table = 4
        self.filter_combo.addItems(["Usuario", "Rol", "Empleado"])
        self.mapping_columns = {
            "Usuario": "cod_user",
            "Rol": "rol",
            "Código de empleado": "cod_emp"}
        self.consultar_button = QPushButton("Consultar")
        self.consultar_button.clicked.connect(self.read_row)
        self.layout.addLayout(self.filter_layout)
        self.filter_layout.addWidget(self.filter_label)
        self.filter_layout.addWidget(self.filter_combo)
        self.filter_layout.addWidget(self.search_label)
        self.filter_layout.addWidget(self.search_field)
        self.filter_layout.addWidget(self.consultar_button)

    def create_and_exec(self):
        form = ConsultarCuenta()
        form.exec_()