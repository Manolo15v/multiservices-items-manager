<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('categories', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('slug')->unique();
            $table->text('description')->nullable();
            $table->timestamps();

            $table->index('slug');
        });

        // Insertar datos de prueba
        DB::table('categories')->insert([
            [
                'name' => 'Electrónica',
                'slug' => 'electronica',
                'description' => 'Dispositivos electrónicos y accesorios tecnológicos',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'name' => 'Ropa y Accesorios',
                'slug' => 'ropa-y-accesorios',
                'description' => 'Prendas de vestir para todas las edades y complementos',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'name' => 'Hogar y Jardín',
                'slug' => 'hogar-y-jardin',
                'description' => 'Artículos para el hogar, decoración y jardinería',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'name' => 'Deportes y Fitness',
                'slug' => 'deportes-y-fitness',
                'description' => 'Equipamiento y accesorios deportivos para entrenamiento',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'name' => 'Libros y Educación',
                'slug' => 'libros-y-educacion',
                'description' => 'Libros, material educativo y recursos de aprendizaje',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'name' => 'Salud y Belleza',
                'slug' => 'salud-y-belleza',
                'description' => 'Productos de cuidado personal, salud y cosmética',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'name' => 'Juguetes y Juegos',
                'slug' => 'juguetes-y-juegos',
                'description' => 'Juguetes infantiles, juegos de mesa y entretenimiento',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'name' => 'Automóvil y Accesorios',
                'slug' => 'automovil-y-accesorios',
                'description' => 'Repuestos, accesorios y herramientas para vehículos',
                'created_at' => now(),
                'updated_at' => now(),
            ],
        ]);
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('categories');
    }
};
