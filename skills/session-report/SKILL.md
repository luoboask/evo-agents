# Session Report - Conversation Summary & Memory Saver

> **Core Concept**: Session isolation ≠ Knowledge loss  
> **Purpose**: Extract cross-session valuable knowledge, discard temporary states  
> **Status**: ✅ Production Ready | Manual Trigger | Three-Layer Filtering

---

## 🎯 When to Use

### ✅ Recommended Scenarios

- After completing important tasks or project milestones
- After making key architectural decisions with clear rationale
- After discovering new knowledge, tips, or workarounds
- After user provides workflow guidance (correction or confirmation)
- After learning about user's role, preferences, or goals
- Before ending a session, want to preserve highlights

### ❌ Not Recommended

- Just temporary debugging, no general value
- Task still in progress, status changes frequently
- Pure chat without substantial content
- Involving sensitive information (passwords, keys, etc.)

---

## 🚀 Quick Start

### Basic Usage

```bash
# Full flow (preview → confirm → save)
/session-report

# Preview only, don't save
/session-report --dry-run

# Force save (skip confirmation, use with caution)
/session-report --force
```

### Specify Type

```bash
# Only save user memory
/session-report --type user

# Only save feedback memory
/session-report --type feedback

# Only save project memory
/session-report --type project

# Only save reference memory
/session-report --type reference
```

### Limit Scope

```bash
# Review only last 50 messages
/session-report --limit 50

# Export as Markdown file
/session-report --export report.md
```

---

## 📋 What to Save vs Discard

### ✅ Should Save (Long-term Value)

| Type | Example | Destination |
|------|---------|-------------|
| **User Preferences** | "I prefer concise replies" | MEMORY.md (Feedback) |
| **Project Decisions** | "Choose Redis for caching needs" | MEMORY.md (Project) |
| **External Resources** | "API docs at api.example.com" | MEMORY.md (Reference) |
| **User Role** | "I'm a data scientist" | MEMORY.md (User) |
| **Workflow Guidance** | "Tests must use real database" | MEMORY.md (Feedback) |
| **Non-derivable Knowledge** | "Legal compliance requires this" | MEMORY.md (Project) |

### ❌ Should Discard (Temporary States)

| Type | Example | Reason |
|------|---------|--------|
| **Task Status** | "Fixing bug #123" | Session-specific, quickly outdated |
| **Intermediate Code** | Unfinished implementation | Codebase is authoritative source |
| **One-time Conversations** | "Help me check this file" | No general value |
| **Derivable Info** | Git commits, file structure | `git log` / code can derive |
| **Debugging Process** | "Tried A, didn't work, tried B" | Solution already in code |

---

## 🏗️ Execution Flow

### Step 1: Review Session History

```python
# Get current session conversation records
messages = get_session_history(limit=100)
```

**Note**: 
- Only review current session, not other sessions
- Maintain session isolation
- If session too long, focus on last 20-50 messages

---

### Step 2: Identify Candidates

Use three-layer filtering:

#### Layer 1: Temporary vs Long-term

```python
def is_long_term_value(message):
    """Judge if has long-term value"""
    # ❌ Temporary states
    if contains_temporal_refs(message):  # "now", "today", "this bug"
        return False
    if is_task_status(message):  # "doing X"
        return False
    
    # ✅ Long-term knowledge
    if is_user_preference(message):  # "I prefer..."
        return True
    if is_project_decision(message):  # "we decided..."
        return True
    if is_external_reference(message):  # "docs at..."
        return True
    
    return False
```

#### Layer 2: Private vs Shared

```python
def determine_scope(content):
    """Determine scope"""
    if is_personal_preference(content):
        return 'private'  # User memory
    elif is_team_convention(content):
        return 'team'     # Team memory
    else:
        return 'project'  # Project memory
```

#### Layer 3: Derivable vs Non-derivable

