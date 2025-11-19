create database Porteria;
use Porteria;

CREATE TABLE IF NOT EXISTS Empleado (
	id INTEGER NOT NULL AUTO_INCREMENT,
	Apellido VARCHAR(50) NOT NULL,
	Nombre VARCHAR(50) NOT NULL,
	Correo VARCHAR(150) NOT NULL,
	Telefono VARCHAR(15) NOT NULL,
	Estado BOOLEAN NOT NULL DEFAULT True,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Usuario (
	id INTEGER NOT NULL AUTO_INCREMENT,
	NombreUsuario VARCHAR(50) NOT NULL UNIQUE,
	Contraseña VARCHAR(255) NOT NULL,
	Rol ENUM('admin', 'supervisor', 'usuario', 'propietario') NOT NULL,
	Estado BOOLEAN NOT NULL,
	id_empleado INTEGER NOT NULL unique,		
	PRIMARY KEY(id),
    foreign key(id_empleado) references Empleado(id)
);

CREATE TABLE IF NOT EXISTS Eventos(
	id integer not null auto_increment,
    tipo enum('ingreso','egreso','paqueteria','visitas','otros') not null,
    fecha datetime default current_timestamp not null,
    observaciones varchar(500),
    imagen varchar(255),
    id_usuario integer not null,
    primary key(id),
    foreign key(id_usuario) references Usuario(id),
    INDEX(fecha)
);

#ALTER TABLE Eventos ADD column imagen varchar(255) default null;

# TABLE Usuario MODIFY Rol ENUM('admin', 'supervisor', 'usuario', 'propietario') NOT NULL;

SHOW COLUMNS FROM Usuario LIKE 'Rol';

select * from empleado;

insert into empleado(apellido,nombre,correo,telefono)
values
('grillo','pepe','pepe@gmail.com','3816328144');

select * from usuario;

update usuario set Contraseña = '$2a$12$15JXJaBcPt./ycSvSKbQ.eg7tFZ4yUmMKr8Obc9QZOnLFmqK0XG26' WHERE id = 1;

insert into usuario(nombreusuario,contraseña,rol,estado,id_empleado)
values
('1234','$2a$12$15JXJaBcPt./ycSvSKbQ.eg7tFZ4yUmMKr8Obc9QZOnLFmqK0XG26','admin',1,1);

select * from Eventos; 
insert into Eventos(tipo,observaciones,id_usuario)
values
('paqueteria','Paquete de ML para Diego de la Vega, del 3ro C',1)

