import hashlib

import qdarkstyle
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLineEdit, QMessageBox, \
     QTableWidget, QTableWidgetItem, QAbstractItemView, QInputDialog, QComboBox
from PySide6.QtCore import Qt
import dao


class FormularioWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet())
        self.setWindowIcon(QIcon("img/icon.ico"))
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 20))
        self.layout.addWidget(self.title_label)
        self.image_label = QLabel()
        self.image_path = ""
        self.pixmap = QPixmap(self.image_path)
        self.pixmap = self.pixmap.scaled(128, 128)
        self.image_label.setPixmap(self.pixmap)
        self.layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

    def set_title_text(self, text):
        self.title_label.setText(text)

    def update_image(self):
        self.pixmap = QPixmap(self.image_path)
        self.pixmap = self.pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(self.pixmap)

    def create_table(self):
        # Obtener los datos de la tabla "finanza" usando el DAO
        columns = self.columns
        column_names = ', '.join(columns)
        fdao = dao.DAO()
        query = f"SELECT {column_names} FROM {self.table_name}"
        result = fdao.mostrar(query)
        fdao.cerrar_conexion()

        # Establecer el número de filas en función del resultado de la consulta
        self.table_widget.setRowCount(len(result))

        # Agregar los datos a la tabla
        for row_index, row_data in enumerate(result):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.table_widget.setItem(row_index, col_index, item)


