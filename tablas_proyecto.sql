use prueba;
CREATE TABLE Almacen (
   ID INT AUTO_INCREMENT PRIMARY KEY,
   Nombre VARCHAR(255),
   Ubicacion VARCHAR(255)
);
CREATE TABLE EquipoMaquina (
   ID INT AUTO_INCREMENT PRIMARY KEY,
   Nombre VARCHAR(255),
   Descripcion TEXT,
   Categoria VARCHAR(50),
   EspecificacionesTecnicas TEXT,
   Estado BOOLEAN DEFAULT TRUE
);
CREATE TABLE Repuesto (
   ID INT AUTO_INCREMENT PRIMARY KEY,
   Nombre VARCHAR(255),
   Descripcion TEXT,
   Stock INT,
   PrecioSinIVA INT,
   PrecioConIVA INT,
   ID_proveedor Int,
   ID_almacen Int,
   ID_maquina Int,
   FOREIGN KEY (ID_proveedor) REFERENCES Proveedor(ID),
   FOREIGN KEY (ID_almacen) REFERENCES Almacen(ID),
   FOREIGN KEY (ID_maquina) REFERENCES EquipoMaquina(ID)
   );
   CREATE TABLE transacciones (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    repuesto VARCHAR(255),
    fecha DATE,
    cantidad INT,
    ID_proveedor INT,
    ID_almacen INT,
    ID_maquina INT,
    FOREIGN KEY (ID_proveedor) REFERENCES proveedor(ID),
    FOREIGN KEY (ID_almacen) REFERENCES almacen(ID),
    FOREIGN KEY (ID_maquina) REFERENCES equipomaquina(ID)
);