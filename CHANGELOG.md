# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-25

### Added
- Unified Memory System with bidirectional Markdown ↔ SQLite bridge
- Semantic search with bge-m3 embedding model (via Ollama)
- FTS5 Chinese full-text search with jieba tokenization
- Smart importance scoring (decisions 8+, learnings 6+, events 5)
- Automatic compression: daily → weekly → monthly → long-term
- Concurrency safety with fcntl locks and SQLite WAL mode
- One-click install script (`init-agent.sh`)
- Complete bilingual documentation (EN/ZH)
- Health check with auto-fix capabilities

### Changed
- Repository focus from "evo-agents" to "Unified Memory System"
- README completely rewritten with clear quick-start guide
- AGENTS.md updated with conversation memory flow specification

### Fixed
- Concurrent write conflicts with file locking
- Data loss on file truncation with atomic read-modify-write
- Bridge sync cache invalidation when files are cleared
- Empty file header recovery

## [0.9.0] - 2026-03-24

### Added
- Memory Hub library for agent data isolation
- Self-evolution skills with nightly cycle
- RAG evaluation system
- Web search skill

### Changed
- Workspace structure standardized
- Configuration separation for security

## [0.1.0] - 2026-03-16

### Added
- Initial project setup
- Basic agent workspace template
- Documentation structure
