create database test;
use test;


CREATE TABLE IF NOT EXISTS Usuario (
	id INTEGER NOT NULL AUTO_INCREMENT,
	Username VARCHAR(50) NOT NULL,
	Contraseña VARCHAR(255) NOT NULL,
	Rol ENUM('admin', 'supervisor', 'usuario') NOT NULL,
	Estado BOOLEAN NOT NULL,
	id_empleado INTEGER NOT NULL unique,		
	PRIMARY KEY(id),
    foreign key(id_empleado) references Empleado(id)
);


CREATE TABLE IF NOT EXISTS Empleado (
	id INTEGER NOT NULL AUTO_INCREMENT,
	Apellido VARCHAR(50) NOT NULL,
	Nombre VARCHAR(50) NOT NULL,
	Correo VARCHAR(150) NOT NULL,
	Telefono VARCHAR(11) NOT NULL,
	Estado BOOLEAN NOT NULL DEFAULT True,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Eventos(
	id integer not null auto_increment,
    tipo enum('ingreso','egreso','paqueteria','visitas','otros') not null,
    fecha datetime default current_timestamp not null,
    observaciones varchar(500),
    id_empleado integer not null,
    primary key(id),
    foreign key(id_empleado) references empleado(id)
);



select * from empleado;

insert into empleado(apellido,nombre,correo,telefono)
values
('grillo','pepe','pepe@gmail.com','3816328144');

select * from usuario;

insert into usuario(username,contraseña,rol,estado,id_empleado)
values
('pepex','1234','admin',1,1);

select * from Eventos;
insert into Eventos(tipo,observaciones,id_empleado)
values
('paqueteria','Paquete de ML para Diego de la Vega, del 3ro C',2)