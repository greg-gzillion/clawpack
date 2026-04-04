use pyo3::prelude::*;
use rayon::prelude::*;
use walkdir::WalkDir;
use regex::Regex;
use std::fs;
use std::path::Path;
use std::collections::HashMap;

// Simple structs without complex serialization first
#[pyclass]
#[derive(Clone)]
pub struct Bug {
    #[pyo3(get, set)]
    pub file: String,
    #[pyo3(get, set)]
    pub line: u32,
    #[pyo3(get, set)]
    pub column: u32,
    #[pyo3(get, set)]
    pub message: String,
    #[pyo3(get, set)]
    pub severity: String,
    #[pyo3(get, set)]
    pub suggestion: String,
}

#[pymethods]
impl Bug {
    #[new]
    fn new(file: String, line: u32, column: u32, message: String, severity: String, suggestion: String) -> Self {
        Bug { file, line, column, message, severity, suggestion }
    }
    
    fn __repr__(&self) -> String {
        format!("Bug(file={}, line={}, {})", self.file, self.line, self.message)
    }
}

#[pyclass]
#[derive(Clone)]
pub struct SearchMatch {
    #[pyo3(get, set)]
    pub file: String,
    #[pyo3(get, set)]
    pub line: u32,
    #[pyo3(get, set)]
    pub content: String,
    #[pyo3(get, set)]
    pub context_before: Vec<String>,
    #[pyo3(get, set)]
    pub context_after: Vec<String>,
}

#[pymethods]
impl SearchMatch {
    #[new]
    fn new(file: String, line: u32, content: String, context_before: Vec<String>, context_after: Vec<String>) -> Self {
        SearchMatch { file, line, content, context_before, context_after }
    }
}

#[pyclass]
#[derive(Clone)]
pub struct FileInfo {
    #[pyo3(get, set)]
    pub path: String,
    #[pyo3(get, set)]
    pub size: u64,
    #[pyo3(get, set)]
    pub lines: u32,
    #[pyo3(get, set)]
    pub language: String,
}

#[pymethods]
impl FileInfo {
    #[new]
    fn new(path: String, size: u64, lines: u32, language: String) -> Self {
        FileInfo { path, size, lines, language }
    }
}

#[pyclass]
pub struct Crawler {
    root_path: String,
}

#[pymethods]
impl Crawler {
    #[new]
    fn new(path: String) -> Self {
        Crawler { root_path: path }
    }

    // Simple search - returns Vec<String>
    fn fast_search(&self, pattern: &str) -> Vec<String> {
        let path = self.root_path.clone();
        let pattern = pattern.to_string();
        
        WalkDir::new(&path)
            .into_iter()
            .par_bridge()
            .filter_map(|entry| {
                let entry = entry.ok()?;
                let path = entry.path();
                if path.is_file() {
                    if let Ok(content) = fs::read_to_string(path) {
                        if content.contains(&pattern) {
                            return Some(path.display().to_string());
                        }
                    }
                }
                None
            })
            .collect()
    }

    // Search with context - returns Vec<SearchMatch>
    fn search_with_context(&self, pattern: &str, context_lines: usize) -> Vec<SearchMatch> {
        let path = self.root_path.clone();
        let pattern = pattern.to_string();
        
        let mut results = Vec::new();
        
        for entry in WalkDir::new(&path).into_iter().filter_map(|e| e.ok()) {
            let path = entry.path();
            if path.is_file() {
                if let Ok(content) = fs::read_to_string(path) {
                    let lines: Vec<String> = content.lines().map(|l| l.to_string()).collect();
                    
                    for (i, line) in lines.iter().enumerate() {
                        if line.contains(&pattern) {
                            let start = i.saturating_sub(context_lines);
                            let end = (i + context_lines + 1).min(lines.len());
                            
                            results.push(SearchMatch {
                                file: path.display().to_string(),
                                line: (i + 1) as u32,
                                content: line.clone(),
                                context_before: lines[start..i].to_vec(),
                                context_after: lines[i+1..end].to_vec(),
                            });
                        }
                    }
                }
            }
        }
        
        results
    }

    // Find unnecessary .clone() calls - returns Vec<Bug>
    fn pinch_clones(&self) -> Vec<Bug> {
        let path = self.root_path.clone();
        let mut bugs = Vec::new();
        
        for entry in WalkDir::new(&path).into_iter().filter_map(|e| e.ok()) {
            let path = entry.path();
            if path.is_file() && path.extension().map_or(false, |e| e == "rs") {
                if let Ok(content) = fs::read_to_string(path) {
                    for (i, line) in content.lines().enumerate() {
                        if line.contains(".clone()") {
                            let trimmed = line.trim_start();
                            if !trimmed.starts_with("//") {
                                bugs.push(Bug {
                                    file: path.display().to_string(),
                                    line: (i + 1) as u32,
                                    column: line.find(".clone()").unwrap_or(0) as u32,
                                    message: "Unnecessary .clone() detected".to_string(),
                                    severity: "warning".to_string(),
                                    suggestion: "Consider using reference or borrowing".to_string(),
                                });
                            }
                        }
                    }
                }
            }
        }
        
        bugs
    }

    // Count files by language - returns HashMap
    fn count_by_language(&self) -> HashMap<String, usize> {
        let path = self.root_path.clone();
        let mut counts = HashMap::new();
        
        for entry in WalkDir::new(&path).into_iter().filter_map(|e| e.ok()) {
            let path = entry.path();
            if path.is_file() {
                let ext = path.extension()
                    .and_then(|e| e.to_str())
                    .unwrap_or("unknown")
                    .to_string();
                
                let lang = match ext.as_str() {
                    "rs" => "Rust",
                    "py" => "Python",
                    "ts" | "tsx" => "TypeScript",
                    "js" | "jsx" => "JavaScript",
                    "md" => "Markdown",
                    "toml" => "TOML",
                    "json" => "JSON",
                    _ => "Other",
                }.to_string();
                
                *counts.entry(lang).or_insert(0) += 1;
            }
        }
        
        counts
    }

    // Total lines of code
    fn total_lines(&self) -> usize {
        let path = self.root_path.clone();
        let mut total = 0;
        
        for entry in WalkDir::new(&path).into_iter().filter_map(|e| e.ok()) {
            let path = entry.path();
            if path.is_file() {
                if let Ok(content) = fs::read_to_string(path) {
                    total += content.lines().count();
                }
            }
        }
        
        total
    }
    
    // Hello test method
    fn hello(&self) -> String {
        format!("Hello from Rust! Scanning: {}", self.root_path)
    }
}

#[pymodule]
fn rustypycrawcore(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Crawler>()?;
    m.add_class::<Bug>()?;
    m.add_class::<SearchMatch>()?;
    m.add_class::<FileInfo>()?;
    Ok(())
}
