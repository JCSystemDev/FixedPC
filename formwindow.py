import hashlib
from datetime import datetime
import os
import qdarkstyle
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLineEdit, QMessageBox, \
     QTableWidget, QTableWidgetItem, QAbstractItemView, QInputDialog, QComboBox
from PySide6.QtCore import Qt
from fpdf import FPDF

import dao
# import notifications


class FormWindow(QDialog):
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
        self.ticket_state_list = ["abierto", "pendiente", "cerrado"]
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


class Crear(FormWindow):
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


class Eliminar(FormWindow):
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
        self.codigo_label = QLabel()
        self.codigo_borrar = QLineEdit()
        self.borrar_button = QPushButton("Eliminar")
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


class Actualizar(FormWindow):
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
        self.codigo_label = QLabel()
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


class Buscar(FormWindow):
    def __init__(self):
        super().__init__()
        self.table_name = ""
        self.setWindowTitle("Fixed PC - Consultar")
        self.image_path = "img/buscar.png"
        self.update_image()
        # Create filter options
        self.filter_layout = QVBoxLayout()
        self.filter_label = QLabel("Filtro de búsqueda:")
        self.filter_combo = QComboBox()
        # Create search field
        self.search_label = QLabel("Elemento a buscar:")
        self.consultar_button = QPushButton("Buscar")
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


class Reporte(FormWindow):
    pass


