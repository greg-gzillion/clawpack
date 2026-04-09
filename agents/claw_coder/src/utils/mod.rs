// Utility modules for claw_coder

pub mod safe_logger;
pub mod secure_client;

// Re-export commonly used items
pub use safe_logger::{Sensitive, log_api_key_present, log_token_safe, mask_key};
pub use secure_client::{create_secure_client, create_authenticated_client, safe_request};
