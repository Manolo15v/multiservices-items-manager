<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\Product;
use Illuminate\Support\Str;

class ProductSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $products = [
            [
                'name' => 'Laptop Gaming Pro',
                'slug' => 'laptop-gaming-pro',
                'description' => 'Laptop de alto rendimiento con RTX 4060, Intel i7, 16GB RAM, 512GB SSD. Ideal para gaming y trabajo pesado.',
                'price' => 1299.99,
                'stock' => 15,
                'category_id' => 1,
                'status' => 'active'
            ],
            [
                'name' => 'Smartphone Galaxy S24',
                'slug' => 'smartphone-galaxy-s24',
                'description' => 'Teléfono flagship con cámara de 108MP, pantalla AMOLED 6.2", 256GB storage, 5G.',
                'price' => 899.99,
                'stock' => 25,
                'category_id' => 1,
                'status' => 'active'
            ],
            [
                'name' => 'Auriculares Bluetooth Pro',
                'slug' => 'auriculares-bluetooth-pro',
                'description' => 'Auriculares inalámbricos con cancelación de ruido, 30 horas de batería, audio HD.',
                'price' => 199.99,
                'stock' => 50,
                'category_id' => 1,
                'status' => 'active'
            ],
            [
                'name' => 'Camiseta Algodón Orgánico',
                'slug' => 'camiseta-algodon-organico',
                'description' => 'Camiseta de algodón orgánico premium, disponible en varios colores, corte moderno.',
                'price' => 29.99,
                'stock' => 100,
                'category_id' => 2,
                'status' => 'active'
            ],
            [
                'name' => 'Jeans Slim Fit',
                'slug' => 'jeans-slim-fit',
                'description' => 'Pantalones jeans de corte slim, tela elástica confortable, varios talles.',
                'price' => 79.99,
                'stock' => 60,
                'category_id' => 2,
                'status' => 'active'
            ],
            [
                'name' => 'Set de Sartenes Antiadherentes',
                'slug' => 'set-sartenes-antiadherentes',
                'description' => 'Set de 3 sartenes antiadherentes con recubrimiento cerámico, mango ergonómico.',
                'price' => 89.99,
                'stock' => 30,
                'category_id' => 3,
                'status' => 'active'
            ],
            [
                'name' => 'Lámpara LED Inteligente',
                'slug' => 'lampara-led-inteligente',
                'description' => 'Lámpara con control por app, millones de colores, programación horaria, 10W.',
                'price' => 45.99,
                'stock' => 40,
                'category_id' => 3,
                'status' => 'active'
            ],
            [
                'name' => 'Balón de Fútbol Profesional',
                'slug' => 'balon-futbol-profesional',
                'description' => 'Balón oficial FIFA tamaño 5, cuero sintético, cámara butílica.',
                'price' => 39.99,
                'stock' => 35,
                'category_id' => 4,
                'status' => 'active'
            ],
            [
                'name' => 'Botella de Agua Térmica',
                'slug' => 'botella-agua-termica',
                'description' => 'Botella de acero inoxidable 500ml, mantiene temperatura 12 horas, libre de BPA.',
                'price' => 24.99,
                'stock' => 80,
                'category_id' => 4,
                'status' => 'active'
            ],
            [
                'name' => 'Best Seller Programming',
                'slug' => 'best-seller-programming',
                'description' => 'Libro sobre patrones de diseño y arquitectura de software, 450 páginas, edición actualizada.',
                'price' => 49.99,
                'stock' => 25,
                'category_id' => 5,
                'status' => 'active'
            ],
            [
                'name' => 'Tablet Android Pro',
                'slug' => 'tablet-android-pro',
                'description' => 'Tablet 10.1" con 4G, 128GB storage, stylus incluido, batería 8000mAh.',
                'price' => 399.99,
                'stock' => 20,
                'category_id' => 1,
                'status' => 'active'
            ],
            [
                'name' => 'Chaqueta Impermeable',
                'slug' => 'chaqueta-impermeable',
                'description' => 'Chaqueta impermeable con capucha, tejido respirable,Available en negro y azul.',
                'price' => 99.99,
                'stock' => 45,
                'category_id' => 2,
                'status' => 'active'
            ],
        ];

        foreach ($products as $product) {
            Product::create($product);
        }
    }
}
