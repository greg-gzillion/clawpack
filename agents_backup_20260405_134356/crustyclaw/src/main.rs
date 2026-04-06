use reqwest::Client;
use serde_json::json;
use std::env;
use std::fs;
use std::path::Path;
use std::process::Command;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        print_help();
        return Ok(());
    }
    
    match args[1].as_str() {
        // AI commands - using local Ollama (no API key needed)
        "ask" if args.len() > 2 => {
            let question = &args[2..].join(" ");
            ask_ollama(question).await?;
        }
        "analyze" if args.len() > 2 => {
            analyze_file(&args[2]).await?;
        }
        "audit" if args.len() > 2 => {
            audit_project(&args[2]).await?;
        }
        
        // Lobster special commands
        "pinch" if args.len() > 2 => {
            pinch_bugs(&args[2]).await?;
        }
        "shell" => {
            lobster_shell().await?;
        }
        "molt" => {
            molt_upgrade().await?;
        }
        "claw" => show_lobster(),
        
        // System commands
        "status" => system_status(),
        "optimize" => system_optimize(),
        "clean" => system_clean(),
        "prices" => show_prices(),
        "help" => print_help(),
        
        _ => println!("Unknown command. Try: help, pinch, shell, molt, ask, audit, claw"),
    }
    
    Ok(())
}

// ============ AI FUNCTIONS - Using Local Ollama ============
async fn ask_ollama(question: &str) -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new();
    
    println!("Thinking... 🧠");
    
    let response = client
        .post("http://localhost:11434/api/generate")
        .json(&json!({
            "model": "codellama:7b",
            "prompt": question,
            "stream": false
        }))
        .send()
        .await?;
    
    let result: serde_json::Value = response.json().await?;
    if let Some(answer) = result["response"].as_str() {
        println!("\n{}\n", answer);
    }
    Ok(())
}

async fn analyze_file(path: &str) -> Result<(), Box<dyn std::error::Error>> {
    if !Path::new(path).exists() {
        println!("File not found: {}", path);
        return Ok(());
    }
    
    let content = fs::read_to_string(path)?;
    let preview = if content.len() > 2000 {
        format!("{}...\n\n[File truncated: {} total chars]", &content[..2000], content.len())
    } else {
        content
    };
    
    let question = format!("Analyze this Rust/CosmWasm file and provide insights on code quality, potential issues, and best practices:\n\n{}", preview);
    println!("Analyzing code... 🔍");
    ask_ollama(&question).await?;
    Ok(())
}

// ============ LOBSTER SPECIAL COMMANDS ============

async fn pinch_bugs(target: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("PINCH MODE - Squashing bugs!");
    println!("==========================");
    println!("Target: {}", target);
    
    let mut fixed_count = 0;
    let mut warning_count = 0;
    let mut file_count = 0;
    
    // Find and "pinch" (fix) common issues
    for entry in walkdir::WalkDir::new(target)
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|e| e.path().extension().map_or(false, |ext| ext == "rs"))
    {
        file_count += 1;
        let path = entry.path();
        
        // Skip target/ directory
        if path.to_string_lossy().contains("/target/") {
            continue;
        }
        
        let content = fs::read_to_string(path)?;
        let mut new_content = content.clone();
        let mut modified = false;
        
        // Pinch unwrap() -> ? operator (but be careful with tests)
        if content.contains(".unwrap()") && !path.to_string_lossy().contains("tests") {
            new_content = new_content.replace(".unwrap()", "?");
            println!("✓ Pinched .unwrap() in {}", path.display());
            modified = true;
            fixed_count += 1;
        }
        
        // Warn about clone() on references
        if content.contains(".clone()") && content.contains("&") {
            println!("⚠️ Found .clone() on reference in {} - manual review needed", path.display());
            warning_count += 1;
        }
        
        // Warn about expect() in production code
        if content.contains(".expect(") && !path.to_string_lossy().contains("tests") {
            println!("⚠️ Found .expect() in {} - consider better error handling", path.display());
            warning_count += 1;
        }
        
        if modified {
            fs::write(path, new_content)?;
        }
    }
    
    println!("\nPINCH SUMMARY");
    println!("==============");
    println!("Files scanned: {}", file_count);
    println!("Bugs pinched: {}", fixed_count);
    println!("Warnings: {}", warning_count);
    println!("🦞🦞🦞🦞🦞🦞🦞🦞🦞");
    
    if fixed_count > 0 {
        println!("Success! Your code is less buggy!");
        println!("Run 'cargo test' to verify changes");
    } else if warning_count > 0 {
        println!("No auto-fixable bugs found, but review the warnings above.");
    } else {
        println!("No issues found. Your code is clean!");
    }
    
    Ok(())
}

