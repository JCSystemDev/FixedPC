import qdarkstyle
from PySide6.QtGui import QIcon, QPixmap, Qt, QFont
from PySide6.QtWidgets import QMainWindow, QTabWidget, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QLabel, \
    QMessageBox
import dao
import formwindow


class MainWindow(QMainWindow):
    def __init__(self, username, role):
        super().__init__()

        self.setWindowTitle("Main - Fixed PC")
        self.setFixedSize(800, 600)

        # Aplicar estilo oscuro
        self.setStyleSheet(qdarkstyle.load_stylesheet())

        # Establecer el icono de la ventana
        self.setWindowIcon(QIcon("img/icon.ico"))

        self.tab_widget = QTabWidget()

        # Verificar el rol del usuario y habilitar/deshabilitar las pestañas correspondientes
        self.check_user_role(role)

        widget_container = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.tab_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        widget_container.setLayout(layout)

        self.setCentralWidget(widget_container)

    def create_widget(self, num_buttons, button_names, name, image_path, description_text, button_functions):

        button_names = button_names[:num_buttons]

        buttons = []

        for name, func in zip(button_names, button_functions):
            button = QPushButton(name)
            button.clicked.connect(func)  # Asignar la función al evento clicked del botón
            buttons.append(button)

        widget = QWidget()
        layout = QVBoxLayout()

        description_label = QLabel(description_text)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setFont(QFont("Arial", 20))
        layout.addWidget(description_label)

        image_label = QLabel()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        description_label.setContentsMargins(0, 0, 0, 40)
        # Ajustar los márgenes del layout (arriba, izquierda, abajo, derecha)

        image_label.setContentsMargins(0, 0, 0, 180)
        # Ajustar los márgenes de la imagen (arriba, izquierda, derecha, abajo)

        crud_layout = QHBoxLayout()
        crud_layout.setContentsMargins(0, 0, 0, 0)
        # Ajustar los márgenes de la capa de botones (arriba, izquierda, abajo, derecha)

        for button in buttons:
            crud_layout.addWidget(button)

        layout.addLayout(crud_layout)
        widget.setLayout(layout)
        return widget

    def create_tab(self, num_buttons, button_names, name, path, title, button_functions):
        widget = self.create_widget(num_buttons, button_names, name, path, title, button_functions)
        self.tab_widget.addTab(widget, name)

    def check_user_role(self, role):
        if role == "administrador":

            self.create_tab(4, ["Agregar Ticket", "Borrar Ticket", "Modificar Ticket", "Consultar Ticket"],
                            "Ticket", "img/ticket.png", "Gestión de Tickets",
                            [formwindow.AgregarTicket.create_and_exec, formwindow.BorrarTicket.create_and_exec,
                             formwindow.ModificarTicket.create_and_exec, formwindow.ConsultarTicket.create_and_exec])

            self.create_tab(4, ["Agregar Usuario", "Borrar Usuario", "Modificar Usuario", "Consultar Usuario"],
                            "Usuario", "img/usuario.png", "Gestión de Usuarios",
                            [formwindow.AgregarCuenta.create_and_exec, formwindow.BorrarCuenta.create_and_exec,
                             formwindow.ModificarCuenta.create_and_exec, formwindow.ConsultarCuenta.create_and_exec])

            self.create_tab(4, ["Agregar Cliente", "Borrar Cliente", "Modificar Cliente", "Consultar Cliente"],
                            "Cliente", "img/cliente.png", "Gestión de Clientes",
                            [formwindow.AgregarCliente.create_and_exec, formwindow.BorrarCliente.create_and_exec,
                             formwindow.ModificarCliente.create_and_exec, formwindow.ConsultarCliente.create_and_exec])

            self.create_tab(4, ["Agregar Repuesto", "Borrar Repuesto", "Modificar Repuesto", "Consultar Repuesto"],
                            "Repuesto", "img/repuesto.png", "Gestión de Repuestos",
                            [formwindow.AgregarRepuesto.create_and_exec, formwindow.BorrarRepuesto.create_and_exec,
                             formwindow.ModificarRepuesto.create_and_exec, formwindow.ConsultarRepuesto.create_and_exec])

            self.create_tab(4, ["Agregar Servicio", "Borrar Servicio", "Modificar Servicio", "Consultar Servicio"],
                            "Servicio", "img/servicio.png", "Gestión de Servicios",
                            [formwindow.AgregarServicio.create_and_exec, formwindow.BorrarServicio.create_and_exec,
                             formwindow.ModificarServicio.create_and_exec, formwindow.ConsultarServicio.create_and_exec])

            self.create_tab(4, ["Agregar Empleado", "Borrar Empleado", "Modificar Empleado", "Consultar Empleado"],
                            "Empleado", "img/empleado.png", "Gestión de Empleados",
                            [formwindow.AgregarEmpleado.create_and_exec, formwindow.BorrarEmpleado.create_and_exec,
                             formwindow.ModificarEmpleado.create_and_exec, formwindow.ConsultarEmpleado.create_and_exec])

        elif role == "administrativo":

            self.create_tab(3, ["Agregar Empleado", "Modificar Empleado", "Consultar Empleado"],
                            "Empleado", "img/empleado.png", "Gestión de Empleados",
                            [formwindow.AgregarEmpleado.create_and_exec, formwindow.ModificarEmpleado.create_and_exec, formwindow.ConsultarEmpleado.create_and_exec])

            self.create_tab(3, ["Agregar Cliente", "Modificar Cliente", "Consultar Cliente"],
                            "Cliente", "img/cliente.png", "Gestión de Clientes",
                            [formwindow.AgregarCliente.create_and_exec, formwindow.ModificarCliente.create_and_exec, formwindow.ConsultarCliente.create_and_exec])


        elif role == "tecnico":

            self.create_tab(1, ["Consultar Repuesto"],
                            "Repuesto", "img/repuesto.png", "Gestión de Repuestos",
                            [formwindow.abrir_formagregar])

            self.create_tab(3, ["Agregar Servicio", "Modificar Servicio", "Consultar Servicio"],
                            "Servicio", "img/servicio.png", "Gestión de Servicios",
                            [formwindow.abrir_formagregar, dao.modificar, dao.consultar])


        elif role == "inventario":
            self.create_tab(3, ["Agregar Repuesto", "Modificar Repuesto", "Consultar Repuesto"],
                            "Repuesto", "img/repuesto.png", "Gestión de Repuestos",
                            [formwindow.abrir_formagregar, dao.modificar, dao.consultar])

        elif role == "recepcionista":

            self.create_tab(3, ["Agregar Ticket",  "Modificar Ticket", "Consultar Ticket"],
                            "Ticket", "img/ticket.png", "Gestión de Tickets",
                            [formwindow.abrir_formagregar, dao.modificar, dao.consultar])

            self.create_tab(3, ["Agregar Cliente", "Modificar Cliente", "Consultar Cliente"],
                            "Cliente", "img/cliente.png", "Gestión de Clientes",
                            [formwindow.abrir_formagregar, dao.modificar, dao.consultar])

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "¿Salir?",
            "¿Estás seguro de que deseas salir?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