class AgregarFormularioWindow(FormularioWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fixed PC - Agregar")
        self.image_path = "img/agregar.png"
        self.update_image()
        self.campos_layout = QVBoxLayout()
        self.layout.addLayout(self.campos_layout)
        self.button_layout = QHBoxLayout()
        self.agregar_button = QPushButton("Agregar")
        self.agregar_button.clicked.connect(self.insert_row)
        self.button_layout.addWidget(self.agregar_button)
        self.layout.addLayout(self.button_layout)
        self.field_values = []
        self.autoincrement = False

    def create_fields(self, campos, layout):
        for campo in campos:
            label = QLabel(campo)
            field = QLineEdit()
            if campo == "Contraseña":
                field.setEchoMode(QLineEdit.Password)
            layout.addWidget(label)
            layout.addWidget(field)
            self.field_list.append(field)
            field.textChanged.connect(self.update_field_values)

    def update_field_values(self):
        self.field_values = [field.text() for field in self.field_list]

    def clear_fields(self):
        for field in self.field_list:
            field.clear()

    def insert_row(self):
        columns = self.columnas
        values = self.field_values

        if columns[1] == "clave_user":
            values[1] = hashlib.sha256(values[1].encode('utf-8')).hexdigest()

        column_names = ', '.join(columns)
        if self.autoincrement:
            values.insert(0, "0")
            field_values = "','".join(values)
        else:
            field_values = "','".join(values)

        # Verificar si algún campo está vacío
        if len(self.field_values) < len(self.columnas):
            QMessageBox.critical(self, "Error", "Todos los campos deben ser completados.")
            return

        # Crear la consulta de inserción con los valores de los campos
        query = f"INSERT INTO {self.table_name} ({column_names}) VALUES ('{field_values}')"

        # Crear una instancia del DAO y ejecutar la consulta de inserción
        daof = dao.DAO()
        try:
            daof.crear(query)
            daof.cerrar_conexion()
            self.clear_fields()
            QMessageBox.information(self, "", "El Documento se ha agregado correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar el Documento.\nError: {str(e)}")


class BorrarFormularioWindow(FormularioWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fixed PC - Eliminar")
        self.setFixedSize(550, 600)
        self.image_path = "img/borrar.png"
        self.update_image()
        self.headers = []
        self.columns = []
        self.table_widget = QTableWidget()
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.codigo_borrar = QLineEdit()
        self.borrar_button = QPushButton("Borrar")
        self.borrar_button.clicked.connect(self.delete_row)

    def delete_row(self):
        codigo_borrar = self.codigo_borrar.text()
        columns = self.columns
        column_names = ', '.join(columns)

        # Verificar si se ingresó un código válido
        if codigo_borrar:
            # Consultar si el código existe en la tabla "finanza"
            fdao = dao.DAO()
            query_buscar = f"SELECT {column_names} FROM {self.table_name} WHERE {columns[0]} = '{codigo_borrar}'"
            resultado = fdao.buscar(query_buscar)
            fdao.cerrar_conexion()

            if resultado:
                # Mostrar mensaje de confirmación
                reply = QMessageBox.question(self, "Confirmación", f"¿Deseas borrar el elemento {codigo_borrar}?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # Realizar el borrado en la base de datos usando el DAO
                    fdao = dao.DAO()
                    query_eliminar = f"DELETE FROM {self.table_name} WHERE {columns[0]} = '{codigo_borrar}'"
                    filas_afectadas = fdao.eliminar(query_eliminar)
                    fdao.cerrar_conexion()

                    if filas_afectadas > 0:
                        # Eliminar la fila de la tabla
                        for row in range(self.table_widget.rowCount()):
                            codigo_celda = self.table_widget.item(row, 0).text()
                            if codigo_celda == codigo_borrar:
                                self.table_widget.removeRow(row)
                                break

                        QMessageBox.information(self, "Éxito", "El elemento se ha borrado correctamente.")
                    else:
                        QMessageBox.warning(self, "Error", "No se pudo borrar el elemento.")
                else:
                    QMessageBox.information(self, "Cancelado", "La operación ha sido cancelada.")
            else:
                QMessageBox.warning(self, "Error", "ELemento no encontrado.")
        else:
            QMessageBox.warning(self, "Error", "Ingrese un código válido.")
        self.codigo_borrar.clear()


class ModificarFormularioWindow(FormularioWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fixed PC - Modificar")
        self.setFixedSize(550, 600)
        self.image_path = "img/modificar.png"
        self.update_image()
        self.headers = []
        self.columns = []
        self.table_widget = QTableWidget()
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.codigo_modificar = QLineEdit()
        self.modificar_button = QPushButton("Actualizar")
        self.modificar_button.clicked.connect(self.update_row)

    def update_row(self):
        codigo_modificar = self.codigo_modificar.text()
        columns = self.columns
        column_names = ', '.join(columns)

        if codigo_modificar:
            fdao = dao.DAO()
            query_buscar = f"SELECT {column_names} FROM {self.table_name} WHERE {columns[0]} = '{codigo_modificar}'"
            resultado = fdao.buscar(query_buscar)
            fdao.cerrar_conexion()

            if resultado:
                # Mostrar mensaje de confirmación
                reply = QMessageBox.question(self, "Confirmación", f"¿Deseas modificar el elemento {codigo_modificar}?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    fdao = dao.DAO()
                    column_values = {}
                    new_values = []
                    for header, column in zip(self.headers[1:], self.columns[1:]):
                        new_value, ok = QInputDialog.getText(self, "Actualizar",
                                                             f"Ingrese nuevo valor para '{header}':",
                                                             QLineEdit.Normal, "")
                        if ok:
                            column_values[column] = new_value
                            new_values.append(new_value)

                    if column_values:  # Verificar si se han ingresado datos para actualizar
                        update_columns = ", ".join(f"{column} = %s" for column in column_values.keys())
                        query_actualizar = f"UPDATE {self.table_name} SET {update_columns} WHERE {self.columns[0]} = %s"
                        new_values.append(codigo_modificar)

                        fdao.modificar(query_actualizar, new_values)
                        fdao.cerrar_conexion()
                    QMessageBox.information(self, "Éxito", "El elemento se ha actualizado correctamente.")
                    self.create_table()

                else:
                    QMessageBox.information(self, "Confirmación", "No se realizaron cambios en los datos del elemento.")

            else:
                QMessageBox.warning(self, "Error", "Elemento no encontrado.")

        else:
            QMessageBox.warning(self, "Error", "Ingrese un código válido.")

        self.codigo_modificar.clear()


class AgregarCliente(AgregarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 700)
        self.title_label.setText("Agregar Cliente")
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


class AgregarEmpleado(AgregarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 700)
        self.title_label.setText("Agregar Empleado")
        self.table_name = 'empleado'
        self.campos = ["Nombre", "Apellido", "Cargo", "Rut", "Fecha de ingreso", "Fecha de salida"]
        self.columnas = ["cod_emp", "name_emp", "lastname_emp", "job_title", "rut_emp", "hire_date", "dep_date"]
        self.field_list = []
        self.autoincrement = True
        self.create_fields(self.campos, self.campos_layout)
        self.campos_layout.setContentsMargins(60, 20, 60, 20)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
        self.clear_fields

    def create_and_exec(self):
        form = AgregarEmpleado()
        form.exec_()


class AgregarTicket(AgregarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 700)
        self.title_label.setText("Agregar Ticket")
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


class AgregarCuenta(AgregarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 700)
        self.title_label.setText("Agregar Cuenta")
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


class AgregarRepuesto(AgregarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 700)
        self.title_label.setText("Agregar Repuesto")
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


class AgregarServicio(AgregarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 700)
        self.title_label.setText("Agregar Servicio")
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


class BorrarCliente(BorrarFormularioWindow):
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
        self.codigo_label = QLabel("Ingrese el código del cliente que desea eliminar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_borrar)
        self.layout.addWidget(self.borrar_button)

    def create_and_exec(self):
        form = BorrarCliente()
        form.exec_()


class BorrarEmpleado(BorrarFormularioWindow):
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
        self.codigo_label = QLabel("Ingrese el código del empleado que desea eliminar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_borrar)
        self.layout.addWidget(self.borrar_button)

    def create_and_exec(self):
        form = BorrarEmpleado()
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
        self.codigo_label = QLabel("Ingrese el código del cliente que desea eliminar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_borrar)
        self.layout.addWidget(self.borrar_button)

    def create_and_exec(self):
        form = BorrarRepuesto()
        form.exec_()


class BorrarServicio(BorrarFormularioWindow):
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
        self.codigo_label = QLabel("Ingrese el código del servicio que desea eliminar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_borrar)
        self.layout.addWidget(self.borrar_button)

    def create_and_exec(self):
        form = BorrarServicio()
        form.exec_()


class ModificarCliente(ModificarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.set_title_text("Modificar Cliente")
        self.table_name = "cliente"
        self.table_widget.setColumnCount(7)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Codigo", "Nombre", "Apellido", "Rut", "Dirección", "Email", "Teléfono"]
        self.columns = ["cod_customer", "name_customer", "lastname_customer", "rut_customer", "address_customer",
                        "email_customer", "phone_customer"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label = QLabel("Ingrese el código de cliente que desea actualizar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_modificar)
        self.layout.addWidget(self.modificar_button)

    def create_and_exec(self):
        form = ModificarCliente()
        form.exec_()


class ModificarCuenta(ModificarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.set_title_text("Modificar Cuenta")
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


class ModificarEmpleado(ModificarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.set_title_text("Modificar Empleado")
        self.table_name = "empleado"
        self.table_widget.setColumnCount(7)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Codigo", "Nombre", "Apellido", "Cargo", "Rut", "Fecha de contratación", "Fecha de retiro"]
        self.columns = ["cod_emp", "name_emp", "lastname_emp", "job_title", "rut_emp", "hire_date", "dep_date"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label = QLabel("Ingrese el código de empleado que desea actualizar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_modificar)
        self.layout.addWidget(self.modificar_button)

    def create_and_exec(self):
        form = ModificarEmpleado()
        form.exec_()


class ModificarRepuesto(ModificarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.set_title_text("Modificar Respuesto")
        self.table_name = "repuesto"
        self.table_widget.setColumnCount(5)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Codigo", "Nombre", "Descripción", "Precio", "Stock"]
        self.columns = ["cod_rep", "name_rep", "desc_rep", "price_rep", "stock"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label = QLabel("Ingrese el código de repuesto que desea actualizar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_modificar)
        self.layout.addWidget(self.modificar_button)

    def create_and_exec(self):
        form = ModificarRepuesto()
        form.exec_()


class ModificarServicio(ModificarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.set_title_text("Modificar Servicio")
        self.table_name = "servicio"
        self.table_widget.setColumnCount(4)
        self.layout.addWidget(self.table_widget)
        self.headers = ["Codigo", "Nombre", "Descripción", "Precio"]
        self.columns = ["cod_serv", "name_serv", "desc_serv", "price_serv"]
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        self.create_table()
        self.codigo_label = QLabel("Ingrese el código de servicio que desea actualizar")
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_modificar)
        self.layout.addWidget(self.modificar_button)

    def create_and_exec(self):
        form = ModificarServicio()
        form.exec_()


class ModificarTicket(ModificarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.set_title_text("Modificar Ticket")
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


class ConsultarFormularioWindow(FormularioWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fixed PC - Consultar")
        self.image_path = "img/buscar.png"
        self.update_image()
        # Create filter options
        self.filter_layout = QVBoxLayout()
        self.filter_label = QLabel("Filtro de búsqueda:")
        self.filter_combo = QComboBox()
        # Create search field
        self.search_label = QLabel("Buscar:")
        self.search_field = QLineEdit()
        self.headers = []
        self.columns = []
        self.mapping_columns = {}
        self.columns_table = 0

    def read_row(self):
        filtro = self.filter_combo.currentText()
        valor_busqueda = self.search_field.text()
        columns = self.columns
        column_names = ', '.join(columns)

        if valor_busqueda:
            # Map the filter selection to the corresponding column name
            columna = self.mapping_columns.get(filtro, "")
            # Get the corresponding column name, or empty string if not found

            if columna:
                # Query the "finanza" table based on the selected filter and search value
                fdao = dao.DAO()
                query_buscar = f"SELECT {column_names} " \
                               f"FROM {self.table_name} WHERE {columna} = '{valor_busqueda}'"
                resultado = fdao.mostrar(query_buscar)
                fdao.cerrar_conexion()

                if resultado:
                    # Show the results in a dialog with a non-editable table
                    dialog = QDialog(self)
                    dialog.setWindowTitle("Resultado de la Consulta")
                    dialog.setFixedSize(550, 400)

                    layout = QVBoxLayout(dialog)
                    layout.setContentsMargins(20, 20, 20, 20)

                    table_widget = QTableWidget()
                    table_widget.setColumnCount(self.columns_table)
                    table_widget.setHorizontalHeaderLabels(self.headers)
                    table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
                    table_widget.setRowCount(len(resultado))

                    for row_index, row_data in enumerate(resultado):
                        for col_index, col_data in enumerate(row_data):
                            item = QTableWidgetItem(str(col_data))
                            table_widget.setItem(row_index, col_index, item)

                    layout.addWidget(table_widget)
                    dialog.setLayout(layout)
                    dialog.exec_()
                else:
                    QMessageBox.warning(self, "Error", "Documento no encontrado en la tabla.")
            else:
                QMessageBox.warning(self, "Error", "Selecciona un campo de búsqueda válido.")
        else:
            QMessageBox.warning(self, "Error", "Ingresa un valor de búsqueda válido.")

        self.search_field.clear()


class ConsultarTicket(ConsultarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.set_title_text("Consultar Ticket")
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


class ConsultarCliente(ConsultarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.set_title_text("Consultar Cliente")
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
        self.consultar_button = QPushButton("Consultar")
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


class ConsultarCuenta(ConsultarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.set_title_text("Consultar Cuenta")
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


class ConsultarEmpleado(ConsultarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.set_title_text("Consultar Empleado")
        self.table_name = "empleado"
        self.headers = ["Código", "Nombre", "Apellido", "Cargo", "Rut", "Fecha de contratación", "Fecha de retiro"]
        self.columns = ["cod_emp", "name_emp", "lastname_emp", "job_title", "rut_emp", "hire_date", "dep_date"]
        self.columns_table = 7
        self.filter_combo.addItems(["Código", "Rut", "Cargo"])
        self.mapping_columns = {
            "Código": "cod_emp",
            "Rut": "rut_emp",
            "Cargo": "job_title"}
        self.consultar_button = QPushButton("Consultar")
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


class ConsultarRepuesto(ConsultarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.set_title_text("Consultar Respuesto")
        self.table_name = "repuesto"
        self.headers = ["Código", "Nombre", "Descripción", "Precio", "Stock"]
        self.columns = ["cod_rep", "name_rep", "desc_rep", "price_rep", "stock"]
        self.columns_table = 5
        self.filter_combo.addItems(["Código"])
        self.mapping_columns = {
            "Código": "cod_rep"}
        self.consultar_button = QPushButton("Consultar")
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


class ConsultarServicio(ConsultarFormularioWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.set_title_text("Consultar Servicio")
        self.table_name = "servicio"
        self.headers = ["Código", "Nombre", "Descripción", "Precio"]
        self.columns = ["cod_serv", "name_serv", "desc_serv", "price_serv"]
        self.columns_table = 4
        self.filter_combo.addItems(["Código"])
        self.mapping_columns = {
            "Código": "cod_serv"}
        self.consultar_button = QPushButton("Consultar")
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
