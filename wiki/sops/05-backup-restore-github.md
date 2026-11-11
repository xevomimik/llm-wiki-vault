# SOP-05: Backup/Restore via GitHub

**Version:** 1.0
**Last Updated:** 2026-11-11
**Status:** Active

---

## Purpose
Version control all OmniRoute configuration, LLM Wiki, and SOPs in GitHub for disaster recovery and synchronization across machines.

---

## Repositories

### Primary: `xevomimik/omniroute-config`
**Contains:** All OmniRoute config, keys (encrypted), SOPs, systemd service file, wiki snapshots
**Location:** `~/omniroute-config` (to be created)
**Remote:** `git@github.com:xevomimik/omniroute-config.git`

### Secondary: `xevomimik/llm-wiki-vault`
**Contains:** LLM Wiki markdown vault (already exists at `~/llm-wiki-vault`)
**Remote:** `git@github.com:xevomimik/llm-wiki-vault.git` (needs setup)

---

## What to Back Up

### OmniRoute Config (Critical)
```
~/.config/omniroute/
├── config.yaml          # Main config (combos, providers, models)
├── .env                 # ENCRYPTED API keys — MUST be encrypted
├── catalog/             # Model catalog cache (optional, regenerates)
└── logs/                # Optional
```

### LLM Wiki Vault
```
~/llm-wiki-vault/
├── wiki/
│   ├── omniroute/
│   │   └── current_models_and_gaps.md
│   ├── sops/
│   │   ├── 01-provider-onboarding.md
│   │   ├── 02-combo-creation-testing.md
│   │   ├── 03-key-rotation-expiry.md
│   │   ├── 04-systemd-service-management.md
│   │   ├── 05-backup-restore-github.md
│   │   ├── 06-model-testing-protocol.md
│   │   └── (future SOPs)
│   ├── concepts/
│   ├── entities/
│   └── ...
├── scripts/
├── schema/
└── raw/
```

### Systemd Service File
```
~/.config/systemd/user/omniroute.service
```

### Hermes Config
```
~/.hermes/config.yaml
```

---

## Encryption for Secrets

**NEVER commit plaintext API keys to Git.**

### Option 1: SOPS (Recommended)
```bash
# Install
sudo pacman -S sops age

# Generate age key
age-keygen -o ~/.config/sops/age/keys.txt

# Encrypt .env
sops --encrypt --age <public-key> ~/.config/omniroute/.env > omniroute-config/.env.enc

# Decrypt
sops --decrypt omniroute-config/.env.enc > ~/.config/omniroute/.env
```

### Option 2: Git-Crypt
```bash
# Setup once
git-crypt init
# Add .gitattributes: .env filter=git-crypt diff=git-crypt
```

### Option 3: Manual (Current)
Keep `.env` local only. Document key rotation in SOPs. Restore keys manually from password manager.

---

## Backup Procedure (Run Weekly)

### 1. Sync OmniRoute Config to Repo
```bash
cd ~/omniroute-config

# Copy current config (excluding plaintext .env)
rsync -av ~/.config/omniroute/config.yaml .
rsync -av ~/.config/omniroute/catalog/ catalog/ 2>/dev/null || true
cp ~/.config/systemd/user/omniroute.service .

# Encrypt .env if using SOPS
sops --encrypt --age <pubkey> ~/.config/omniroute/.env > .env.enc

# Copy Hermes config
cp ~/.hermes/config.yaml hermes-config.yaml
```

### 2. Commit & Push
```bash
git add -A
git commit -m "backup: $(date +%Y-%m-%d) OmniRoute config + Hermes + systemd"
git push origin main
```

### 3. Push LLM Wiki Vault
```bash
cd ~/llm-wiki-vault
git add -A
git commit -m "wiki: $(date +%Y-%m-%d) SOPs + model updates"
git push origin main
```

---

## Restore Procedure (New Machine / Disaster)

### Prerequisites
- GitHub SSH key configured
- `age` key for SOPS decryption (if used)
- OmniRoute installed

### 1. Clone Repos
```bash
git clone git@github.com:xevomimik/omniroute-config.git ~/omniroute-config
git clone git@github.com:xevomimik/llm-wiki-vault.git ~/llm-wiki-vault
```

### 2. Restore OmniRoute Config
```bash
mkdir -p ~/.config/omniroute

# Config
cp ~/omniroute-config/config.yaml ~/.config/omniroute/

# Decrypt keys
sops --decrypt ~/omniroute-config/.env.enc > ~/.config/omniroute/.env
chmod 600 ~/.config/omniroute/.env

# Systemd
mkdir -p ~/.config/systemd/user
cp ~/omniroute-config/omniroute.service ~/.config/systemd/user/
systemctl --user daemon-reload
```

### 3. Restore Hermes Config
```bash
cp ~/omniroute-config/hermes-config.yaml ~/.hermes/config.yaml
```

### 4. Enable & Start
```bash
systemctl --user enable omniroute
systemctl --user start omniroute
loginctl enable-linger $USER  # for boot start
```

### 5. Verify
```bash
curl -s http://localhost:20128/health
# Test each combo
for combo in FLAGSHIP ROUND-ROBIN NVIDIA GOOGLE OPENROUTER CEREBRAS CODING VISION-MULTIMODAL "PS5LM PLUS"; do
  echo "Testing $combo..."
  curl -s -X POST http://localhost:20128/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d "{\"model\": \"$combo\", \"messages\": [{\"role\": \"user\", \"content\": \"hello\"}], \"max_tokens\": 10}"
done
```

---

## GitHub Repository Setup (One-Time)

### Create `omniroute-config` Repo
```bash
cd ~/omniroute-config
git init
git remote add origin git@github.com:xevomimik/omniroute-config.git
# Add .gitignore for .env (plaintext), logs, catalog
echo ".env" > .gitignore
echo "logs/" >> .gitignore
echo "catalog/" >> .gitignore
git add .gitignore
git commit -m "init: repo structure"
git push -u origin main
```

### Connect Existing `llm-wiki-vault`
```bash
cd ~/llm-wiki-vault
git remote add origin git@github.com:xevomimik/llm-wiki-vault.git
git push -u origin main
```

---

## Automation (Optional)
Add cron job for weekly backup:
```bash
# ~/.config/cron/weekly-backup.sh
#!/bin/bash
cd ~/omniroute-config && ./backup.sh
cd ~/llm-wiki-vault && ./backup.sh
```

---

## Related SOPs
- SOP-03: Key Rotation & Expiry Handling (triggers backup)
- SOP-04: Systemd Service Management (restore includes service)
- SOP-01: Provider Onboarding (update config after)