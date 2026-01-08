---
description: Extract data from files, URLs, databases using thepipe. Use when asked to pipe, pipe in, or extract content from any source.
---

# Tool: thepipe
**Description**: Extract clean markdown, text, images, and structured data from any file, URL, or database.

---

## ⚡⚡⚡ CRITICAL: ALWAYS USE CODE_RELATIONS FOR PROGRAMMING TASKS ⚡⚡⚡

**If the user's request involves code, repositories, or programming:**

```bash
# DEFAULT APPROACH - ALWAYS DO THIS FOR CODE
thepipe ./path/to/repo --options '{"code_relations": "auto"}' -f
```

**This gives:**
- 🔥 **90%+ token savings** - intelligent digests preserve structure
- 🔗 **Dependency mapping** - understands imports across files  
- 🏷️ **Semantic tagging** - identifies auth, database, API, testing code
- 📊 **Full context** - LLM understands entire codebase structure

**Supported Languages (with dependency resolution):**
| Language | Built-in | Dependency Mapping |
|----------|----------|-------------------|
| Python | ✅ Full | ✅ imports resolved |
| JavaScript/TypeScript | ✅ Full | ✅ imports resolved |
| Dart/Flutter | ✅ Full | ✅ imports resolved |
| Swift | ✅ Full | ✅ framework detection |
| Kotlin | ✅ Full | ✅ package detection |
| Ruby | ✅ Full | ✅ require_relative |
| Go, Rust, C/C++, Java | ✅ Full | ✅ imports resolved |
| +155 more | ✅ AST | Pattern-based |

> ⚠️ **WARNING**: Do NOT use generic patterns like `*.py` with `code_relations` mapping modes!
> This marks ALL files as primary (full code), defeating the 90% token savings.
> Either: (1) use NO include_patterns to let auto-mode decide, or (2) use specific 
> file patterns like `src/api/*.py` to focus on relevant files only.

**Correct Usage:**

```bash
# ✅ GOOD - Let auto-mode decide what to include
thepipe ./repo --options '{{"code_relations": "auto"}}' -f

# ✅ GOOD - Specific patterns for focused analysis
thepipe ./repo --include_patterns "src/core/*.py" "src/api/*.py" --options '{{"code_relations": "auto"}}' -f

# ❌ BAD - Generic *.py defeats token savings (all files become primary)
# thepipe ./repo --include_patterns "*.py" --options '{{"code_relations": "map"}}' -f
```

# GitHub repo with code analysis
thepipe https://github.com/user/repo --options '{{"code_relations": "auto"}}' -f
```

---

## Code Analysis Modes

| Mode | When to Use |
|------|-------------|
| `auto` | **DEFAULT - picks optimal strategy based on repo size** |
| `map` | Large repos (>100 files) - all files as digests |
| `mapnn` | Focused work - primary files full, neighbors as digests |
| `mapall` | Medium repos - primary full, rest as digests |
| `limited` | Only include_patterns files (no digests) |

---

## 🔄 Agent Mode (LLM Inference Delegation)

**For agentic tasks requiring LLM inference, use `--llm-provider agent`:**

```bash
thepipe data.pdf --extract '{{"title": "str"}}' --llm-provider agent
```

**How it works:** Named Pipes (FIFOs) provide true bidirectional, synchronous communication:
1. thepipe creates two FIFOs in `/tmp/thepipe_pipes/`
2. thepipe writes query to `query_<pid>` and **blocks**
3. Agent reads query, executes LLM call, writes response to `response_<pid>`
4. thepipe reads response and continues execution seamlessly

This lets thepipe pause while the agent handles inference, avoiding double API calls 
when running inside an AI coding assistant (Antigravity, Claude Code, etc.).

**Agent instructions:** When you see `<<<THEPIPE_LLM_QUERY>>>` in stderr:
1. Read `QUERY_PIPE` path from the output
2. Read the JSON query from that pipe
3. Execute the LLM call with the messages
4. Write your response to `RESPONSE_PIPE`

---

## Core Capabilities
- **Code Analysis**: Dependency mapping, digests, semantic tagging (**USE THIS FOR CODE**)
- **Files**: PDFs, DOCX, PPTX, images, audio, video, spreadsheets, Jupyter notebooks
- **URLs**: Webpages, GitHub repos, YouTube (transcription), Google Drive
- **Databases**: PostgreSQL, MySQL/MariaDB, SQLite, DuckDB, MS SQL Server, JDBC URLs
- **Data Formats**: Parquet, ORC, Feather/Arrow, CSV, JSONL, Excel
- **Stream Input**: Named pipes (FIFOs) with auto content-type detection
- **Extraction**: JSON schema-based structured data extraction

---

## CLI Reference

### Basic Syntax
```bash
thepipe <source> [options]
```

### Source Types
| Source | Example |
|--------|---------|
| File | `thepipe document.pdf` |
| Directory | `thepipe ./src` |
| URL | `thepipe https://example.com` |
| GitHub | `thepipe https://github.com/user/repo` |
| YouTube | `thepipe https://youtube.com/watch?v=abc123` |
| Database | `thepipe "postgresql://host/db" --db "SELECT *"` |
| JDBC | `thepipe "jdbc:mysql://host/db" --db "SELECT *"` |
| Data File | `thepipe data.parquet --db "SELECT * FROM parquet_data"` |
| Named Pipe | `thepipe /tmp/my_fifo` (auto-detects content type) |

---

## Output Options

