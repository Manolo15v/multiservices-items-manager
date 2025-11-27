<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Category>
 */
class CategoryFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        $name = $this->faker->unique()->words(2, true);
        $slug = \Illuminate\Support\Str::slug($name);

        return [
            'name' => ucfirst($name),
            'slug' => $slug,
            'description' => $this->faker->sentence(10),
        ];
    }
}
