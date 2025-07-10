USE cafes_marloy_db;

-- Login
CREATE TABLE IF NOT EXISTS login (
  correo VARCHAR(255) PRIMARY KEY,
  contraseña VARBINARY(128) NOT NULL,
  es_administrador BOOLEAN NOT NULL DEFAULT FALSE
);

-- Proveedores
CREATE TABLE IF NOT EXISTS proveedores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL UNIQUE,
  contacto VARCHAR(255)
);

-- Insumos
CREATE TABLE IF NOT EXISTS insumos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  descripcion VARCHAR(255) NOT NULL,
  tipo VARCHAR(100),
  precio_unitario DECIMAL(10, 2) NOT NULL,
  id_proveedor INT,
  FOREIGN KEY (id_proveedor) REFERENCES proveedores(id) ON DELETE SET NULL
);

-- Clientes
CREATE TABLE IF NOT EXISTS clientes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  direccion VARCHAR(255),
  telefono VARCHAR(50),
  correo VARCHAR(255) UNIQUE
);

-- Maquinas
CREATE TABLE IF NOT EXISTS maquinas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  modelo VARCHAR(255) NOT NULL,
  id_cliente INT,
  ubicacion_cliente VARCHAR(255),
  costo_alquiler_mensual DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (id_cliente) REFERENCES clientes(id) ON DELETE SET NULL,
  CONSTRAINT unico_cliente_ubicacion UNIQUE (id_cliente, ubicacion_cliente) -- 4a. Respetar las restricciones: Una máquina sólo puede estar asignada a un cliente y una ubicación a la vez.
);

-- Registro de Consumo
CREATE TABLE IF NOT EXISTS registro_consumo (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_maquina INT NOT NULL,
  id_insumo INT NOT NULL,
  fecha DATE NOT NULL,
  cantidad_usada INT NOT NULL,
  FOREIGN KEY (id_maquina) REFERENCES maquinas(id) ON DELETE CASCADE,
  FOREIGN KEY (id_insumo) REFERENCES insumos(id) ON DELETE CASCADE
);

-- Tecnicos
CREATE TABLE IF NOT EXISTS tecnicos (
  ci VARCHAR(20) PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  telefono VARCHAR(50)
);

-- Mantenimientos
CREATE TABLE IF NOT EXISTS mantenimientos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_maquina INT NOT NULL,
  ci_tecnico VARCHAR(20) NOT NULL,
  tipo VARCHAR(100),
  fecha DATETIME NOT NULL,
  observaciones TEXT,
  FOREIGN KEY (id_maquina) REFERENCES maquinas(id) ON DELETE CASCADE,
  FOREIGN KEY (ci_tecnico) REFERENCES tecnicos(ci) ON DELETE CASCADE,
  CONSTRAINT unico_tecnico_fecha UNIQUE (ci_tecnico, fecha) -- 4c. Respetar las restricciones: Un técnico puede realizar varios mantenimientos, pero no debe estarasignado a dos mantenimientos simultáneos (en el mismo día y hora, si seregistra).
);
