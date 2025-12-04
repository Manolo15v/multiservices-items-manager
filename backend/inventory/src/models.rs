use chrono::NaiveDateTime;
use serde::{Deserialize, Serialize};
use sqlx::FromRow;

/// Inventory record representing stock for a product
#[derive(Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct Inventory {
    pub id: i32,
    pub product_id: i32,
    pub quantity: i32,
    pub min_stock_alert: Option<i32>,
    pub created_at: Option<NaiveDateTime>,
    pub updated_at: Option<NaiveDateTime>,
}

/// Inventory with product details for API responses
#[derive(Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct InventoryWithProduct {
    pub id: i32,
    pub product_id: i32,
    pub quantity: i32,
    pub min_stock_alert: Option<i32>,
    pub product_name: Option<String>,
    pub product_sku: Option<String>,
    pub created_at: Option<NaiveDateTime>,
    pub updated_at: Option<NaiveDateTime>,
}

/// Inventory movement record for audit trail
#[derive(Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct InventoryMovement {
    pub id: i32,
    pub product_id: i32,
    pub quantity_change: i32,
    pub movement_type: String,
    pub reason: Option<String>,
    pub created_at: Option<NaiveDateTime>,
}

/// Request payload for stock quantity changes
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuantityRequest {
    pub quantity: i32,
}

/// Request payload for setting stock with optional reason
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SetStockRequest {
    pub quantity: i32,
    pub reason: Option<String>,
}

/// Generic API response wrapper
#[derive(Debug, Serialize)]
pub struct ApiResponse<T> {
    pub success: bool,
    pub data: Option<T>,
    pub message: Option<String>,
}

impl<T> ApiResponse<T> {
    pub fn success(data: T) -> Self {
        Self {
            success: true,
            data: Some(data),
            message: None,
        }
    }

    pub fn success_with_message(data: T, message: &str) -> Self {
        Self {
            success: true,
            data: Some(data),
            message: Some(message.to_string()),
        }
    }
}

impl ApiResponse<()> {
    pub fn error(message: &str) -> Self {
        Self {
            success: false,
            data: None,
            message: Some(message.to_string()),
        }
    }
}

