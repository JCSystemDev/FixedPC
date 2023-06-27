create database fixedpc;

create table cliente
(
    cod_customer      int auto_increment comment 'El código del cliente'
        primary key,
    name_customer     varchar(20) not null comment 'Nombre del cliente',
    lastname_customer varchar(20) not null comment 'Apellido del cliente',
    rut_customer      varchar(10) not null comment 'Rut del cliente',
    address_customer  varchar(40) null comment 'Dirección del cliente',
    email_customer    varchar(25) null comment 'Correo electrónico del cliente',
    phone_customer    varchar(8)  null comment 'Teléfono del cliente'
)
    comment 'Todos los clientes que ha tenido la empresa.';

create table cuenta
(
    cod_user   varchar(10) not null comment 'Nombre de usuario'
        primary key,
    clave_user varchar(20) not null comment 'Contraseña de cuenta de usuario',
    rol        varchar(20) not null comment 'Rol de usuario asignado',
    cod_emp    int         null comment 'Codigo de empleado asignado a la cuenta'
);

create table empleado
(
    cod_emp      int auto_increment
        primary key,
    name_emp     varchar(20) not null comment 'Nombre del empleado',
    lastname_emp varchar(20) not null comment 'Apellido del empleado',
    job_title    varchar(20) not null comment 'Cargo del empleado',
    rut_emp      varchar(10) not null comment 'Rut del empleado',
    hire_date    date        not null comment 'Fecha de ingreso a la empresa',
    dep_date     date        null comment 'Fecha de salida de la empresa'
)
    comment 'Todos los Empleados que han sido contratados alguna vez en la empresa.';

create table repuesto
(
    cod_rep   varchar(8)   not null comment 'Código de repuesto'
        primary key,
    name_rep  varchar(30)  not null comment 'Nombre del repuesto.',
    desc_rep  varchar(100) not null comment 'Descripción del repuesto.',
    price_rep int          not null comment 'Precio del repuesto.',
    stock     int          not null comment 'Stock del repuesto'
);

create table servicio
(
    cod_serv   varchar(8)   not null comment 'Código del servicio.'
        primary key,
    name_serv  varchar(30)  not null comment 'Nombre del servicio.',
    desc_serv  varchar(100) not null comment 'Descripción del servicio.',
    price_serv int          not null comment 'Precio del servicio'
)
    comment 'Todos los servicios que ofrece la empresa.';

create table ticket
(
    cod_ticket   int auto_increment comment 'Código del ticket generado.'
        primary key,
    state_ticket varchar(10) null comment 'Estado del ticket',
    cod_customer int         not null comment 'Código del cliente asociado al ticket',
    cod_emp      int         not null comment 'Código del empleado técnico asociado al ticket',
    cod_fact     int         not null comment 'Código del la facturación asociada al ticket',
    constraint ticket_cliente_cod_customer_fk
        foreign key (cod_customer) references cliente (cod_customer),
    constraint ticket_empleado_cod_emp_fk
        foreign key (cod_emp) references empleado (cod_emp)
)
    comment 'Todos los tickets generados por la empresa.';

create index cod_doc_fk
    on ticket (cod_fact);