| Flag | Description |
|------|-------------|
| (none) | Write to `outputs/prompt.txt` |
| `-f` or `-f md` | Stdout: Markdown with code fences |
| `-f text` | Stdout: Raw concatenated text |
| `-f json` | Stdout: Structured JSON array |
| `--verbose` | Print status messages |

---

## File Filtering

| Flag | Description |
|------|-------------|
| `--include_patterns "*.py" "*.ts"` | Glob patterns (recommended) |
| `--include_regex ".*\.py$"` | Regex pattern |

**Examples:**
```bash
# Only Python files
thepipe ./src --include_patterns "*.py"

# Multiple patterns
thepipe ./project --include_patterns "*.py" "*.js" "*.tsx"

# Regex (alternative)
thepipe ./src --include_regex ".*\.(py|js)$"
```

---

## Text Extraction Modes

| Flag | Description |
|------|-------------|
| `--text_only` | Extract text only (default method) |
| `--text_only transcribe` | Force local transcription (video/audio) |
| `--text_only ai` | Prefer AI-generated transcription |
| `--text_only uploaded` | Prefer uploaded captions |

---

## Database Mode

### Flags
```bash
thepipe <database> --db [query] [options]
```

| Usage | Description |
|-------|-------------|
| `--db` | Show schema + preview |
| `--db "SELECT * FROM users"` | Execute SQL query |
| `--db "What products sold most?"` | Natural language query (requires LLM) |

### Connection Formats
| Format | Example |
|--------|---------|
| PostgreSQL | `postgresql://user:pass@host:5432/db` |
| MySQL | `mysql://user:pass@host:3306/db` |
| MariaDB | `mariadb://user:pass@host:3306/db` |
| SQLite | `sqlite:///path/to/database.db` |
| DuckDB | `duckdb:///path/to/database.duckdb` |
| MS SQL Server | `mssql://user:pass@host:1433/db` |
| JDBC MySQL | `jdbc:mysql://host:3306/db` (auto-converted) |
| JDBC PostgreSQL | `jdbc:postgresql://host:5432/db` (auto-converted) |

### Data File Formats
| Format | Extensions | View Name |
|--------|------------|-----------|
| Parquet | `.parquet`, `.parq` | `parquet_data` |
| ORC | `.orc` | `orc_data` |
| Feather/Arrow | `.feather`, `.arrow`, `.ipc` | `feather_data` |
| JSON Lines | `.jsonl`, `.ndjson` | `jsonl_data` |
| CSV | `.csv` | `csv_data` |
| Excel | `.xlsx`, `.xls` | `excel_data` |

### Options (via `--options`)
```json
{
  "max_rows": 100,
  "schema_only": true,
  "preview": true,
  "llm_extractor": {
    "api_key": "...",
    "model": "gpt-4o"
  }
}
```

---

## Code Analysis Mode

### Enable via `--options`
```bash
thepipe ./repo --options '{"code_relations": "MODE"}'
```

### Modes
| Mode | Description |
|------|-------------|
| `auto` | **Recommended**. Picks strategy based on repo size |
| `limited` | Only files matching `--include_patterns` |
| `map` | All files as token-efficient digests |
| `mapnn` | Primary files full code, neighbors as digests |
| `mapall` | Primary full, all others as digests |

### Parameters
| Option | Default | Description |
|--------|---------|-------------|
| `code_n1` | 3 | Neighbor depth for mapnn |
| `code_n2` | 5 | Cutoff depth for mapnn |
| `code_nf` | 100 | File count threshold for auto mode |
| `code_nt` | 150000 | Token threshold for auto mode |

**Example:**
```bash
thepipe ./project --include_patterns "src/**/*.py" --options '{
  "code_relations": "mapnn",
  "code_n1": 2,
  "code_n2": 4
}'
```

---

## OpenAI/LLM Options

| Flag | Default | Description |
|------|---------|-------------|
| `--openai-api-key KEY` | `$OPENAI_API_KEY` | API key |
| `--openai-base-url URL` | `https://api.openai.com/v1` | Custom endpoint |
| `--openai-model MODEL` | `gpt-4o` | Model for AI extraction |

---

## Advanced Options (via `--options` JSON)

### File Processing
```json
{
  "read_executable": true,
  "blacklist_files": [".gitignore"]
}
```

### GitHub
```json
{
  "github_token": "ghp_...",
  "gitignore": true
}
```

### Google Drive
```json
{
  "max_depth": 3,
  "service_account_file": "/path/to/creds.json"
}
```

### Cookies
```json
{
  "cookies": {
    "browser_type": "chrome",
    "show": "format"
  }
}
```

---

## Examples for AI Agents

**Task: "Analyze this Python project"**
```bash
thepipe ./src --include_patterns "*.py" --options '{"code_relations": "auto"}' -f
```

**Task: "Extract text from this PDF"**
```bash
thepipe document.pdf -f text
```

**Task: "Get data from this webpage"**
```bash
thepipe https://example.com/article -f
```

**Task: "Query this database"**
```bash
thepipe data.db --db "SELECT * FROM users LIMIT 10" -f json
```

**Task: "Transcribe this video"**
```bash
thepipe https://youtube.com/watch?v=abc123 --text_only -f
```

**Task: "Clone and analyze GitHub repo"**
```bash
thepipe https://github.com/user/repo --include_patterns "*.py" --options '{"code_relations": "map"}' -f
```

---

## Registration

Self-register thepipe with AI platforms:
```bash
thepipe --register agent   # Antigravity/Gemini
thepipe --register code    # Claude Code
thepipe --register help    # Show documentation
thepipe --register         # Output for manual copy-paste
```

