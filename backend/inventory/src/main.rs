mod db;
mod handlers;
mod models;

use actix_cors::Cors;
use actix_web::{middleware::Logger, web, App, HttpServer};
use db::create_pool;
use std::env;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Load environment variables
    dotenvy::dotenv().ok();
    
    // Initialize logger
    env_logger::init_from_env(env_logger::Env::new().default_filter_or("info"));
    
    // Get configuration from environment
    let host = env::var("HOST").unwrap_or_else(|_| "0.0.0.0".to_string());
    let port = env::var("PORT")
        .unwrap_or_else(|_| "8003".to_string())
        .parse::<u16>()
        .expect("PORT must be a valid number");
    
    let database_url = env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set");
    
    log::info!("Starting inventory service on {}:{}", host, port);
    
    // Create database connection pool
    let pool = create_pool(&database_url)
        .await
        .expect("Failed to create database pool");
    
    log::info!("Database connection established");
    
    // Start HTTP server
    HttpServer::new(move || {
        // Configure CORS
        let cors = Cors::default()
            .allow_any_origin()
            .allow_any_method()
            .allow_any_header()
            .supports_credentials()
            .max_age(3600);
        
        App::new()
            .app_data(web::Data::new(pool.clone()))
            .wrap(cors)
            .wrap(Logger::default())
            .configure(handlers::configure_routes)
    })
    .bind((host.as_str(), port))?
    .run()
    .await
}