```python
def is_derivable_from_code(content):
    """Judge if can derive from code"""
    # ❌ Should not save (code/tools can derive)
    if is_file_structure(content):      # File list
        return True
    if is_git_history(content):         # Commit history
        return True
    if is_code_pattern_obvious(content): # Obvious code patterns
        return True
    
    # ✅ Should save (non-derivable)
    # - Decision reasons (why A not B)
    # - User preferences (communication style)
    # - External dependencies (third-party system locations)
    # - Historical lessons (past pitfalls)
    return False
```

---

### Step 3: Generate Structured Report

```markdown
## Session Report - {datetime}

### 🧠 New Knowledge (Recommended to Save)

#### User Memory
- {User role/preferences/goals}

#### Feedback Memory
- {Workflow guidance + Why + How to apply}

#### Project Memory
- {Project decision/goal/event + Why + How to apply}

#### Reference Memory
- {External resource location + purpose}

### 💡 Reusable Patterns
- {Reusable code patterns/tools}

### ❌ Discarded (Temporary States)
- {Temporary task status}
- {Intermediate code snippets}
- {One-time conversations}

### 📊 Statistics
- Messages reviewed: {N}
- Recommended to save: {M} items
- Discarded: {K} items
```

---

### Step 4: User Confirmation (Critical!)

```markdown
📋 Session Report Preview

I analyzed {N} messages from this session and found the following worth saving:

**✅ Recommended to Save ({M} items):**

1. **[User Memory]** User prefers TypeScript over JavaScript
   - Source: User said "I prefer TS, type safety"
   - Scope: Private
   
2. **[Project Memory]** Choose solution A (Redis cache) due to QPS requirements
   - Source: Architecture discussion, mentioned "3x QPS improvement"
   - Scope: Team
   - Why: Performance requirements
   - How to apply: New APIs should add cache layer

3. **[Reference Memory]** API docs at https://api.example.com/v2
   - Source: User shared link
   - Scope: Team

**❌ Discarded (Temporary States):**
- Bug fix #123 progress (task-specific)
- Intermediate code modification attempts (derivable from codebase)
- Debugging trial-and-error records (solution already implemented)

---
**Actions:**
- `y` or `confirm` - Save above content to memory system
- `n` or `cancel` - Don't save anything
- `edit` - Manually edit what to save
- `show N` - View item N details
```

**Key Design**:
- ✅ Clearly list source of each item
- ✅ Mark scope (private/team)
- ✅ Explain why worth saving
- ✅ User can review item by item
- ✅ Default not saved, requires explicit confirmation

---

### Step 5: Save to Memory System

Save according to user confirmation and type:

```python
def save_to_memory(items, user_confirmed):
    for item in items:
        if not user_confirmed.get(item.id, False):
            continue  # Skip unconfirmed
        
        if item.type == 'user':
            save_user_memory({
                'name': item.name,
                'description': item.description,
                'content': format_user_memory(item)
            })
        
        elif item.type == 'feedback':
            save_feedback_memory({
                'name': item.name,
                'description': item.description,
                'content': f"{item.rule}\n\n**Why:** {item.why}\n\n**How to apply:** {item.how}"
            })
        
        elif item.type == 'project':
            save_project_memory({
                'name': item.name,
                'description': item.description,
                'content': f"{item.fact}\n\n**Why:** {item.why}\n\n**How to apply:** {item.how}"
            })
        
        elif item.type == 'reference':
            save_reference_memory({
                'name': item.name,
                'description': item.description,
                'content': item.location
            })
    
    return f"✅ Successfully saved {count} memories"
```

---

## 🔒 Security & Privacy

### 🚫 Absolutely Forbidden to Save

- 🔐 API keys, passwords, tokens
- 🔐 User personal info (email, phone, address)
- 🔐 Internal system addresses (unless explicitly allowed)
- 🔐 Undisclosed business models or secrets
- 🔐 Third-party confidential information

### 🎯 Scope Control

| Content Type | Scope | Storage Location | Visibility |
|--------------|-------|------------------|------------|
| Personal Preferences | Private | `MEMORY.md` | Main session only |
| User Roles | Private | `MEMORY.md` | Main session only |
| Project Decisions | Team | `MEMORY.md` | Team members |
| External Resources | Team | `MEMORY.md` | Team members |

