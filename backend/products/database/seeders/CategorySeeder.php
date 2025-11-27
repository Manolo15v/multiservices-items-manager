<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\Category;

class CategorySeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $categories = [
            [
                'name' => 'Electrónicos',
                'slug' => 'electronicos',
                'description' => 'Dispositivos electrónicos y accesorios tecnológicos'
            ],
            [
                'name' => 'Ropa',
                'slug' => 'ropa',
                'description' => 'Prendas de vestir para todas las edades'
            ],
            [
                'name' => 'Hogar',
                'slug' => 'hogar',
                'description' => 'Artículos para el hogar y decoración'
            ],
            [
                'name' => 'Deportes',
                'slug' => 'deportes',
                'description' => 'Equipamiento y accesorios deportivos'
            ],
            [
                'name' => 'Libros',
                'slug' => 'libros',
                'description' => 'Libros de diversos géneros y autores'
            ],
        ];

        foreach ($categories as $category) {
            Category::create($category);
        }
    }
}
