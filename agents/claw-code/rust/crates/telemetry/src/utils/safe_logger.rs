// Safe logging utility - prevents sensitive data exposure

use std::fmt;

/// Wrapper for sensitive data that redacts when logged
pub struct Sensitive<T>(pub T);

impl<T> Sensitive<T> {
    pub fn new(value: T) -> Self { Sensitive(value) }
    pub fn into_inner(self) -> T { self.0 }
}

impl<T> fmt::Debug for Sensitive<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[REDACTED]")
    }
}

impl<T> fmt::Display for Sensitive<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[REDACTED]")
    }
}

/// Log API key presence safely (never logs the key itself)
pub fn log_api_key_present(key: &str, service: &str) {
    log::debug!("{} API key present: {}", service, !key.is_empty());
}

/// Mask an API key for logging (shows only last 4 chars)
pub fn mask_key(key: &str) -> String {
    if key.len() <= 4 { return "[REDACTED]".to_string(); }
    format!("****{}", &key[key.len()-4..])
}