### ⚠️ Checklist

Before saving, automatically check:
- [ ] No sensitive words (password, secret, key, token)
- [ ] No complete URLs (unless public docs)
- [ ] No file paths (unless public config)
- [ ] Scope marked correctly
- [ ] User explicitly confirmed

---

## 📊 Relationship with Session Isolation

### Design That Doesn't Break Isolation

```
┌─────────────┐              ┌─────────────┐
│  Session A  │              │  Session B  │
│             │              │             │
│ Temp States │              │ Temp States │
│ (bug #123)  │              │ (feature X) │
│    ↓        │              │    ↓        │
│  Discard ❌ │              │  Discard ❌ │
│             │              │             │
│ Long-term   │              │             │
│ Knowledge   │              │             │
│ (preferences)│             │             │
│    ↓        │              │    ↑        │
│  MEMORY.md  ├──────────────┤             │
│             │ Shared Knowledge            │
└─────────────┘              └─────────────┘

Isolated: Temporary states, task context, intermediate processes
Shared: User preferences, project decisions, external resources
```

### Actually Enhances Isolation Value

| Without session-report | With session-report |
|-----------------------|--------------------|
| Everything lost after session ends | Knowledge preserved |
| Re-explain background every time | Future sessions auto-get background |
| Make same mistakes twice | Learn from historical experience |
| Isolation = Isolation | Isolation but interconnected |

---

## 🔄 Integration with Other Skills

### With memory-search

```
/session-report              memory-search
     │                            │
     ▼                            ▼
Write to memory ←──────────→ Retrieve memory
     │                            │
     └──────────────┬─────────────┘
                    │
                    ▼
          Future sessions auto-get context
```

**Synergy**:
- `session-report` responsible for **writing** high-quality memories
- `memory-search` responsible for **reading** relevant memories
- Forms complete memory loop

---

### With self-evolution

```
/session-report              self-evolution
     │                            │
     ▼                            ▼
Extract lessons ←──────────→ Evolve agent behavior
     │                            │
     └──────────────┬─────────────┘
                    │
                    ▼
          Agent increasingly matches user preferences
```

**Synergy**:
- `session-report` discovers patterns ("user always corrects X")
- `self-evolution` adjusts behavior (reduce X behavior)

---

## ⚠️ Common Mistakes & How to Avoid

### ❌ Mistake 1: Save All Conversations

**Wrong**:
```markdown
User: Help me fix this bug
AI: OK, checking...
User: How's it going?
AI: Found it, null pointer...

→ Save all ❌
```

**Right**:
```markdown
Extract from conversation:
- [Project Memory] User service has null pointer risk, add null check ✅
- [Feedback Memory] User wants proactive issue reporting, don't wait for questions ✅

Discard:
- Temporary conversation flow ❌
```

---

### ❌ Mistake 2: Over-summarize

**Wrong**:
```markdown
Save: "User asked 3 questions today: A, B, C"
```

**Problem**: This is session state, not long-term knowledge

**Right**:
```markdown
Save: "User prefers to understand background first before getting solutions" 
(pattern abstracted from 3 questions)
```

---

### ❌ Mistake 3: Don't Distinguish Scope

**Wrong**:
```markdown
Save everything to project memory
```

**Problem**: Personal preferences pollute project space

**Right**:
```markdown
Personal preferences → User Memory (private)
Project conventions → Project Memory (team)
```

---

### ❌ Mistake 4: Skip User Confirmation

**Wrong**:
```python
# Automatically save all content
save_to_memory(extracted_items)  # ❌
```

**Right**:
```python
# Generate preview first
preview = generate_preview(extracted_items)

# User confirmation
if user_confirms(preview):
    save_to_memory(extracted_items)  # ✅
```

---

## 📝 Memory Format Templates

### User Memory Format

