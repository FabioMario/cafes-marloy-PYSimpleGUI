-- Script para la tabla de login
USE cafes_marloy_db;

CREATE TABLE IF NOT EXISTS `login` (
  `correo` VARCHAR(255) PRIMARY KEY,
  `contraseña` VARBINARY(128) NOT NULL, -- Cambiado a VARBINARY para almacenar el hash binario
  `es_administrador` BOOLEAN NOT NULL DEFAULT FALSE
);
