-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-07-2023 a las 07:08:37
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `fixedpc`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `cod_customer` int(11) NOT NULL COMMENT 'El código del cliente',
  `name_customer` varchar(20) NOT NULL COMMENT 'Nombre del cliente',
  `lastname_customer` varchar(20) NOT NULL COMMENT 'Apellido del cliente',
  `rut_customer` varchar(10) NOT NULL COMMENT 'Rut del cliente',
  `address_customer` varchar(40) DEFAULT NULL COMMENT 'Dirección del cliente',
  `email_customer` varchar(25) DEFAULT NULL COMMENT 'Correo electrónico del cliente',
  `phone_customer` varchar(12) DEFAULT NULL COMMENT 'Teléfono del cliente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci COMMENT='Todos los clientes que ha tenido la empresa.';

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`cod_customer`, `name_customer`, `lastname_customer`, `rut_customer`, `address_customer`, `email_customer`, `phone_customer`) VALUES
(2000, 'Pepito', 'Perez', '10999999-9', 'Los Pepinos #5050, Rancagua', 'p.perez@email.cl', '+56987554322'),
(2001, 'Alejandro', 'Fernandez', '11888888-8', 'Los Calamares #3030, Quillota', 'a.fernandez@email.cl', '+56981552039'),
(2002, 'Pedro', 'Rodriguez', '9777777-7', 'Los Dragones #999, Villa Alemana', 'p.rodriguez@email.cl', '+56974559423'),
(2003, 'María', 'Cofré', '18569123-1', 'Los Puentes #2121, Quilpue', 'm.cofre@email.cl', '+56966983321'),
(2004, ' Penélope', 'Martinez', '16555444-1', 'Las Cañas #995, Quillota', 'p.martinez@email.cl', '+56942395566'),
(2015, 'Pedro', 'Rodriguez', '9556644-1', 'Los Manzanos #5050, Talca', 'p.rodriguez@email.cl', '+56962664499');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuenta`
--

CREATE TABLE `cuenta` (
  `cod_user` varchar(10) NOT NULL COMMENT 'Nombre de usuario',
  `clave_user` varchar(100) NOT NULL COMMENT 'Contraseña de cuenta de usuario',
  `rol` enum('administrador','administrativo','tecnico','inventario','recepcionista') NOT NULL COMMENT 'Rol de usuario asignado',
  `cod_emp` int(11) DEFAULT NULL COMMENT 'Codigo de empleado asignado a la cuenta'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `cuenta`
--

INSERT INTO `cuenta` (`cod_user`, `clave_user`, `rol`, `cod_emp`) VALUES
('amarchant', '0e949b5f9de9cfa8437d0beeca8d8c96a6b578caa889fd6659e85b7dff22e59b', 'tecnico', 3003),
('dcornejo', '98b400a96cb84215f4ced0b9c9bd7298f44dd36d6fe19b8751bd745eac926369', 'inventario', 3002),
('dgarrido', 'db1963354b34cc7e89e71bfd4fcd5b65d16667b33b82bbe77610f74467a738cd', 'recepcionista', 3001),
('jgallardo', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'administrador', 3000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `cod_emp` int(11) NOT NULL,
  `name_emp` varchar(20) NOT NULL COMMENT 'Nombre del empleado',
  `lastname_emp` varchar(20) NOT NULL COMMENT 'Apellido del empleado',
  `job_title` varchar(20) NOT NULL COMMENT 'Cargo del empleado',
  `rut_emp` varchar(10) NOT NULL COMMENT 'Rut del empleado',
  `hire_date` date NOT NULL COMMENT 'Fecha de ingreso a la empresa',
  `dep_date` date DEFAULT NULL COMMENT 'Fecha de salida de la empresa'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci COMMENT='Todos los Empleados que han sido contratados alguna vez en la empresa.';

--
-- Volcado de datos para la tabla `empleado`
--

INSERT INTO `empleado` (`cod_emp`, `name_emp`, `lastname_emp`, `job_title`, `rut_emp`, `hire_date`, `dep_date`) VALUES
(3000, 'Juan', 'Gallardo', 'Administrador', '11111111-1', '2020-01-01', NULL),
(3001, 'Danilo', 'Garrido', 'Recepcionista', '22222222-2', '2020-02-03', NULL),
(3002, 'Diego', 'Cornejo', 'Inventario', '33333333-3', '2020-03-02', NULL),
(3003, 'Angelo', 'Marchant', 'Técnico', '44444444-4', '2020-03-03', '0000-00-00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura`
--

