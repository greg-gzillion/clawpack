// Safe logging utility - prevents sensitive data exposure
// Use this instead of directly logging API keys, tokens, etc.

use std::fmt;

/// Wrapper for sensitive data that redacts when logged
#[derive(Clone, Copy)]
pub struct Sensitive<T>(pub T);

impl<T> Sensitive<T> {
    pub fn new(value: T) -> Self {
        Sensitive(value)
    }
    
    pub fn into_inner(self) -> T {
        self.0
    }
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

/// Log API key presence safely
pub fn log_api_key_present(key: &str, service: &str) {
    let is_present = !key.is_empty();
    let length = key.len();
    log::debug!("{} API key present: {}, length: {}", service, is_present, length);
}

/// Log token safely (only shows first/last 4 chars)
pub fn log_token_safe(token: &str, name: &str) {
    if token.len() >= 8 {
        let first_four = &token[..4];
        let last_four = &token[token.len()-4..];
        log::debug!("{} token: {}...{}", name, first_four, last_four);
    } else {
        log::debug!("{} token: [REDACTED]", name);
    }
}

/// Mask an API key for logging (shows only last 4 chars)
pub fn mask_key(key: &str) -> String {
    if key.len() <= 4 {
        return "[REDACTED]".to_string();
    }
    format!("****{}", &key[key.len()-4..])
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sensitive_redaction() {
        let api_key = "sk-1234567890abcdef";
        let sensitive = Sensitive::new(api_key);
        assert_eq!(format!("{:?}", sensitive), "[REDACTED]");
        assert_eq!(format!("{}", sensitive), "[REDACTED]");
        assert_eq!(sensitive.into_inner(), api_key);
    }

    #[test]
    fn test_mask_key() {
        assert_eq!(mask_key("sk-1234567890abcdef"), "****cdef");
        assert_eq!(mask_key("short"), "[REDACTED]");
    }
}