async fn lobster_shell() -> Result<(), Box<dyn std::error::Error>> {
    println!("🐚 LOBSTER SHELL - Type commands, 'exit' to quit, 'help' for lobster wisdom");
    println!("==========================================================================");
    
    use std::io::{self, Write};
    
    loop {
        print!("🐚 ");
        io::stdout().flush()?;
        
        let mut input = String::new();
        io::stdin().read_line(&mut input)?;
        let input = input.trim();
        
        if input == "exit" {
            println!("Goodbye!");
            break;
        } else if input == "help" {
            println!("LOBSTER WISDOM:");
            println!("  🦞 Pinch bugs, don't let them pinch you");
            println!("  🦞 Molt regularly to stay sharp");
            println!("  🦞 The best code is well-seasoned");
            println!("  🦞 Claws deep into the problem");
        } else if input == "🦞" || input == "lobster" || input == "claw" {
            show_lobster();
        } else if input.starts_with("cd ") {
            // Handle cd command
            let dir = &input[3..];
            if let Err(e) = env::set_current_dir(dir) {
                println!("Error: {}", e);
            }
        } else {
            // Run the command
            let output = Command::new("sh")
                .arg("-c")
                .arg(input)
                .output()?;
            
            if !output.stdout.is_empty() {
                println!("{}", String::from_utf8_lossy(&output.stdout));
            }
            if !output.stderr.is_empty() {
                eprintln!("{}", String::from_utf8_lossy(&output.stderr));
            }
        }
    }
    
    Ok(())
}

async fn molt_upgrade() -> Result<(), Box<dyn std::error::Error>> {
    println!("🦞 MOLTING - Upgrading CrustyClaw...");
    println!("==================================");
    
    // Check current version
    let current_version = env!("CARGO_PKG_VERSION");
    println!("Current version: v{}", current_version);
    
    // Pull latest from git if it's a git repo
    if Path::new(".git").exists() {
        println!("Fetching latest updates...");
        let pull_output = Command::new("git")
            .args(["pull", "origin", "main"])
            .output();
        
        if let Ok(output) = pull_output {
            if output.status.success() {
                println!("Updates fetched successfully!");
            } else {
                println!("No updates found or git pull failed.");
            }
        }
    }
    
    // Rebuild
    println!("Rebuilding CrustyClaw...");
    let build_output = Command::new("cargo")
        .args(["build", "--release"])
        .output()?;
    
    if build_output.status.success() {
        // Reinstall
        println!("Installing new version...");
        let install_output = Command::new("sudo")
            .args(["cp", "target/release/crustyclaw", "/usr/local/bin/crustyclaw"])
            .output()?;
        
        if install_output.status.success() {
            println!("✅ MOLT COMPLETE!");
            println!("🦞 CrustyClaw has shed its shell and grown a new one!");
            println!("Run 'crustyclaw --version' to see the new version");
        } else {
            println!("❌ Failed to install. Try: sudo cp target/release/crustyclaw /usr/local/bin/");
        }
    } else {
        println!("❌ Build failed. Check the errors above.");
    }
    
    Ok(())
}

// ============ AUDIT FUNCTION ============

