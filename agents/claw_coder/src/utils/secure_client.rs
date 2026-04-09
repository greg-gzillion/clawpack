// Secure HTTP client - enforces HTTPS and safe header handling

use reqwest::{Client, ClientBuilder, Error, Response};
use std::time::Duration;
use crate::utils::safe_logger::{log_api_key_present, Sensitive};

/// Create a secure HTTP client with TLS enforced
pub fn create_secure_client(timeout_secs: u64) -> Result<Client, Error> {
    ClientBuilder::new()
        .use_rustls_tls()           // Use Rustls (modern TLS)
        .https_only(true)            // Enforce HTTPS only
        .timeout(Duration::from_secs(timeout_secs))
        .user_agent("claw_coder/1.0")
        .build()
}

/// Create a client with an API key (key is NOT logged)
pub fn create_authenticated_client(
    api_key: &str, 
    timeout_secs: u64
) -> Result<Client, Error> {
    // Safe logging - only logs presence, not the key itself
    log_api_key_present(api_key, "HTTP Client");
    
    let mut headers = reqwest::header::HeaderMap::new();
    let auth_value = format!("Bearer {}", api_key);
    
    headers.insert(
        reqwest::header::AUTHORIZATION,
        reqwest::header::HeaderValue::from_str(&auth_value)
            .expect("Invalid header value")
    );
    
    ClientBuilder::new()
        .use_rustls_tls()
        .https_only(true)
        .timeout(Duration::from_secs(timeout_secs))
        .default_headers(headers)
        .build()
}

/// Safe request logging - never logs headers or body
pub async fn safe_request(client: &Client, url: &str) -> Result<Response, Error> {
    log::debug!("Making secure request to: {}", url);
    client.get(url).send().await
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_create_secure_client() {
        let client = create_secure_client(30);
        assert!(client.is_ok());
    }
}
