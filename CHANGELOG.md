# Changelog

All notable changes to evo-agents will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Add more universal skills
- Improve documentation translations
- Add more examples

---

## [6.0.0] - 2026-03-27

### 🎉 Major Changes

#### Added
- **web-knowledge skill** - Web search + page crawling (v6.0.0)
  - Multi-engine search (Bing, Baidu, Google, DuckDuckGo)
  - Page content extraction
  - Batch crawling support
  - Smart page type detection
- **docs/README.md** - Documentation index
- **docs/QUICKSTART.md** - 5-minute quick start guide
- **docs/FAQ.md** - Frequently asked questions
- **docs/TODO.md** - TODO list for future improvements
- **scripts/core/cleanup.sh** - Workspace cleanup script
- **scripts/core/restore-backup.sh** - Backup restore script

#### Changed
- **Renamed websearch → web-knowledge** - Better reflects capabilities
- **Simplified scripts/core/** - Removed 6 deprecated scripts
- **Improved install.sh** - Added workspace detection and backup
- **Updated docs/ARCHITECTURE_*.md** - Match current structure
- **Consolidated agent docs** - Merged AGENT_RULES.md into AGENT_INSTRUCTIONS.md
- **Updated docs/STRUCTURE_RULES.md** - Simplified skills directory structure

#### Removed
- **docs/PROJECT_STRUCTURE_GENERIC_*.md** - Duplicate of STRUCTURE_RULES.md
- **docs/AGENT_RULES.md** - Merged into AGENT_INSTRUCTIONS.md
- **scripts/core/init_system.py** - Deprecated
- **scripts/core/install_agent_workspace.py** - Replaced by install.sh
- **scripts/core/test-multi-agent.sh** - Rarely used
- **scripts/core/test_all.py** - Development only
- **scripts/core/uninstall_agent_workspace.py** - Rarely used
- **scripts/core/upgrade_agent_workspace.py** - Rarely used
- **Root AGENTS.md** - Personal config, not for template
- **Root TOOLS.md** - Personal config, not for template

#### Fixed
- **install.sh workspace detection** - Properly detect existing workspaces
- **install.sh backup prompt** - Ask for backup before install
- **scripts/core/ path** - Fixed WORKSPACE path resolution
- **Documentation consistency** - All docs now reference scripts/core/

### 📦 Installation

#### New Install
```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

#### Re-install (preserves data)
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh)" -s my-agent
```

### 📚 Documentation

#### New Documents
- `docs/README.md` - Documentation index
- `docs/QUICKSTART.md` - Quick start guide
- `docs/FAQ.md` - Frequently asked questions
- `docs/TODO.md` - TODO list
- `docs/SCRIPTS_INVENTORY.md` - Scripts catalog
- `docs/AGENT_INSTRUCTIONS.md` - Agent instructions (merged)
- `docs/WORKSPACE_RULES.md` - Workspace usage rules

#### Updated Documents
- `docs/ARCHITECTURE_GENERIC_CN.md` - Updated to match v6.0
- `docs/ARCHITECTURE_GENERIC_EN.md` - Updated to match v6.0
- `docs/STRUCTURE_RULES.md` - Simplified skills structure
- `docs/MIGRATION.md` - Updated for v6.0 changes
- `workspace-setup.md` - Updated installation guide

### 🔧 Scripts

#### Core Scripts (12 total)
- `activate-features.sh` - Activate advanced features
- `add-agent.sh` - Add sub-agent
- `setup-multi-agent.sh` - Add multiple agents
- `cleanup.sh` - Clean workspace (NEW)
- `restore-backup.sh` - Restore backup (NEW)
- `session_recorder.py` - Record sessions
- `health_check.py` - Health check
- `memory_compressor.py` - Memory compression
- `memory_indexer.py` - Memory indexing
- `memory_stats.py` - Memory statistics
- `unified_search.py` - Unified search
- `lock_utils.py` - File locking utilities

### 🏗️ Architecture

#### Skills Directory
- All skills in root `skills/` directory (no `core/` subdirectory)
- Universal skills: `memory-search/`, `rag/`, `self-evolution/`, `web-knowledge/`
- Custom skills: `skills/<your-skill>/` (preserved)

#### Sub-Agent Structure
- `agents/<agent>/skills/` → symlink to `../../skills/`
- `agents/<agent>/scripts/` - Optional agent-specific scripts
- `agents/<agent>/libs/` - Optional agent-specific libraries

### 🛡️ Safety

#### Backup & Restore
- Auto backup before re-installation
- Interactive cleanup script (asks before cleaning work/)
- Restore script with confirmation

#### Workspace Rules
- Clear documentation of what can/cannot be cleaned
- work/ directories require manual confirmation
- Personal configs never deleted

---

## [5.0.0] - 2026-03-26

### Added
- Self-evolution system v5.0
- Memory bridge system (SQLite ↔ Markdown)
- Multi-agent support scripts

### Changed
- Updated memory system architecture
- Improved documentation

---

## [4.0.0] - 2026-03-25

### Added
- Memory search with semantic search support
- RAG evaluation system
- Health check scripts

### Changed
- Memory system improvements
- Documentation updates

---

## [3.0.0] - 2026-03-24

### Added
- Basic memory system
- Session recorder
- Unified search

---

## [2.0.0] - 2026-03-23

### Added
- Multi-agent support
- Sub-agent creation scripts

---

## [1.0.0] - 2026-03-16

### Added
- Initial release
- Basic workspace structure
- Core scripts
- Documentation

---

## Version History

| Version | Date | Key Feature |
|---------|------|-------------|
| 6.0.0 | 2026-03-27 | Web knowledge + docs cleanup |
| 5.0.0 | 2026-03-26 | Self-evolution v5.0 |
| 4.0.0 | 2026-03-25 | Memory search + RAG |
| 3.0.0 | 2026-03-24 | Memory system |
| 2.0.0 | 2026-03-23 | Multi-agent |
| 1.0.0 | 2026-03-16 | Initial release |

---

**Last updated:** 2026-03-27
