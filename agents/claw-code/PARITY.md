# Parity Status — claw-code Rust Port

Last updated: 2026-04-03

## Mock parity harness — milestone 1

- [x] Deterministic Anthropic-compatible mock service (`rust/crates/mock-anthropic-service`)
- [x] Reproducible clean-environment CLI harness (`rust/crates/rusty-claude-cli/tests/mock_parity_harness.rs`)
- [x] Scripted scenarios: `streaming_text`, `read_file_roundtrip`, `grep_chunk_assembly`, `write_file_allowed`, `write_file_denied`

## Mock parity harness — milestone 2 (behavioral expansion)

- [x] Scripted multi-tool turn coverage: `multi_tool_turn_roundtrip`
- [x] Scripted bash coverage: `bash_stdout_roundtrip`
- [x] Scripted permission prompt coverage: `bash_permission_prompt_approved`, `bash_permission_prompt_denied`
- [x] Scripted plugin-path coverage: `plugin_tool_roundtrip`
- [x] Behavioral diff/checklist runner: `rust/scripts/run_mock_parity_diff.py`

## Harness v2 behavioral checklist

Canonical scenario map: `rust/mock_parity_scenarios.json`

- Multi-tool assistant turns
- Bash flow roundtrips
- Permission enforcement across tool paths
- Plugin tool execution path
- File tools — harness-validated flows

## Tool Surface: 40/40 (spec parity)

### Real Implementations (behavioral parity — varying depth)

| Tool | Rust Impl | Behavioral Notes |
|------|-----------|-----------------|
| **bash** | `runtime::bash` 283 LOC | subprocess exec, timeout, background, sandbox — **strong parity**. Missing: sedValidation, pathValidation, readOnlyValidation, destructiveCommandWarning, commandSemantics (upstream has 18 submodules for bash alone) |
| **read_file** | `runtime::file_ops` | offset/limit read — **good parity** |
| **write_file** | `runtime::file_ops` | file create/overwrite — **good parity** |
| **edit_file** | `runtime::file_ops` | old/new string replacement — **good parity**. Missing: replace_all was recently added |
| **glob_search** | `runtime::file_ops` | glob pattern matching — **good parity** |
| **grep_search** | `runtime::file_ops` | ripgrep-style search — **good parity** |
| **WebFetch** | `tools` | URL fetch + content extraction — **moderate parity** (need to verify content truncation, redirect handling vs upstream) |
| **WebSearch** | `tools` | search query execution — **moderate parity** |
| **TodoWrite** | `tools` | todo/note persistence — **moderate parity** |
| **Skill** | `tools` | skill discovery/install — **moderate parity** |
| **Agent** | `tools` | agent delegation — **moderate parity** |
| **ToolSearch** | `tools` | tool discovery — **good parity** |
| **NotebookEdit** | `tools` | jupyter notebook cell editing — **moderate parity** |
| **Sleep** | `tools` | delay execution — **good parity** |
| **SendUserMessage/Brief** | `tools` | user-facing message — **good parity** |
| **Config** | `tools` | config inspection — **moderate parity** |
| **EnterPlanMode** | `tools` | worktree plan mode toggle — **good parity** |
| **ExitPlanMode** | `tools` | worktree plan mode restore — **good parity** |
| **StructuredOutput** | `tools` | passthrough JSON — **good parity** |
| **REPL** | `tools` | subprocess code execution — **moderate parity** |
| **PowerShell** | `tools` | Windows PowerShell execution — **moderate parity** |

### Stubs Only (surface parity, no behavior)

| Tool | Status | Notes |
|------|--------|-------|
| **AskUserQuestion** | stub | needs user I/O integration |
| **TaskCreate** | stub | needs sub-agent runtime |
| **TaskGet** | stub | needs task registry |
| **TaskList** | stub | needs task registry |
| **TaskStop** | stub | needs process management |
| **TaskUpdate** | stub | needs task message passing |
| **TaskOutput** | stub | needs output capture |
| **TeamCreate** | stub | needs parallel task orchestration |
| **TeamDelete** | stub | needs team lifecycle |
| **CronCreate** | stub | needs scheduler runtime |
| **CronDelete** | stub | needs cron registry |
| **CronList** | stub | needs cron registry |
| **LSP** | stub | needs language server client |
| **ListMcpResources** | stub | needs MCP client |
| **ReadMcpResource** | stub | needs MCP client |
| **McpAuth** | stub | needs OAuth flow |
| **MCP** | stub | needs MCP tool proxy |
| **RemoteTrigger** | stub | needs HTTP client |
| **TestingPermission** | stub | test-only, low priority |

## Slash Commands: 67/141 upstream entries

- 27 original specs (pre-today) — all with real handlers
- 40 new specs — parse + stub handler ("not yet implemented")
- Remaining ~74 upstream entries are internal modules/dialogs/steps, not user `/commands`

### Missing Behavioral Features (in existing real tools)

**Bash tool — upstream has 18 submodules, Rust has 1:**
- [ ] `sedValidation` — validate sed commands before execution
- [ ] `pathValidation` — validate file paths in commands
- [ ] `readOnlyValidation` — block writes in read-only mode
- [ ] `destructiveCommandWarning` — warn on rm -rf, etc.
- [ ] `commandSemantics` — classify command intent
- [ ] `bashPermissions` — permission gating per command type
- [ ] `bashSecurity` — security checks
- [ ] `modeValidation` — validate against current permission mode
- [ ] `shouldUseSandbox` — sandbox decision logic

Harness note: milestone 2 validates bash success plus workspace-write escalation approve/deny flows, but the deeper validation/security submodules above are still open.

**File tools — need verification:**
- [ ] Path traversal prevention (symlink following, ../ escapes)
- [ ] Size limits on read/write
- [ ] Binary file detection
- [ ] Permission mode enforcement (read-only vs workspace-write)

Harness note: read_file, grep_search, write_file allow/deny, and multi-tool same-turn assembly are now covered by the mock parity harness.

**Config/Plugin/MCP flows:**
- [ ] Full MCP server lifecycle (connect, list tools, call tool, disconnect)
- [ ] Plugin install/enable/disable/uninstall full flow
- [ ] Config merge precedence (user > project > local)

Harness note: external plugin discovery + execution is now covered via `plugin_tool_roundtrip`; full lifecycle and MCP behavior remain open.

## Runtime Behavioral Gaps

- [ ] Permission enforcement across all tools (read-only, workspace-write, danger-full-access)
- [ ] Output truncation (large stdout/file content)
- [ ] Session compaction behavior matching
- [ ] Token counting / cost tracking accuracy
- [x] Streaming response support validated by the mock parity harness

Harness note: current coverage now includes write-file denial, bash escalation approve/deny, and plugin workspace-write execution paths.

## Migration Readiness

- [ ] `PARITY.md` maintained and honest
- [ ] No `#[ignore]` tests hiding failures (only 1 allowed: `live_stream_smoke_test`)
- [ ] CI green on every commit
- [ ] Codebase shape clean for handoff
