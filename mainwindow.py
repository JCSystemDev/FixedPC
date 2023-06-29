import qdarkstyle
from PySide6.QtGui import QIcon, QPixmap, Qt, QFont
from PySide6.QtWidgets import QMainWindow, QTabWidget, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QLabel, \
    QMessageBox
import clienteservice
import cuentaservice
import empleadoservice
import repuestoservice
import servicioservice
import ticketservice


class MainWindow(QMainWindow):
    def __init__(self, username, role):
        super().__init__()

        self.setWindowTitle("Main - Fixed PC")
        self.setFixedSize(1024, 640)

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

            self.create_tab(4, ["Crear Ticket", "Eliminar Ticket", "Actualizar Ticket", "Buscar Ticket"],
                            "Ticket", "img/ticket.png", "Gestión de Tickets de reparación",
                            [ticketservice.AgregarTicket.create_and_exec,
                             ticketservice.BorrarTicket.create_and_exec,
                             ticketservice.ModificarTicket.create_and_exec,
                             ticketservice.ConsultarTicket.create_and_exec])

            self.create_tab(4, ["Crear Cuenta", "Eliminar Cuenta", "Actualizar Cuenta", "Buscar Cuenta"],
                            "Usuario", "img/usuario.png", "Gestión de Cuentas de Usuario",
                            [cuentaservice.AgregarCuenta.create_and_exec,
                             cuentaservice.BorrarCuenta.create_and_exec,
                             cuentaservice.ModificarCuenta.create_and_exec,
                             cuentaservice.ConsultarCuenta.create_and_exec])

            self.create_tab(4, ["Crear Cliente", "Eliminar Cliente", "Actualizar Cliente", "Buscar Cliente"],
                            "Cliente", "img/cliente.png", "Gestión de Clientes",
                            [clienteservice.AgregarCliente.create_and_exec,
                             clienteservice.BorrarCliente.create_and_exec,
                             clienteservice.ModificarCliente.create_and_exec,
                             clienteservice.ConsultarCliente.create_and_exec])

            self.create_tab(4, ["Crear Repuesto", "Eliminar Repuesto", "Actualizar Repuesto", "Buscar Repuesto"],
                            "Repuesto", "img/repuesto.png", "Gestión de Inventario de Repuestos",
                            [repuestoservice.AgregarRepuesto.create_and_exec,
                             repuestoservice.BorrarRepuesto.create_and_exec,
                             repuestoservice.ModificarRepuesto.create_and_exec,
                             repuestoservice.ConsultarRepuesto.create_and_exec])

            self.create_tab(4, ["Crear Servicio", "Eliminar Servicio", "Actualizar Servicio", "Buscar Servicio"],
                            "Servicio", "img/servicio.png", "Gestión de Servicios",
                            [servicioservice.AgregarServicio.create_and_exec,
                             servicioservice.BorrarServicio.create_and_exec,
                             servicioservice.ModificarServicio.create_and_exec,
                             servicioservice.ConsultarServicio.create_and_exec])

            self.create_tab(4, ["Crear Empleado", "Eliminar Empleado", "Actualizar Empleado", "Buscar Empleado"],
                            "Empleado", "img/empleado.png", "Gestión de Empleados",
                            [empleadoservice.AgregarEmpleado.create_and_exec,
                             empleadoservice.BorrarEmpleado.create_and_exec,
                             empleadoservice.ModificarEmpleado.create_and_exec,
                             empleadoservice.ConsultarEmpleado.create_and_exec])

        elif role == "administrativo":

            self.create_tab(3, ["Crear Empleado", "Actualizar Empleado", "Buscar Empleado"],
                            "Empleado", "img/empleado.png", "Gestión de Empleados",
                            [empleadoservice.AgregarEmpleado.create_and_exec,
                             empleadoservice.ModificarEmpleado.create_and_exec,
                             empleadoservice.ConsultarEmpleado.create_and_exec])

            self.create_tab(3, ["Crear Cliente", "Actualizar Cliente", "Buscar Cliente"],
                            "Cliente", "img/cliente.png", "Gestión de Clientes",
                            [clienteservice.AgregarCliente.create_and_exec,
                             clienteservice.ModificarCliente.create_and_exec,
                             clienteservice.ConsultarCliente.create_and_exec])

        elif role == "tecnico":

            self.create_tab(1, ["Buscar Repuesto"],
                            "Repuesto", "img/repuesto.png", "Gestión de Repuestos",
                            [repuestoservice.ConsultarRepuesto.create_and_exec])

            self.create_tab(3, ["Crear Servicio", "Actualizar Servicio", "Buscar Servicio"],
                            "Servicio", "img/servicio.png", "Gestión de Servicios",
                            [servicioservice.AgregarServicio.create_and_exec,
                             servicioservice.ModificarServicio.create_and_exec,
                             servicioservice.ConsultarServicio.create_and_exec])

        elif role == "inventario":
            self.create_tab(3, ["Crear Repuesto", "Actualizar Repuesto", "Buscar Repuesto"],
                            "Repuesto", "img/repuesto.png", "Gestión de Repuestos",
                            [repuestoservice.AgregarRepuesto.create_and_exec,
                             repuestoservice.ModificarRepuesto.create_and_exec,
                             repuestoservice.ConsultarRepuesto.create_and_exec])

        elif role == "recepcionista":

            self.create_tab(3, ["Crear Ticket",  "Actualizar Ticket", "Buscar Ticket"],
                            "Ticket", "img/ticket.png", "Gestión de Tickets",
                            [ticketservice.AgregarTicket.create_and_exec,
                             ticketservice.ModificarTicket.create_and_exec,
                             ticketservice.ConsultarTicket.create_and_exec])

            self.create_tab(3, ["Crear Cliente", "Actualizar Cliente", "Buscar Cliente"],
                            "Cliente", "img/cliente.png", "Gestión de Clientes",
                            [clienteservice.AgregarCliente.create_and_exec,
                             clienteservice.ModificarCliente.create_and_exec,
                             clienteservice.ConsultarCliente.create_and_exec])

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
