#!/usr/bin/env python3
"""
ios-simulator-skill registration tool.

Registers the iOS Simulator Skill with AI development platforms:
- Claude Code: Creates .claude/skills/ios-sim/ with SKILL.md
- Antigravity: Creates .antigravity/workflows/ios-simulator-skill.md
- Manual: Outputs markdown for copy-paste into chat interfaces

Usage:
    ios-sim --register code    # Claude Code skill
    ios-sim --register agent   # Antigravity workflow
    ios-sim --register help    # Show this documentation
    ios-sim --register         # Manual copy-paste output
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def get_skill_dir() -> Path:
    """Get the skill directory (where SKILL.md lives)."""
    # This script is in skill/scripts/, so skill/ is parent
    return Path(__file__).parent.parent


def get_skill_content() -> str:
    """Read SKILL.md content."""
    skill_file = get_skill_dir() / "SKILL.md"
    if skill_file.exists():
        return skill_file.read_text()
    return ""


def get_claude_content() -> str:
    """Read CLAUDE.md content."""
    # Check both locations
    for path in [get_skill_dir() / "CLAUDE.md", get_skill_dir().parent / "CLAUDE.md"]:
        if path.exists():
            return path.read_text()
    return ""


def generate_antigravity_workflow() -> str:
    """Generate Antigravity workflow content."""
    return '''---
description: Build, test, and automate iOS apps with semantic navigation. Use when asked about iOS simulators, Xcode builds, accessibility testing, or app automation.
---

# iOS Simulator Skill

Production-ready automation for iOS app testing and building. 21 scripts optimized for AI agents.

---

## ⚡ Quick Start

```bash
# 1. Check environment
bash scripts/sim_health_check.sh

# 2. Launch app
python scripts/app_launcher.py --launch com.example.app

# 3. Map screen to see elements
python scripts/screen_mapper.py

# 4. Tap button by text
python scripts/navigator.py --find-text "Login" --tap

# 5. Enter text
python scripts/navigator.py --find-type TextField --enter-text "user@example.com"
```

---

## Script Categories

### Build & Development
| Script | Description |
|--------|-------------|
| `build_and_test.py` | Build Xcode projects, run tests, parse results |
| `log_monitor.py` | Real-time log monitoring with filtering |

### Navigation & Interaction
| Script | Description |
|--------|-------------|
| `screen_mapper.py` | Analyze current screen elements |
| `navigator.py` | Find and interact with elements semantically |
| `gesture.py` | Swipes, scrolls, pinches, long press |
| `keyboard.py` | Text input and hardware buttons |
| `app_launcher.py` | App lifecycle (launch, terminate, install) |

### Testing & Analysis
| Script | Description |
|--------|-------------|
| `accessibility_audit.py` | WCAG compliance checking |
| `visual_diff.py` | Screenshot comparison |
| `test_recorder.py` | Automated test documentation |
| `app_state_capture.py` | Debugging snapshots |
| `sim_health_check.sh` | Environment verification |

### Advanced Testing & Permissions
| Script | Description |
|--------|-------------|
| `clipboard.py` | Clipboard management |
| `status_bar.py` | Override status bar appearance |
| `push_notification.py` | Send test push notifications |
| `privacy_manager.py` | Grant/revoke app permissions |

### Device Lifecycle
| Script | Description |
|--------|-------------|
| `simctl_boot.py` | Boot simulators |
| `simctl_shutdown.py` | Shutdown simulators |
| `simctl_create.py` | Create new simulators |
| `simctl_delete.py` | Delete simulators |
| `simctl_erase.py` | Factory reset simulators |

---

## Common Patterns

**Auto-UDID Detection**: Scripts auto-detect the booted simulator if `--udid` not provided.

**Device Name Resolution**: Use names like "iPhone 16 Pro" instead of UDIDs.

**Batch Operations**: Many scripts support `--all` or `--type iPhone` for bulk operations.

**Output Formats**:
- Default: Concise human-readable (3-5 lines)
- `--verbose`: Detailed output
- `--json`: Machine-readable for CI/CD

---

## Examples for AI Agents

### Login Flow Test

```bash
# Launch app
python scripts/app_launcher.py --launch com.example.app

# Map screen to find fields
python scripts/screen_mapper.py

# Enter email
python scripts/navigator.py --find-type TextField --index 0 --enter-text "user@test.com"

# Enter password
python scripts/navigator.py --find-type SecureTextField --enter-text "password123"

# Tap login button
python scripts/navigator.py --find-text "Login" --tap

# Verify accessibility compliance
python scripts/accessibility_audit.py
```

### Permission Testing

```bash
# Grant camera and location permissions
python scripts/privacy_manager.py --bundle-id com.example.app --grant camera,location

# Test app behavior...

# Revoke permissions
python scripts/privacy_manager.py --bundle-id com.example.app --revoke camera,location
```

### CI/CD Device Lifecycle

```bash
# Create test device
DEVICE_ID=$(python scripts/simctl_create.py --device "iPhone 16 Pro" --json | jq -r '.new_udid')

# Run tests
python scripts/build_and_test.py --project MyApp.xcodeproj --test

# Clean up
python scripts/simctl_delete.py --udid $DEVICE_ID --yes
```

---

## Safe Commands (Read-Only)

// turbo
The following commands are safe to auto-execute:

```bash
# List simulators
python scripts/simctl_boot.py --list

# Health check
bash scripts/sim_health_check.sh

# Screen analysis (no interaction)
python scripts/screen_mapper.py

# Accessibility audit
python scripts/accessibility_audit.py

# App state capture
python scripts/app_state_capture.py --app-bundle-id com.example.app
```

---

## Requirements

- macOS 12+
- Xcode Command Line Tools
- Python 3
- IDB (optional, for interactive features)

---

## Registration

```bash
ios-sim --register agent   # Antigravity/Gemini
ios-sim --register code    # Claude Code
ios-sim --register help    # Show documentation
ios-sim --register         # Manual copy-paste
```
'''


def generate_help_text() -> str:
    """Generate help documentation."""
    return '''ios-simulator-skill - Self-Registration Guide

Register this skill with AI development platforms:

1. **Claude Code**: Run `ios-sim --register code`
   - Creates `.claude/skills/ios-sim/` with SKILL.md and CLAUDE.md
   - Skill loads automatically after restart

2. **Antigravity/Gemini**: Run `ios-sim --register agent`
   - Creates `.agent/workflows/ios-simulator-skill.md`
   - Workflow becomes available immediately

3. **Manual/Chat**: Run `ios-sim --register`
   - Outputs markdown to copy-paste into chat interfaces

After registration, the skill is available for iOS automation tasks.

Requirements:
- macOS 12+
- Xcode Command Line Tools
- Python 3
- IDB (optional, for interactive features)
'''


def register_claude_code(target_dir: Path) -> bool:
    """Register as Claude Code skill."""
    skill_dir = target_dir / ".claude" / "skills" / "ios-sim"
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Copy SKILL.md
    skill_content = get_skill_content()
    if skill_content:
        (skill_dir / "SKILL.md").write_text(skill_content)
        print(f"✓ Created: {skill_dir / 'SKILL.md'}")
    else:
        print("⚠ Warning: SKILL.md not found")

    # Copy CLAUDE.md
    claude_content = get_claude_content()
    if claude_content:
        (skill_dir / "CLAUDE.md").write_text(claude_content)
        print(f"✓ Created: {skill_dir / 'CLAUDE.md'}")

    # Copy scripts directory
    scripts_src = get_skill_dir() / "scripts"
    scripts_dst = skill_dir / "scripts"
    if scripts_src.exists():
        if scripts_dst.exists():
            shutil.rmtree(scripts_dst)
        shutil.copytree(scripts_src, scripts_dst)
        print(f"✓ Copied: {scripts_dst}")

    print(f"\nClaude Code skill registered at: {skill_dir}")
    print("Restart Claude Code to load the skill.")
    return True


def register_antigravity(target_dir: Path) -> bool:
    """Register as Antigravity workflow."""
    workflow_dir = target_dir / ".agent" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)

    workflow_file = workflow_dir / "ios-simulator-skill.md"
    workflow_file.write_text(generate_antigravity_workflow())

    print(f"✓ Created workflow: {workflow_file}")
    print("✓ Added to auto-execute allowlist")
    return True


def main() -> None:
    """Main entry point for registration CLI."""
    parser = argparse.ArgumentParser(
        description="iOS Simulator Skill - Registration Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ios-sim --register code    # Register with Claude Code
  ios-sim --register agent   # Register with Antigravity
  ios-sim --register help    # Show documentation
  ios-sim --register         # Output for manual copy-paste
        """,
    )

    parser.add_argument(
        "--register",
        nargs="?",
        const="none",
        choices=["none", "code", "agent", "help", "mcp"],
        metavar="PLATFORM",
        help="Register with AI platform: code (Claude), agent (Antigravity), help (docs), mcp (coming soon)",
    )

    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help="Target directory for registration (default: current directory)",
    )

    args = parser.parse_args()

    if args.register is None:
        parser.print_help()
        sys.exit(0)

    if args.register == "help":
        print(generate_help_text())
        sys.exit(0)

    if args.register == "code":
        success = register_claude_code(args.target)
        sys.exit(0 if success else 1)

    if args.register == "agent":
        success = register_antigravity(args.target)
        sys.exit(0 if success else 1)

    if args.register == "mcp":
        print("MCP server registration coming soon.")
        print("For now, use --register code or --register agent")
        sys.exit(0)

    if args.register == "none":
        # Output for manual copy-paste
        print(generate_antigravity_workflow())
        sys.exit(0)


if __name__ == "__main__":
    main()
