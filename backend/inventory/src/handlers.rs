use actix_web::{web, HttpResponse, Responder};
use sqlx::PgPool;

use crate::db;
use crate::models::{ApiResponse, QuantityRequest, SetStockRequest};

/// Configure all routes for the inventory service
pub fn configure_routes(cfg: &mut web::ServiceConfig) {
    cfg.service(
        web::scope("/inventory")
            .route("", web::get().to(get_all_inventory))
            .route("/{product_id}", web::get().to(get_inventory_by_product))
            .route("/{product_id}", web::put().to(set_stock))
            .route("/{product_id}/increase", web::post().to(increase_stock))
            .route("/{product_id}/decrease", web::post().to(decrease_stock)),
    )
    .route("/health", web::get().to(health_check));
}

/// Health check endpoint
async fn health_check() -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({
        "status": "healthy",
        "service": "inventory"
    }))
}

/// GET /inventory - Get all inventory items
async fn get_all_inventory(pool: web::Data<PgPool>) -> impl Responder {
    match db::get_all_inventory(pool.get_ref()).await {
        Ok(inventory) => HttpResponse::Ok().json(ApiResponse::success(inventory)),
        Err(e) => {
            log::error!("Failed to get inventory: {}", e);
            HttpResponse::InternalServerError()
                .json(ApiResponse::<()>::error("Failed to retrieve inventory"))
        }
    }
}

/// GET /inventory/{product_id} - Get inventory for a specific product
async fn get_inventory_by_product(
    pool: web::Data<PgPool>,
    path: web::Path<i32>,
) -> impl Responder {
    let product_id = path.into_inner();

    match db::get_inventory_by_product(pool.get_ref(), product_id).await {
        Ok(Some(inventory)) => HttpResponse::Ok().json(ApiResponse::success(inventory)),
        Ok(None) => {
            HttpResponse::NotFound().json(ApiResponse::<()>::error("Inventory not found for product"))
        }
        Err(e) => {
            log::error!("Failed to get inventory for product {}: {}", product_id, e);
            HttpResponse::InternalServerError()
                .json(ApiResponse::<()>::error("Failed to retrieve inventory"))
        }
    }
}

/// POST /inventory/{product_id}/increase - Increase stock for a product
async fn increase_stock(
    pool: web::Data<PgPool>,
    path: web::Path<i32>,
    body: web::Json<QuantityRequest>,
) -> impl Responder {
    let product_id = path.into_inner();
    let quantity = body.quantity;

    if quantity <= 0 {
        return HttpResponse::BadRequest()
            .json(ApiResponse::<()>::error("Quantity must be greater than 0"));
    }

    // Ensure inventory exists
    if let Err(e) = db::ensure_inventory_exists(pool.get_ref(), product_id).await {
        log::error!("Failed to ensure inventory exists: {}", e);
        return HttpResponse::InternalServerError()
            .json(ApiResponse::<()>::error("Failed to process request"));
    }

    match db::increase_stock(pool.get_ref(), product_id, quantity).await {
        Ok(inventory) => {
            log::info!("Increased stock for product {}: +{}", product_id, quantity);
            HttpResponse::Ok().json(ApiResponse::success_with_message(
                inventory,
                &format!("Stock increased by {}", quantity),
            ))
        }
        Err(e) => {
            log::error!("Failed to increase stock for product {}: {}", product_id, e);
            HttpResponse::InternalServerError()
                .json(ApiResponse::<()>::error("Failed to increase stock"))
        }
    }
}

/// POST /inventory/{product_id}/decrease - Decrease stock for a product
async fn decrease_stock(
    pool: web::Data<PgPool>,
    path: web::Path<i32>,
    body: web::Json<QuantityRequest>,
) -> impl Responder {
    let product_id = path.into_inner();
    let quantity = body.quantity;

    if quantity <= 0 {
        return HttpResponse::BadRequest()
            .json(ApiResponse::<()>::error("Quantity must be greater than 0"));
    }

    // Check current stock
    match db::check_stock(pool.get_ref(), product_id).await {
        Ok(current_stock) => {
            if current_stock < quantity {
                return HttpResponse::BadRequest().json(ApiResponse::<()>::error(&format!(
                    "Insufficient stock. Available: {}, Requested: {}",
                    current_stock, quantity
                )));
            }
        }
        Err(e) => {
            log::error!("Failed to check stock for product {}: {}", product_id, e);
            return HttpResponse::NotFound()
                .json(ApiResponse::<()>::error("Product not found in inventory"));
        }
    }

    match db::decrease_stock(pool.get_ref(), product_id, quantity).await {
        Ok(inventory) => {
            log::info!("Decreased stock for product {}: -{}", product_id, quantity);
            HttpResponse::Ok().json(ApiResponse::success_with_message(
                inventory,
                &format!("Stock decreased by {}", quantity),
            ))
        }
        Err(e) => {
            log::error!("Failed to decrease stock for product {}: {}", product_id, e);
            HttpResponse::InternalServerError()
                .json(ApiResponse::<()>::error("Failed to decrease stock"))
        }
    }
}

/// PUT /inventory/{product_id} - Set absolute stock quantity
async fn set_stock(
    pool: web::Data<PgPool>,
    path: web::Path<i32>,
    body: web::Json<SetStockRequest>,
) -> impl Responder {
    let product_id = path.into_inner();
    let quantity = body.quantity;
    let reason = body.reason.clone();

    if quantity < 0 {
        return HttpResponse::BadRequest()
            .json(ApiResponse::<()>::error("Quantity cannot be negative"));
    }

    // Ensure inventory exists
    if let Err(e) = db::ensure_inventory_exists(pool.get_ref(), product_id).await {
        log::error!("Failed to ensure inventory exists: {}", e);
        return HttpResponse::InternalServerError()
            .json(ApiResponse::<()>::error("Failed to process request"));
    }

    match db::set_stock(pool.get_ref(), product_id, quantity, reason).await {
        Ok(inventory) => {
            log::info!("Set stock for product {} to {}", product_id, quantity);
            HttpResponse::Ok().json(ApiResponse::success_with_message(
                inventory,
                &format!("Stock set to {}", quantity),
            ))
        }
        Err(e) => {
            log::error!("Failed to set stock for product {}: {}", product_id, e);
            HttpResponse::InternalServerError()
                .json(ApiResponse::<()>::error("Failed to set stock"))
        }
    }
}