CREATE TABLE `factura` (
  `cod_fact` int(11) NOT NULL COMMENT 'Código de la facturación',
  `name_customer` varchar(30) DEFAULT NULL COMMENT 'Nombre del cliente asociado a la facturación.',
  `valor_total_neto` int(11) DEFAULT NULL COMMENT 'Valor Total neto de la facturación.',
  `valor_total_iva` int(11) DEFAULT NULL COMMENT 'Valor Total del IVA de la facturación.',
  `valor_total` int(11) DEFAULT NULL COMMENT 'Valor Total de la facturación con IVA.',
  `fecha_fact` datetime DEFAULT NULL COMMENT 'Fecha en que se emitió la facturación.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci COMMENT='Todas las facturaciones.';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `repuesto`
--

CREATE TABLE `repuesto` (
  `cod_rep` varchar(8) NOT NULL COMMENT 'Código de repuesto',
  `name_rep` varchar(30) NOT NULL COMMENT 'Nombre del repuesto.',
  `desc_rep` varchar(100) NOT NULL COMMENT 'Descripción del repuesto.',
  `price_rep` int(11) NOT NULL COMMENT 'Precio del repuesto.',
  `stock` int(11) NOT NULL COMMENT 'Stock del repuesto'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `repuesto`
--

INSERT INTO `repuesto` (`cod_rep`, `name_rep`, `desc_rep`, `price_rep`, `stock`) VALUES
('REP0001', 'W11OEM', 'Sistema Operativo Windows 11 Versión PRO', 15000, 50),
('REP0002', 'WDSSD500GB', 'Unidad de estado sódilo Western Digital de 500GB ', 30000, 15),
('REP0003', 'WDNVME500GB', 'Unidad de estado sólido NVME de 500 GB Western Digital', 40000, 10),
('REP0004', 'BM50GB', 'Placa Madre BM50 Marca Gygabyte', 50000, 5),
('REP0005', 'A320-KASUS', 'Placa Madre Asus Modelo A302-K', 50000, 5),
('REP0006', 'RAMDDR4HYPER', 'Memoria Ram Hyper DDR-4 de 8GB', 30000, 10),
('REP0007', 'SAMSUNGLED15', 'Pantalla de notebook Samsung de 15 pulgadas', 60000, 5),
('REP0008', 'WDSSD1TB', 'Unidad de estado sólido Western Digital de 1 TB', 50000, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicio`
--

CREATE TABLE `servicio` (
  `cod_serv` varchar(8) NOT NULL COMMENT 'Código del servicio.',
  `name_serv` varchar(30) NOT NULL COMMENT 'Nombre del servicio.',
  `desc_serv` varchar(100) NOT NULL COMMENT 'Descripción del servicio.',
  `price_serv` int(11) NOT NULL COMMENT 'Precio del servicio'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci COMMENT='Todos los servicios que ofrece la empresa.';

--
-- Volcado de datos para la tabla `servicio`
--

INSERT INTO `servicio` (`cod_serv`, `name_serv`, `desc_serv`, `price_serv`) VALUES
('SERV0000', 'Diagnóstico', 'Se realizará un diagnóstico al equipo para buscar posibles problemas', 10000),
('SERV0001', 'Formatear', 'Se realizará una restauración de fábrica al Sistema Operativo del equipo', 15000),
('SERV0002', 'Cambio de SO', 'Se realizará un cambio de Sistema Operativo al equipo', 10000),
('SERV0003', 'Respaldo ', 'Se realizará un respaldo total al almacenamiento del equipo', 15000),
('SERV0004', 'Cambio de Unidad ', 'Se realizará un cambio de unidad de almacenamiento del equipo', 15000),
('SERV0005', 'Limpieza y mantención', 'Se realizará una limpieza y mantención completa a los componentes del equipo', 20000),
('SERV0006', 'Cambio de Memoria RAM', 'Se realizará un cambio de memoria ram', 5000),
('SERV0007', 'Cambio de Procesador', 'Se realizará un cambio de procesador del equipo', 10000),
('SERV0008', 'Cambio de Fuente de Poder', 'Se realizará un cambio de la fuente de poder del equipo', 10000),
('SERV0009', 'Cambio de Pantalla', 'Se realizará un cambio de pantalla al equipo', 25000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ticketrepuesto`
--

CREATE TABLE `ticketrepuesto` (
  `cod_ticket` int(11) NOT NULL,
  `state_ticket` enum('abierto','pendiente','cerrado') NOT NULL COMMENT 'Estado del ticket.',
  `cod_customer` int(11) DEFAULT NULL,
  `cod_rep` varchar(8) DEFAULT NULL COMMENT 'Código de repuesto asociado al ticket.',
  `cod_fact` int(11) DEFAULT NULL COMMENT 'Código de facturación asociado al Ticket'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci COMMENT='Todos los Tickets asociados a un repuesto.';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ticketservicio`
--

CREATE TABLE `ticketservicio` (
  `cod_ticket` int(11) NOT NULL COMMENT 'Código del ticket generado.',
  `state_ticket` enum('abierto','pendiente','cerrado') NOT NULL COMMENT 'Estado del ticket',
  `cod_customer` int(11) NOT NULL COMMENT 'Código del cliente asociado al ticket',
  `cod_emp` int(11) NOT NULL COMMENT 'Código del empleado técnico asociado al ticket',
  `cod_serv` varchar(8) DEFAULT NULL COMMENT 'Código de servicio asociado al Ticket.',
  `cod_fact` int(11) DEFAULT NULL COMMENT 'Código del la facturación asociada al ticket'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci COMMENT='Todos los tickets generados por la empresa.';

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`cod_customer`);

--
-- Indices de la tabla `cuenta`
--
ALTER TABLE `cuenta`
  ADD PRIMARY KEY (`cod_user`);

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`cod_emp`);

--
-- Indices de la tabla `factura`
--
ALTER TABLE `factura`
  ADD PRIMARY KEY (`cod_fact`);

--
-- Indices de la tabla `repuesto`
--
ALTER TABLE `repuesto`
  ADD PRIMARY KEY (`cod_rep`);

--
-- Indices de la tabla `servicio`
--
ALTER TABLE `servicio`
  ADD PRIMARY KEY (`cod_serv`);

--
-- Indices de la tabla `ticketrepuesto`
--
ALTER TABLE `ticketrepuesto`
  ADD PRIMARY KEY (`cod_ticket`),
  ADD KEY `ticketrespuesto_cliente_cod_customer_fk` (`cod_customer`),
  ADD KEY `ticketrespuesto_repuesto_cod_rep_fk` (`cod_rep`);

--
-- Indices de la tabla `ticketservicio`
--
ALTER TABLE `ticketservicio`
  ADD PRIMARY KEY (`cod_ticket`),
  ADD KEY `ticketservicio_cliente_cod_customer_fk` (`cod_customer`),
  ADD KEY `ticketservicio_empleado_cod_emp_fk` (`cod_emp`),
  ADD KEY `ticketservicio_servicio_cod_serv_fk` (`cod_serv`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `cod_customer` int(11) NOT NULL AUTO_INCREMENT COMMENT 'El código del cliente', AUTO_INCREMENT=2016;

--
-- AUTO_INCREMENT de la tabla `empleado`
--
ALTER TABLE `empleado`
  MODIFY `cod_emp` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3006;

--
-- AUTO_INCREMENT de la tabla `factura`
--
ALTER TABLE `factura`
  MODIFY `cod_fact` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Código de la facturación', AUTO_INCREMENT=20230018;

--
-- AUTO_INCREMENT de la tabla `ticketrepuesto`
--
ALTER TABLE `ticketrepuesto`
  MODIFY `cod_ticket` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6015;

--
-- AUTO_INCREMENT de la tabla `ticketservicio`
--
ALTER TABLE `ticketservicio`
  MODIFY `cod_ticket` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Código del ticket generado.', AUTO_INCREMENT=5023;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `ticketrepuesto`
--
ALTER TABLE `ticketrepuesto`
  ADD CONSTRAINT `ticketrespuesto_cliente_cod_customer_fk` FOREIGN KEY (`cod_customer`) REFERENCES `cliente` (`cod_customer`),
  ADD CONSTRAINT `ticketrespuesto_repuesto_cod_rep_fk` FOREIGN KEY (`cod_rep`) REFERENCES `repuesto` (`cod_rep`);

--
-- Filtros para la tabla `ticketservicio`
--
ALTER TABLE `ticketservicio`
  ADD CONSTRAINT `ticketservicio_cliente_cod_customer_fk` FOREIGN KEY (`cod_customer`) REFERENCES `cliente` (`cod_customer`),
  ADD CONSTRAINT `ticketservicio_empleado_cod_emp_fk` FOREIGN KEY (`cod_emp`) REFERENCES `empleado` (`cod_emp`),
  ADD CONSTRAINT `ticketservicio_servicio_cod_serv_fk` FOREIGN KEY (`cod_serv`) REFERENCES `servicio` (`cod_serv`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
