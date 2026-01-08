---
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