class Facturacion(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet())
        self.setWindowIcon(QIcon("img/icon.ico"))
        self.setWindowTitle("Crear Facturación")

        self.code_label = QLabel("Ingrese el código de facturación:")
        self.code_lineedit = QLineEdit()
        self.create_button = QPushButton("Crear Facturación")
        self.total_neto = 0
        self.code_customer = 0
        self.customer_name = ""
        self.phone_customer = ""
        self.replace_chars = "'(),"
        self.replace_table = str.maketrans("", "", self.replace_chars)
        self.date_today = datetime.now()
        self.date_today = self.date_today.strftime("%d-%m-%Y")
        self.total_iva = 0
        self.create_button.clicked.connect(self.create_billing)
        layout = QVBoxLayout()
        layout.addWidget(self.code_label)
        layout.addWidget(self.code_lineedit)
        layout.addWidget(self.create_button)
        self.setLayout(layout)

    def create_billing(self):
        self.code = self.code_lineedit.text().strip()
        if not self.code:
            QMessageBox.warning(self, "Error", "El código de facturación no puede estar vacío.")
            return

        # Realizar consulta para obtener los datos de ticketservicio y ticketrepuesto
        fdao = dao.DAO()
        query_serv = f"SELECT s.cod_serv, s.name_serv, s.price_serv " \
                     "FROM ticketservicio ts " \
                     "JOIN servicio s ON ts.cod_serv = s.cod_serv " \
                     "WHERE ts.cod_fact = {self.code} AND ts.state_ticket = 'cerrado' "
        result_serv = fdao.mostrar(query_serv)
        query_rep = f"SELECT s.cod_rep, s.name_rep, s.price_rep " \
                    "FROM ticketrepuesto ts " \
                    "JOIN repuesto s ON ts.cod_rep = s.cod_rep " \
                    "WHERE ts.cod_fact = {self.code} AND ts.state_ticket = 'cerrado' "
        result_rep = fdao.mostrar(query_rep)
        query_customer = f"SELECT CONCAT(c.name_customer, ' ', c.lastname_customer) AS nombre_customer " \
                         f"FROM ticketservicio ts JOIN cliente c ON ts.cod_customer = c.cod_customer " \
                         f"WHERE ts.cod_fact = {self.code}"
        result_customer = fdao.mostrar(query_customer)
        self.customer_name = str(result_customer[0])
        self.customer_name = self.customer_name.translate(self.replace_table)

        query_phone = f"SELECT c.phone_customer FROM ticketservicio ts JOIN cliente c " \
                      f"ON ts.cod_customer = c.cod_customer WHERE ts.cod_fact = {self.code} "
        result_phone = fdao.mostrar(query_phone)

        self.phone_customer = str(result_phone[0])
        self.phone_customer = self.phone_customer.translate(self.replace_table)
        print(self.phone_customer)

        fdao.cerrar_conexion()

        if not result_serv and not result_rep:
            QMessageBox.information(self, "Información",
                                    "No se encontraron datos para el código de facturación ingresado.")
            return

        # Crear el documento PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Configurar estilo de fuente
        pdf.set_font(family="Arial", style="B", size=12)

        # Agregar encabezado
        pdf.cell(0, 10, f"Facturación: {self.code}", ln=True, align="C")
        pdf.ln(5)

        # Agregar nombre del cliente
        pdf.cell(0, 10, f"Cliente: {self.customer_name}", ln=True)

        # # Agregar fecha de facturación
        pdf.cell(0, 10, f"Fecha: {self.date_today}", ln=True)
        pdf.ln(5)

        # Agregar tabla con los datos de los servicios y repuestos
        headers = ["Item", "Descripción", "Valor Neto"]
        pdf.set_font(family="Arial", style="B", size=12)
        for header in headers:
            pdf.cell(50, 10, header, border=1)
        pdf.ln(10)

        # Agregar los datos de los servicios
        self.add_data_to_pdf(pdf, result_serv)
        total_neto_serv = self.total_neto

        # Agregar los datos de los repuestos
        self.add_data_to_pdf(pdf, result_rep)
        total_neto_rep = self.total_neto

        # Calcular totales
        pdf.ln(10)
        pdf.cell(0, 10, f"Total Neto Servicios: ${total_neto_serv}", ln=True)
        pdf.cell(0, 10, f"Total Neto Repuestos: ${total_neto_rep}", ln=True)
        pdf.cell(0, 10, f"Total Neto: ${total_neto_serv + total_neto_rep}", ln=True)
        self.total_iva = int((total_neto_serv + total_neto_rep) * 0.19)
        pdf.cell(0, 10, f"IVA (19%): ${self.total_iva}", ln=True)
        pdf.cell(0, 10, f"Total con IVA: $"f"{int(self.total_iva + total_neto_serv + total_neto_rep)}", ln=True)
        pdf.ln(10)

        # Agregar pie de página
        pdf.set_font("Arial", size=10, style="I")
        pdf.cell(0, 10, "FIXED PC - 2023", ln=True, align="C")

        # Guardar el documento PDF
        pdf_directory = "facturaciones"
        pdf_filename = f"{self.code}.pdf"
        pdf_path = os.path.join(pdf_directory, pdf_filename)
        os.makedirs(pdf_directory, exist_ok=True)
        pdf.output(pdf_path)

        fdao = dao.DAO()
        query = f"INSERT INTO factura " \
                f"(cod_fact, name_customer, valor_total_neto, valor_total_iva, valor_total, fecha_fact) " \
                f"VALUES ({self.code}, '{self.customer_name}', {total_neto_serv + total_neto_rep}, {self.total_iva}, " \
                f"{int(self.total_iva + total_neto_serv + total_neto_rep)}, '{datetime.now()}')"
        fdao.crear(query)
        fdao.cerrar_conexion()
        QMessageBox.information(self, "Información", f"Se ha creado el documento PDF: {pdf_filename}")
        hora_actual = datetime.now()
        hora = hora_actual.hour
        minuto = hora_actual.minute + 1
        print(hora, minuto)

        # Enviar el mensaje 1 minuto después de la hora actual (Por ahora no se usará)
        """
        notifications.enviar_mensaje_despues(self.phone_customer, f"Hola {self.customer_name},"
                                                           f" su pedido esta listo para retiro." \
                                                           f" Su número de facturación es {self.code}"
                                                           f" y el valor total es por " \
                                                           f"${int(self.total_iva + total_neto_serv + total_neto_rep)}"
                                             , hora, minuto)
        """

    def add_data_to_pdf(self, pdf, data_list):
        pdf.set_font(family="Arial", size=12)
        self.total_neto = 0
        for data in data_list:
            item = data[0]
            desc = data[1]
            price = data[2]

            self.total_neto += int(price)
            pdf.cell(50, 10, item, border=1)
            pdf.cell(50, 10, desc, border=1)
            pdf.cell(50, 10, f"${price}", border=1)
            pdf.ln()

    def create_and_exec(self):
        form = Facturacion()
        form.exec_()
