USE cafes_marloy_db;

-- Proveedores
INSERT INTO proveedores (nombre, contacto) VALUES
('Café de la Montaña S.A.', 'juan.perez@cafedelamontana.com'),
('Distribuidora El Grano Dorado', 'info@granodorado.net'),
('Insumos Lácteos del Sur', 'ventas@lacteosdelsur.uy'),
('Azucarera Oriental', 'contacto@azucareraoriental.com'),
('Repuestos y Servicios Express', 'servicio@repuestosysexpress.com'),
('Importaciones de Café Colombiano', 'pedidos@cafeimportcol.com');

-- Insumos
INSERT INTO insumos (descripcion, tipo, precio_unitario, id_proveedor) VALUES
('Café en grano Arábica 1kg', 'Café', 25.50, 1),
('Café en grano Robusta 1kg', 'Café', 22.00, 2),
('Leche en polvo descremada 500g', 'Lácteo', 8.75, 3),
('Azúcar blanca refinada 1kg', 'Endulzante', 2.50, 4),
('Filtro de papel para cafetera', 'Repuesto', 15.00, 5),
('Café molido descafeinado 500g', 'Café', 18.90, 6);

-- Clientes
INSERT INTO clientes (nombre, direccion, telefono, correo) VALUES
('Oficina Legal & Asociados', 'Av. Principal 123, Piso 2', '099123456', 'compras@legalasociados.com'),
('Clínica Bienestar', 'Calle Secundaria 456', '24005060', 'admin@clinicabienestar.uy'),
('Universidad del Saber', 'Bulevar Universitario 789', '26001234', 'rectorado@universidadsaber.edu'),
('Estudio Contable Moderno', 'Plaza Independencia 1', '098765432', 'contacto@contablemoderno.com'),
('Hotel Gran Vista', 'Rambla Sur 1010', '29018090', 'gerencia@granvistahotel.com'),
('Centro de Coworking Innova', 'Calle Ficticia 2020', '091234567', 'hola@innova.work');

-- Maquinas
INSERT INTO maquinas (modelo, id_cliente, ubicacion_cliente, costo_alquiler_mensual) VALUES
('Espresso Pro X1', 1, 'Recepción Piso 2', 150.00),
('Latte Master 5000', 2, 'Sala de espera', 175.50),
('Office Coffee Plus', 3, 'Cafetería Central', 120.00),
('Compact Brew Mini', 4, 'Oficina Principal', 95.00),
('Vending Coffee Max', 5, 'Lobby Principal', 250.00),
('Single Cup Brewer', 6, 'Área Común', 80.00);

-- Tecnicos
INSERT INTO tecnicos (ci, nombre, apellido, telefono) VALUES
('4.123.456-7', 'Carlos', 'Rodríguez', '099887766'),
('5.987.654-3', 'Ana', 'García', '098112233'),
('3.876.543-2', 'Luis', 'Martínez', '097554433'),
('4.567.890-1', 'María', 'Fernández', '096998877'),
('2.345.678-9', 'Pedro', 'López', '095123123'),
('4.789.012-3', 'Lucía', 'Gómez', '094567567');

-- Registros de Consumo
INSERT INTO registro_consumo (id_maquina, id_insumo, fecha, cantidad_usada) VALUES
(1, 1, '2025-06-05', 5), -- Máquina 1 usó Café Arábica
(2, 3, '2025-06-05', 2), -- Máquina 2 usó Leche en polvo
(3, 2, '2025-06-06', 8), -- Máquina 3 usó Café Robusta
(4, 4, '2025-06-07', 10),-- Máquina 4 usó Azúcar
(5, 1, '2025-06-08', 15),-- Máquina 5 usó Café Arábica
(6, 6, '2025-06-09', 3); -- Máquina 6 usó Café descafeinado

-- Mantenimientos
INSERT INTO mantenimientos (id_maquina, ci_tecnico, tipo, fecha, observaciones) VALUES
(1, '4.123.456-7', 'Preventivo', '2025-07-01 09:00:00', 'Limpieza general y calibración de molinillo.'),
(2, '5.987.654-3', 'Correctivo', '2025-07-02 11:30:00', 'Reemplazo de la bomba de agua. Estaba defectuosa.'),
(3, '3.876.543-2', 'Preventivo', '2025-07-02 15:00:00', 'Descalcificación y revisión de mangueras.'),
(4, '4.567.890-1', 'Instalación', '2025-05-20 10:00:00', 'Instalación y configuración inicial de la máquina.'),
(5, '2.345.678-9', 'Correctivo', '2025-06-15 14:00:00', 'El monedero no aceptaba monedas de $10. Se ajustó el sensor.'),
(6, '4.789.012-3', 'Preventivo', '2025-07-03 08:30:00', 'Revisión periódica. Todo en orden.');