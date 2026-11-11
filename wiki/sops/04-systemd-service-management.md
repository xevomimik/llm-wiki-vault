# SOP-04: Systemd Service Management

**Version:** 1.0
**Last Updated:** 2026-11-11
**Status:** Active

---

## Purpose
Manage OmniRoute as a systemd user service: start, stop, restart, status, logs, auto-start on boot.

---

## Service Name
`omniroute` (user service — `systemctl --user`)

---

## Service File Location
Typical locations (check with `systemctl --user status omniroute`):
- `~/.config/systemd/user/omniroute.service`
- `/etc/systemd/user/omniroute.service` (if installed system-wide)

---

## Common Commands

### Status
```bash
systemctl --user status omniroute
```

### Start
```bash
systemctl --user start omniroute
```

### Stop
```bash
systemctl --user stop omniroute
```

### Restart (After Config/Key Changes)
```bash
systemctl --user restart omniroute
```

### Reload (Config Changes Only, No Downtime)
```bash
systemctl --user reload omniroute
# Note: OmniRoute may not support SIGHUP reload; restart is safer
```

### Enable Auto-Start on Login
```bash
systemctl --user enable omniroute
```

### Disable Auto-Start
```bash
systemctl --user disable omniroute
```

### Enable Lingering (Run at Boot Without Login)
```bash
loginctl enable-linger $USER
# Required for user services to start at boot
```

---

## Logs

### Follow Live Logs
```bash
journalctl --user -u omniroute -f
```

### Last N Lines
```bash
journalctl --user -u omniroute -n 100
```

### Since Last Boot
```bash
journalctl --user -u omniroute -b
```

### Filter by Priority
```bash
journalctl --user -u omniroute -p err  # errors only
journalctl --user -u omniroute -p warning..crit
```

### Export Logs
```bash
journalctl --user -u omniroute --since "2026-11-01" --until "2026-11-11" > omniroute-logs.txt
```

---

## Health Checks

### Quick Health
```bash
curl -s http://localhost:20128/health
# Expected: {"status":"healthy"} or similar
```

### Full Readiness
```bash
curl -s http://localhost:20128/ready
# Checks: providers loaded, models cataloged, combos configured
```

### Via systemd
```bash
systemctl --user is-active omniroute  # active/inactive/failed
systemctl --user is-enabled omniroute # enabled/disabled
```

---

## Troubleshooting

### Service Won't Start
```bash
# Check logs
journalctl --user -u omniroute -n 50

# Common issues:
# - Port 20128 already in use: `ss -ltnp | grep 20128`
# - Missing .env file: `ls -la ~/.config/omniroute/.env`
# - Invalid config: `omniroute config validate`
# - Permission denied: check ExecStart path in service file
```

### Service Crashes Repeatedly
```bash
# Check crash logs
journalctl --user -u omniroute -p err -n 20

# Check core dumps
coredumpctl list omniroute
```

### Port Conflict
```bash
# Find what's on 20128
ss -ltnp | grep 20128

# Kill if needed
kill -9 <PID>
```

### Config Changes Not Picked Up
```bash
# Always restart after .env or config.yaml changes
systemctl --user restart omniroute
# Reload may not work for all config types
```

---

## Service File Template
If creating/recreating service file:
```ini
# ~/.config/systemd/user/omniroute.service
[Unit]
Description=OmniRoute Inference Router
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/home/xevomimik/.local/bin/omniroute serve --config /home/xevomimik/.config/omniroute/config.yaml
Restart=on-failure
RestartSec=5
EnvironmentFile=-/home/xevomimik/.config/omniroute/.env
WorkingDirectory=/home/xevomimik
StandardOutput=journal
StandardError=journal

# Resource limits
LimitNOFILE=4096
MemoryMax=2G
CPUQuota=200%

[Install]
WantedBy=default.target
```

After creating/editing:
```bash
systemctl --user daemon-reload
systemctl --user restart omniroute
```

---

## Backup Service Config
```bash
# Copy service file to LLM Wiki for version control
cp ~/.config/systemd/user/omniroute.service ~/llm-wiki-vault/wiki/sops/assets/omniroute.service
```

---

## Related SOPs
- SOP-03: Key Rotation & Expiry Handling (requires restart)
- SOP-05: Backup/Restore via GitHub
- SOP-01: Provider Onboarding (requires restart)