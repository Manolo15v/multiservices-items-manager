-- =============================================
-- Multi-Service Inventory Manager Database Schema
-- =============================================

-- =============================================
-- AUTH SERVICE TABLES
-- =============================================

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    verification_code VARCHAR(4),
    reset_code VARCHAR(4),
    is_verified BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_usuarios_username ON usuarios(username);
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);

-- =============================================
-- PRODUCTS SERVICE TABLES
-- =============================================

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_categories_slug ON categories(slug);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_products_slug ON products(slug);
CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);

-- Images table (polymorphic)
CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    path VARCHAR(255) NOT NULL,
    alt VARCHAR(255),
    "order" INTEGER DEFAULT 0,
    imageable_id INTEGER NOT NULL,
    imageable_type VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_images_imageable ON images(imageable_type, imageable_id);

-- Laravel cache table
CREATE TABLE IF NOT EXISTS cache (
    key VARCHAR(255) PRIMARY KEY,
    value TEXT NOT NULL,
    expiration INTEGER NOT NULL
);

-- Laravel cache locks table
CREATE TABLE IF NOT EXISTS cache_locks (
    key VARCHAR(255) PRIMARY KEY,
    owner VARCHAR(255) NOT NULL,
    expiration INTEGER NOT NULL
);

-- Laravel personal access tokens (Sanctum)
CREATE TABLE IF NOT EXISTS personal_access_tokens (
    id SERIAL PRIMARY KEY,
    tokenable_type VARCHAR(255) NOT NULL,
    tokenable_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    token VARCHAR(64) UNIQUE NOT NULL,
    abilities TEXT,
    last_used_at TIMESTAMP WITHOUT TIME ZONE,
    expires_at TIMESTAMP WITHOUT TIME ZONE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_personal_access_tokens_tokenable ON personal_access_tokens(tokenable_type, tokenable_id);

-- =============================================
-- INVENTORY SERVICE TABLES
-- =============================================

-- Inventory table (main stock tracking)
CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 0,
    min_stock_alert INTEGER DEFAULT 10,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    UNIQUE(product_id)
);

CREATE INDEX IF NOT EXISTS idx_inventory_product_id ON inventory(product_id);

-- Inventory movements table (audit trail)
CREATE TABLE IF NOT EXISTS inventory_movements (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity_change INTEGER NOT NULL,
    movement_type VARCHAR(20) NOT NULL CHECK (movement_type IN ('increase', 'decrease', 'set', 'adjustment')),
    reason TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_inventory_movements_product_id ON inventory_movements(product_id);
CREATE INDEX IF NOT EXISTS idx_inventory_movements_type ON inventory_movements(movement_type);
CREATE INDEX IF NOT EXISTS idx_inventory_movements_created_at ON inventory_movements(created_at);

-- =============================================
-- SEED DATA
-- =============================================

-- Insert categories
INSERT INTO categories (name, slug, description, created_at, updated_at) VALUES
    ('Electrónica', 'electronica', 'Dispositivos electrónicos y accesorios tecnológicos', NOW(), NOW()),
    ('Ropa y Accesorios', 'ropa-y-accesorios', 'Prendas de vestir para todas las edades y complementos', NOW(), NOW()),
    ('Hogar y Jardín', 'hogar-y-jardin', 'Artículos para el hogar, decoración y jardinería', NOW(), NOW()),
    ('Deportes y Fitness', 'deportes-y-fitness', 'Equipamiento y accesorios deportivos para entrenamiento', NOW(), NOW()),
    ('Libros y Educación', 'libros-y-educacion', 'Libros, material educativo y recursos de aprendizaje', NOW(), NOW()),
    ('Salud y Belleza', 'salud-y-belleza', 'Productos de cuidado personal, salud y cosmética', NOW(), NOW()),
    ('Juguetes y Juegos', 'juguetes-y-juegos', 'Juguetes infantiles, juegos de mesa y entretenimiento', NOW(), NOW()),
    ('Automóvil y Accesorios', 'automovil-y-accesorios', 'Repuestos, accesorios y herramientas para vehículos', NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- Insert sample products
INSERT INTO products (name, slug, description, price, category_id, status, created_at, updated_at) VALUES
    ('Smartphone Galaxy X', 'smartphone-galaxy-x', 'Último modelo de smartphone con cámara de 108MP', 899.99, 1, 'active', NOW(), NOW()),
    ('Laptop ProBook 15', 'laptop-probook-15', 'Laptop profesional con procesador i7 y 16GB RAM', 1299.99, 1, 'active', NOW(), NOW()),
    ('Camiseta Básica Algodón', 'camiseta-basica-algodon', 'Camiseta 100% algodón disponible en varios colores', 19.99, 2, 'active', NOW(), NOW()),
    ('Lámpara LED Escritorio', 'lampara-led-escritorio', 'Lámpara de escritorio con luz ajustable y puerto USB', 45.99, 3, 'active', NOW(), NOW()),
    ('Mancuernas Ajustables', 'mancuernas-ajustables', 'Set de mancuernas ajustables de 5 a 25 kg', 149.99, 4, 'active', NOW(), NOW()),
    ('Programación en Python', 'programacion-en-python', 'Libro completo para aprender Python desde cero', 35.99, 5, 'active', NOW(), NOW()),
    ('Kit Cuidado Facial', 'kit-cuidado-facial', 'Kit completo de cuidado facial con 5 productos', 79.99, 6, 'active', NOW(), NOW()),
    ('Puzzle 1000 Piezas', 'puzzle-1000-piezas', 'Puzzle de paisaje con 1000 piezas', 24.99, 7, 'active', NOW(), NOW()),
    ('Soporte Celular Auto', 'soporte-celular-auto', 'Soporte magnético para celular en el auto', 15.99, 8, 'active', NOW(), NOW()),
    ('Audífonos Bluetooth', 'audifonos-bluetooth', 'Audífonos inalámbricos con cancelación de ruido', 199.99, 1, 'active', NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- Insert inventory for each product
INSERT INTO inventory (product_id, quantity, min_stock_alert, created_at, updated_at)
SELECT id, 
    CASE 
        WHEN id % 3 = 0 THEN 5   -- Low stock
        WHEN id % 3 = 1 THEN 50  -- Good stock
        ELSE 25                   -- Medium stock
    END,
    10,
    NOW(),
    NOW()
FROM products
ON CONFLICT (product_id) DO NOTHING;

-- Insert initial inventory movements
INSERT INTO inventory_movements (product_id, quantity_change, movement_type, reason, created_at)
SELECT id,
    CASE 
        WHEN id % 3 = 0 THEN 5
        WHEN id % 3 = 1 THEN 50
        ELSE 25
    END,
    'set',
    'Initial stock setup',
    NOW()
FROM products;