```markdown
---
name: User Role & Preferences
type: user
scope: private
---

**Role**: Data scientist, focused on observability/logging domain

**Technical Background**:
- Proficient in Python and SQL
- Familiar with data pipelines and ETL
- Has machine learning project experience

**Communication Preferences**:
- Prefers detailed technical explanations
- Prefers code examples
- Values performance and security considerations

**How to Apply**:
When explaining problems:
- Use data analysis-related analogies
- Emphasize logging and monitoring best practices
- Provide quantifiable results
- Prioritize Python solutions
```

---

### Feedback Memory Format

```markdown
---
name: Tests Must Use Real Database
type: feedback
scope: team
---

Integration tests must hit real database, cannot use mocks.

**Why**: 
Last year mock tests passed but production migration failed, mock/prod divergence masked broken migration.
Specific incident: Q4 release, mocked database tests all passed, but production migration failed due to field type mismatch,
causing 2 hours downtime.

**How to apply**:
- All integration tests must configure real database connection
- Use test database (not production)
- Unit tests can mock
- End-to-end tests must be real environment
- Enable real database in CI/CD configuration
```

---

### Project Memory Format

```markdown
---
name: Mobile Release Freeze
type: project
scope: team
---

Freeze all non-critical merges after 2026-03-05 until mobile release completes.

**Why**: 
Mobile team needs stable codebase for final testing and release preparation.
Any non-critical changes could introduce regression bugs, affecting release schedule.

**How to apply**:
- Mark all new PRs as "on hold" unless critical bug fix
- Inform team members about freeze period
- Unfreeze after release (expected 2026-03-12)
- Emergency fixes require mobile lead approval
```

---

### Reference Memory Format

```markdown
---
name: Linear Project Tracking
type: reference
scope: team
---

Pipeline-related bugs and requirements tracked in Linear project "INGEST".

**URL**: https://linear.app/company/project/INGEST

**Purpose**:
- All pipeline bugs should be created in this project
- Requirements priority managed in this project
- Weekly status updates synced here

**Related Teams**:
- Data platform team (primary maintenance)
- Backend team (collaborators)
```

---

## 🎯 Best Practices

### ✅ Do's

1. **Summarize timely** - Run immediately after session ends, memory fresh
2. **Quality over quantity** - Only save truly valuable content
3. **Clear rationale** - Every memory should have Why and How to apply
4. **Regular review** - Check memories monthly, update or remove outdated ones
5. **User-led** - Let user decide what's worth saving

### ❌ Don'ts

1. **Don't auto-save** - Always require user confirmation
2. **Don't save details** - Save patterns and principles, not specific conversations
3. **Don't duplicate** - Check if similar memory exists first
4. **Don't let become outdated** - Update promptly when project decisions change
5. **Don't save sensitive** - Never save passwords, keys, etc.

---

## 🔧 Troubleshooting

### Problem 1: Cannot Find Session History

**Possible causes**:
- Session expired or cleaned up
- Insufficient permissions to read history

**Solutions**:
```bash
# Check session status
openclaw sessions list

# Manually specify session
/session-report --session <session-id>
```

---

### Problem 2: Too Much Extracted Content

**Possible causes**:
- Session too long, contains大量 temporary conversations
- Filtering rules not strict enough

**Solutions**:
```bash
# Limit number of messages reviewed
/session-report --limit 30

# Focus on specific types
/session-report --type feedback --type project
```

---

### Problem 3: User Unsure Whether to Save

**Suggestions**:
- Use `--dry-run` to preview first
- Review item by item (`show N`)
- Start conservative, can supplement later

---

## 📈 Effectiveness Evaluation

### Short-term (1-2 weeks)

- ✅ Important decisions no longer forgotten
- ✅ Reduce repeated background explanations
- ✅ Users feel understood

### Medium-term (1-2 months)

- ✅ Form project knowledge base
- ✅ New members onboard quickly
- ✅ Same mistakes not made twice

### Long-term (3+ months)

- ✅ Agent behavior highly personalized
- ✅ Team collaboration efficiency improved
- ✅ Knowledge assets continuously accumulated

---

_Last updated: 2026-04-06_  
_Version: 1.0.0_  
_Maintainer: evo-agents Team_
