# Changelog

All notable changes to evo-agents will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Multi-agent management scripts (`setup-multi-agent.sh`, `add-agent.sh`)
- Natural language installation via OpenClaw
- Complete workspace documentation (`workspace-setup.md`)
- Multi-Agent implementation test report

### Changed
- Simplified script usage (no need to pass workspace path)
- Auto-generate `-agent` suffix for role names
- Updated README with natural language installation

### Fixed
- (Add bug fixes here)

## [1.0.0] - 2026-03-26

### Added
- Initial release of evo-agents
- Multi-agent workspace architecture
- Bidirectional sync system (Markdown ↔ SQLite)
- Semantic search support (Ollama + bge-m3)
- Data isolation for sub-agents
- Shared scripts/libs/skills across agents
- One-click installation scripts
- Complete documentation (Chinese & English)
- Test suite for multi-agent architecture

### Features
- **Multi-Agent Collaboration** - Create professional sub-agents (analyst/developer/tester or custom roles)
- **Memory Management** - Bidirectional sync with semantic search
- **Data Isolation** - Each agent has independent memory/ and data/
- **Shared Resources** - All agents share scripts/libs/skills
- **Natural Language Install** - Install using OpenClaw natural language commands

### Scripts
- `setup-multi-agent.sh` - Batch create multiple agents
- `add-agent.sh` - Add single agent
- `test-multi-agent.sh` - Test multi-agent architecture

### Documentation
- `README.md` - English documentation
- `README.zh-CN.md` - Chinese documentation
- `workspace-setup.md` - Complete installation guide
- `docs/` - Architecture and project structure docs

---

## Version History

- **[1.0.0]** - 2026-03-26 - Initial Release

### Key Dates
- **2026-03-16** - Project started
- **2026-03-24** - Multi-agent architecture designed
- **2026-03-25** - Core scripts implemented
- **2026-03-26** - Official release (v1.0.0)

---

## Upcoming Features

### Planned
- [ ] Web UI for agent management
- [ ] Pre-built agent templates (content team, dev team, etc.)
- [ ] Agent communication protocols
- [ ] Performance optimization for large-scale deployments
- [ ] Integration with more OpenClaw features

### Under Consideration
- [ ] Agent marketplace
- [ ] Shared memory between agents
- [ ] Agent role templates
- [ ] Automated testing framework

---

**Note:** This changelog follows the Keep a Changelog format. For more information, visit https://keepachangelog.com/
