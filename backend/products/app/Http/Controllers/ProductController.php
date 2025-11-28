<?php

namespace App\Http\Controllers;

use App\Models\Product;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;
use Illuminate\Validation\Rule;

class ProductController extends Controller
{
    private function formatProductImages($product)
    {
        return $product->images->map(function ($image) {
            return [
                'id' => $image->id,
                'path' => $image->path,
                'url' => url('/storage/' . $image->path),
                'alt' => $image->alt,
                'order' => $image->order,
            ];
        });
    }

    private function formatProductData($product)
    {
        return [
            'id' => $product->id,
            'name' => $product->name,
            'slug' => $product->slug,
            'description' => $product->description,
            'price' => $product->price,
            'formatted_price' => $product->formatted_price,
            'stock' => $product->stock,
            'status' => $product->status,
            'category' => $product->category ? [
                'id' => $product->category->id,
                'name' => $product->category->name,
                'slug' => $product->category->slug,
            ] : null,
            'images' => $this->formatProductImages($product),
            'created_at' => $product->created_at,
            'updated_at' => $product->updated_at,
        ];
    }
    public function index(): JsonResponse
    {
        $products = Product::with(['category', 'images'])
            ->orderBy('name')
            ->get();

        return response()->json([
            'success' => true,
            'data' => $products->map(function ($product) {
                return $this->formatProductData($product);
            }),
            'message' => 'Products retrieved successfully'
        ]);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'description' => 'nullable|string',
            'price' => 'required|numeric|min:0',
            'stock' => 'required|integer|min:0',
            'category_id' => 'nullable|exists:categories,id',
            'status' => ['required', Rule::in(['active', 'inactive'])],
            'images' => 'nullable|array|max:5',
            'images.*' => 'nullable|image|mimes:jpeg,png,jpg,gif,webp|max:2048',
        ]);

        $slug = Str::slug($validated['name']);
        $originalSlug = $slug;
        $counter = 1;

        while (Product::where('slug', $slug)->exists()) {
            $slug = $originalSlug . '-' . $counter;
            $counter++;
        }

        $validated['slug'] = $slug;

        $product = Product::create($validated);

        if ($request->hasFile('images')) {
            $images = $request->file('images');

            foreach ($images as $index => $image) {
                if ($image->isValid()) {
                    try {
                        // Generate unique filename
                        $filename = 'product_' . $product->id . '_' . time() . '_' . $index . '.' . $image->getClientOriginalExtension();

                        // Store file manually
                        $image->move(storage_path('app/public/products'), $filename);
                        $path = 'products/' . $filename;

                        $product->images()->create([
                            'path' => $path,
                            'alt' => $product->name . ' - Image ' . ($index + 1),
                            'order' => $index,
                        ]);
                    } catch (\Exception $e) {
                        // Log error but continue with other images
                        continue;
                    }
                }
            }
        }

        $product->load(['category', 'images']);

        return response()->json([
            'success' => true,
            'data' => $this->formatProductData($product),
            'message' => 'Product created successfully'
        ], 201);
    }

    public function show(Product $product): JsonResponse
    {
        $product->load(['category', 'images']);

        return response()->json([
            'success' => true,
            'data' => $this->formatProductData($product),
            'message' => 'Product retrieved successfully'
        ]);
    }

    public function update(Request $request, Product $product): JsonResponse
    {
        $validated = $request->validate([
            'name' => 'sometimes|required|string|max:255',
            'description' => 'nullable|string',
            'price' => 'sometimes|required|numeric|min:0',
            'stock' => 'sometimes|required|integer|min:0',
            'category_id' => 'nullable|exists:categories,id',
            'status' => ['sometimes', 'required', Rule::in(['active', 'inactive'])],
            'images' => 'nullable|array|max:5',
            'images.*' => 'nullable|image|mimes:jpeg,png,jpg,gif,webp|max:2048',
            'deleted_images' => 'nullable|array',
            'deleted_images.*' => 'integer|exists:images,id',
        ]);

        if (isset($validated['name'])) {
            $slug = Str::slug($validated['name']);
            $originalSlug = $slug;
            $counter = 1;

            while (Product::where('slug', $slug)->where('id', '!=', $product->id)->exists()) {
                $slug = $originalSlug . '-' . $counter;
                $counter++;
            }

            $validated['slug'] = $slug;
        }

        $product->update($validated);

        // Delete specified images
        if (isset($validated['deleted_images'])) {
            foreach ($validated['deleted_images'] as $imageId) {
                $image = $product->images()->find($imageId);
                if ($image) {
                    // Delete file from storage
                    if (Storage::disk('public')->exists($image->path)) {
                        Storage::disk('public')->delete($image->path);
                    }
                    $image->delete();
                }
            }
        }

        // Add new images
        if ($request->hasFile('images')) {
            $currentMaxOrder = $product->images()->max('order') ?? 0;
            $images = $request->file('images');
            foreach ($images as $index => $image) {
                if ($image->isValid()) {
                    try {
                        // Generate unique filename
                        $filename = 'product_' . $product->id . '_' . time() . '_' . ($currentMaxOrder + $index) . '.' . $image->getClientOriginalExtension();

                        // Store file manually
                        $image->move(storage_path('app/public/products'), $filename);
                        $path = 'products/' . $filename;

                        $product->images()->create([
                            'path' => $path,
                            'alt' => $product->name . ' - Image ' . ($currentMaxOrder + $index + 1),
                            'order' => $currentMaxOrder + $index + 1,
                        ]);
                    } catch (\Exception $e) {
                        // Continue with other images if one fails
                        continue;
                    }
                }
            }
        }

        $product->load(['category', 'images']);

        return response()->json([
            'success' => true,
            'data' => $this->formatProductData($product),
            'message' => 'Product updated successfully'
        ]);
    }

    public function destroy(Product $product): JsonResponse
    {
        $product->delete();

        return response()->json([
            'success' => true,
            'data' => [
                'id' => $product->id,
                'name' => $product->name,
                'slug' => $product->slug,
            ],
            'message' => 'Product deleted successfully'
        ]);
    }
}