async fn audit_project(path: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("CRUSTYCLAW SECURITY AUDIT");
    println!("========================");
    println!("Target: {}", path);
    println!("");
    
    let mut issues = Vec::new();
    let mut good = Vec::new();
    
    println!("Scuttling through the codebase... 🦀");
    
    // Check for common Rust issues
    let output = Command::new("grep")
        .args(["-rn", "unwrap()", path, "--include=*.rs"])
        .output()?;
    if !output.stdout.is_empty() {
        let count = String::from_utf8_lossy(&output.stdout).lines().count();
        issues.push(format!("Found {} .unwrap() calls - can cause panics", count));
    }
    
    let output = Command::new("grep")
        .args(["-rn", "unsafe", path, "--include=*.rs"])
        .output()?;
    if !output.stdout.is_empty() {
        let count = String::from_utf8_lossy(&output.stdout).lines().count();
        issues.push(format!("Found {} unsafe blocks - review carefully", count));
    }
    
    let output = Command::new("grep")
        .args(["-rn", "expect(", path, "--include=*.rs"])
        .output()?;
    if !output.stdout.is_empty() {
        let count = String::from_utf8_lossy(&output.stdout).lines().count();
        issues.push(format!("Found {} .expect() calls - potential panic points", count));
    }
    
    // PhoenixPME specific checks
    let output = Command::new("grep")
        .args(["-rn", "collateral", path, "--include=*.rs"])
        .output()?;
    if output.stdout.is_empty() {
        issues.push("⚠️ No collateral mechanism found - Required for PhoenixPME".to_string());
    } else {
        good.push("✅ Collateral mechanism present".to_string());
    }
    
    let output = Command::new("grep")
        .args(["-rn", "fee", path, "--include=*.rs"])
        .output()?;
    if output.stdout.is_empty() {
        issues.push("⚠️ No fee structure found - PhoenixPME requires fee mechanism".to_string());
    } else {
        good.push("✅ Fee structure present".to_string());
    }
    
    // Print report
    println!("\n📊 AUDIT REPORT");
    println!("================");
    
    if !good.is_empty() {
        println!("\n✅ PASSED CHECKS:");
        for g in &good {
            println!("  {}", g);
        }
    }
    
    if !issues.is_empty() {
        println!("\n⚠️ ISSUES FOUND:");
        for issue in &issues {
            println!("  {}", issue);
        }
    }
    
    if issues.is_empty() && !good.is_empty() {
        println!("\n🎉 EXCELLENT! No critical issues found!");
        println!("🦞 Your code is claw-some!");
    }
    
    Ok(())
}

// ============ SYSTEM FUNCTIONS ============
fn system_status() {
    println!("SYSTEM STATUS");
    println!("=============");
    
    if let Ok(output) = Command::new("nproc").output() {
        if let Ok(cpus) = String::from_utf8(output.stdout) {
            println!("CPU Cores: {}", cpus.trim());
        }
    }
    
    if let Ok(output) = Command::new("free").args(["-h"]).output() {
        if let Ok(mem) = String::from_utf8(output.stdout) {
            for line in mem.lines().skip(1).take(1) {
                println!("Memory: {}", line);
            }
        }
    }
    
    if let Ok(output) = Command::new("df").args(["-h", "/"]).output() {
        if let Ok(disk) = String::from_utf8(output.stdout) {
            if let Some(line) = disk.lines().nth(1) {
                println!("Disk: {}", line);
            }
        }
    }
}

fn system_optimize() {
    println!("🔧 Optimizing system...");
    Command::new("sudo").args(["apt", "autoremove", "-y"]).output().ok();
    Command::new("sudo").args(["apt", "autoclean", "-y"]).output().ok();
    println!("✅ System optimized!");
}

fn system_clean() {
    println!("🧹 Cleaning system...");
    Command::new("sudo").args(["apt", "clean"]).output().ok();
    println!("✅ System cleaned!");
}

fn show_prices() {
    println!("🏛️ METAL PRICES");
    println!("  Gold: $4,676 | Silver: $72.90");
    println!("  Platinum: $1,980 | Palladium: $1,490");
}

fn show_lobster() {
    println!("");
    println!("  .--.");
    println!(" |o_o |");
    println!(" |:_/ |");
    println!(" //   \\\\ \\");
    println!("(|     |)");
    println!("('\\_   _/`\\");
    println!("\\___)=(___/");
    println!("");
    println!("CRUSTYCLAW - The Lobster of Code!");
    println!("Your AI assistant for TX Blockchain & PhoenixPME");
}

fn print_help() {
    println!("CRUSTYCLAW - Code Analysis Tool");
    println!("===============================");
    println!("");
    println!("CORE COMMANDS:");
    println!("  ask <question>           - Ask AI anything (uses local Ollama)");
    println!("  analyze <file>           - AI analysis of any file");
    println!("  audit <path>             - Security audit of codebase");
    println!("");
    println!("LOBSTER SPECIALS:");
    println!("  pinch <path>             - Automatically fix common bugs");
    println!("  shell                    - Interactive shell with lobster theme");
    println!("  molt                     - Self-upgrade CrustyClaw");
    println!("  claw                     - Show the lobster");
    println!("");
    println!("SYSTEM COMMANDS:");
    println!("  status                   - System status");
    println!("  optimize                 - Optimize system");
    println!("  clean                    - Clean system");
    println!("  prices                   - Show metal prices");
    println!("  help                     - Show this help");
    println!("");
    println!("EXAMPLES:");
    println!("  crustyclaw pinch ~/dev/TX");
    println!("  crustyclaw ask 'What is CosmWasm?'");
    println!("  crustyclaw audit ~/dev/TX/contracts");
    println!("  crustyclaw analyze ~/dev/TX/contracts/auction/src/contract.rs");
    println!("  crustyclaw shell");
}
