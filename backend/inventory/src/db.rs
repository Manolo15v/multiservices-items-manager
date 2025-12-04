use sqlx::{postgres::PgPoolOptions, PgPool, FromRow};

/// Create a PostgreSQL connection pool
pub async fn create_pool(database_url: &str) -> Result<PgPool, sqlx::Error> {
    PgPoolOptions::new()
        .max_connections(10)
        .connect(database_url)
        .await
}

/// Get all inventory items with product information
pub async fn get_all_inventory(pool: &PgPool) -> Result<Vec<crate::models::InventoryWithProduct>, sqlx::Error> {
    let rows = sqlx::query_as::<_, InventoryRow>(
        r#"
        SELECT 
            i.id,
            i.product_id,
            i.quantity,
            i.min_stock_alert,
            p.name as product_name,
            p.slug as product_sku,
            i.created_at,
            i.updated_at
        FROM inventory i
        LEFT JOIN products p ON i.product_id = p.id
        ORDER BY i.id
        "#
    )
    .fetch_all(pool)
    .await?;

    Ok(rows.into_iter().map(|r| r.into()).collect())
}

/// Get inventory for a specific product
pub async fn get_inventory_by_product(
    pool: &PgPool,
    product_id: i32,
) -> Result<Option<crate::models::InventoryWithProduct>, sqlx::Error> {
    let row = sqlx::query_as::<_, InventoryRow>(
        r#"
        SELECT 
            i.id,
            i.product_id,
            i.quantity,
            i.min_stock_alert,
            p.name as product_name,
            p.slug as product_sku,
            i.created_at,
            i.updated_at
        FROM inventory i
        LEFT JOIN products p ON i.product_id = p.id
        WHERE i.product_id = $1
        "#
    )
    .bind(product_id)
    .fetch_optional(pool)
    .await?;

    Ok(row.map(|r| r.into()))
}

/// Increase stock for a product
pub async fn increase_stock(
    pool: &PgPool,
    product_id: i32,
    quantity: i32,
) -> Result<crate::models::Inventory, sqlx::Error> {
    // Update inventory
    let inventory = sqlx::query_as::<_, crate::models::Inventory>(
        r#"
        UPDATE inventory 
        SET quantity = quantity + $2, updated_at = NOW()
        WHERE product_id = $1
        RETURNING id, product_id, quantity, min_stock_alert, created_at, updated_at
        "#
    )
    .bind(product_id)
    .bind(quantity)
    .fetch_one(pool)
    .await?;

    // Record movement
    sqlx::query(
        r#"
        INSERT INTO inventory_movements (product_id, quantity_change, movement_type, reason)
        VALUES ($1, $2, 'increase', 'Stock increased')
        "#
    )
    .bind(product_id)
    .bind(quantity)
    .execute(pool)
    .await?;

    Ok(inventory)
}

/// Decrease stock for a product
pub async fn decrease_stock(
    pool: &PgPool,
    product_id: i32,
    quantity: i32,
) -> Result<crate::models::Inventory, sqlx::Error> {
    // Update inventory
    let inventory = sqlx::query_as::<_, crate::models::Inventory>(
        r#"
        UPDATE inventory 
        SET quantity = quantity - $2, updated_at = NOW()
        WHERE product_id = $1
        RETURNING id, product_id, quantity, min_stock_alert, created_at, updated_at
        "#
    )
    .bind(product_id)
    .bind(quantity)
    .fetch_one(pool)
    .await?;

    // Record movement
    sqlx::query(
        r#"
        INSERT INTO inventory_movements (product_id, quantity_change, movement_type, reason)
        VALUES ($1, $2, 'decrease', 'Stock decreased')
        "#
    )
    .bind(product_id)
    .bind(-quantity)
    .execute(pool)
    .await?;

    Ok(inventory)
}

/// Set absolute stock quantity for a product
pub async fn set_stock(
    pool: &PgPool,
    product_id: i32,
    quantity: i32,
    reason: Option<String>,
) -> Result<crate::models::Inventory, sqlx::Error> {
    // Get current quantity for movement calculation
    let current: i32 = sqlx::query_scalar(
        r#"SELECT quantity FROM inventory WHERE product_id = $1"#
    )
    .bind(product_id)
    .fetch_one(pool)
    .await?;

    let quantity_change = quantity - current;

    // Update inventory
    let inventory = sqlx::query_as::<_, crate::models::Inventory>(
        r#"
        UPDATE inventory 
        SET quantity = $2, updated_at = NOW()
        WHERE product_id = $1
        RETURNING id, product_id, quantity, min_stock_alert, created_at, updated_at
        "#
    )
    .bind(product_id)
    .bind(quantity)
    .fetch_one(pool)
    .await?;

    // Record movement
    let movement_reason = reason.unwrap_or_else(|| format!("Stock set to {}", quantity));
    sqlx::query(
        r#"
        INSERT INTO inventory_movements (product_id, quantity_change, movement_type, reason)
        VALUES ($1, $2, 'set', $3)
        "#
    )
    .bind(product_id)
    .bind(quantity_change)
    .bind(movement_reason)
    .execute(pool)
    .await?;

    Ok(inventory)
}

/// Check if product has sufficient stock
pub async fn check_stock(pool: &PgPool, product_id: i32) -> Result<i32, sqlx::Error> {
    let quantity: i32 = sqlx::query_scalar(
        r#"SELECT quantity FROM inventory WHERE product_id = $1"#
    )
    .bind(product_id)
    .fetch_one(pool)
    .await?;

    Ok(quantity)
}

/// Create inventory entry for a product if it doesn't exist
pub async fn ensure_inventory_exists(
    pool: &PgPool,
    product_id: i32,
) -> Result<(), sqlx::Error> {
    sqlx::query(
        r#"
        INSERT INTO inventory (product_id, quantity, min_stock_alert)
        VALUES ($1, 0, 10)
        ON CONFLICT (product_id) DO NOTHING
        "#
    )
    .bind(product_id)
    .execute(pool)
    .await?;

    Ok(())
}

/// Internal row type for inventory with product join
#[derive(FromRow)]
struct InventoryRow {
    id: i32,
    product_id: i32,
    quantity: i32,
    min_stock_alert: Option<i32>,
    product_name: Option<String>,
    product_sku: Option<String>,
    created_at: Option<chrono::NaiveDateTime>,
    updated_at: Option<chrono::NaiveDateTime>,
}

impl From<InventoryRow> for crate::models::InventoryWithProduct {
    fn from(row: InventoryRow) -> Self {
        Self {
            id: row.id,
            product_id: row.product_id,
            quantity: row.quantity,
            min_stock_alert: row.min_stock_alert,
            product_name: row.product_name,
            product_sku: row.product_sku,
            created_at: row.created_at,
            updated_at: row.updated_at,
        }
    }
}
