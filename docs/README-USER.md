# Hardware Division OS — Guide for non-coders

> You're a one-person business owner (freelancer / shop owner / online store / solo startup).
> You want **13 AI departments** (Legal, Finance, Marketing, Operations, People, ...) to meet and decide and draft documents for you.
> You **don't need to know how to code**. This guide is step by step, copy-paste, anyone can do it.

---

## 🎯 What does this repo do? (Read before installing)

This is an **AI Operating System** for a US division. You chat naturally in Claude Desktop; the system convenes 13 AI departments to meet → generate `.docx`/`.xlsx` documents aligned with US federal + Texas law.

> General information only — the legal/tax content is not legal or tax advice. Confirm with a licensed Texas attorney and CPA.

### The 5 most common use cases

| # | You chat | Output | Time |
|---|---|---|---|
| 1 | "Draft a JD for a barista at $18/hr, Q1" | A full JD: pay, payroll taxes (FICA), job description, requirements, application process | ~30s |
| 2 | "Draft an offer for a store manager at $55k/year, F&B, 1 year exp" | An offer letter: at-will, exempt/non-exempt, FICA, PTO + standard terms (general info, not legal advice) | ~30s |
| 3 | "Plan June marketing, $700 budget, grow revenue from $7,800 → $9,000" | A 6-department debate (Marketing + Finance + Ops + Sales + Customer + Kitchen) → a 250-line decision report: cut the budget $700→$250, week-1 blockers, KPI gates, action items with deadlines | ~3 min |
| 4 | "Analyze whether to open location 2 in Q1 or Q3" | A 5-department debate → a report with CAPEX, payback period, legal risk, 3 options Growth/Cautious/Balanced | ~5 min |
| 5 | "Draft workplace rules for a cafe" | Full work rules: pay, shifts, discipline, uniform, bonus, at-will | ~30s |

### How it differs from a normal ChatGPT chat

| Aspect | Normal ChatGPT / Claude | This repo (bd-business-os) |
|---|---|---|
| Company context | Paste it again every time | Read from the **Brain** (`vault/00-Brain/`) automatically |
| Big decisions | One AI viewpoint | **Multi-department debate** (Pro/Con + 3 perspectives Growth/Cautious/Balanced) |
| US compliance | General knowledge | Hardware-division grounding: FCC Part 15, UL/IEC safety, PCI PTS/EMVCo, customs/HTS, Magnuson-Moss warranty, Texas franchise tax |
| Output | Text in chat | `.docx`/`.xlsx` files + stored in Obsidian + Git auto-commit |
| Citations | Made up | A **citation validator** flags claims missing a source at the end of the report |
| Department Head approval | None | **2 Stops** (after the decision report + after the execution plan) |

→ **You stay the division manager. The departments do the staff work.** (For actual legal/tax/certification decisions, confirm with a licensed Texas attorney, CPA, customs broker, and the labs.)

---

## 🧭 What stage are you at?

Depending on your current state, follow the matching path:

| You are... | Follow path |
|---|---|
| **🆕 Nothing installed** (no Obsidian, Python, Claude Desktop) | **Path A**: do all of PART 1 (Steps 1-9) |
| **🟡 Obsidian + MCP-Obsidian already set up from a prior class** (existing vault, Local REST API enabled, already chatting with Claude via MCP-Obsidian) | **Path B**: skip Step 3, do Steps 1-2 + Steps 4-9 (install Python + repo + DeepSeek + add the `bd-business-os` MCP to the Claude Desktop config) |
| **🟢 Repo + vault for company 1 already there, now want a 2nd company** | **Path C**: only do PART 2 (create a new vault, apply a pack, fill the Brain) — no need to reinstall Python/repo |

**Path B details** (most common — students already have Obsidian):

```
✅ Already have: Obsidian + Local REST API plugin + existing vault + MCP-Obsidian in claude_desktop_config.json
🆕 Need to add:
  - Step 1: Python 3.11+ (if not present)
  - Step 2: Node.js 20+ (if not present)
  - Step 4: Clone the `bd-business-os` repo into `F:\.work\`
  - Step 5: pip install -e .
  - Step 6: DeepSeek API key
  - Step 6.5: Tavily API key
  - Step 7: Create .env in the vault + .vncoderc in $HOME
  - Step 8.2: Add the "bd-business-os" entry to claude_desktop_config.json (do NOT remove the old "mcp-obsidian" entry)
  - Step 8.3: Quit Claude Desktop from the tray + restart
```

---

## 📋 What to prepare before installing

### Hardware + time
- [ ] A Windows 10 or 11 PC (Mac/Linux also work, but this guide focuses on Windows)
- [ ] About **45 minutes** free to install
- [ ] A stable internet connection

### Accounts (free sign-up)
- [ ] An **Anthropic Claude Pro** account (~$20/month) — sign up at https://claude.ai
- [ ] A **DeepSeek** account (free, $5 credit on new sign-up — enough for hundreds of tasks)
- [ ] **Tavily** (free tier 1000 searches/month — RECOMMENDED, so the AI can look up law/competitors on the web)

### Software you'll install (in this guide)
- Python 3.11+
- Node.js 18+
- Obsidian (notes + storage — the company's "memory")
- Claude Desktop (chat with the AI — you'll use the **"</> Code"** tab inside it)

> 🎯 **Important note:** Claude Desktop has 3 tabs: **Chat** | **Cowork** | **</> Code**.
> The US OS system is designed to run in the **Code** tab (10-minute timeout, can call any MCP tool).
> The Cowork tab (60s timeout) only handles light tasks. The Chat tab has no MCP.

> 💡 **Don't worry if you don't know what these are.** Each step has a download link + the exact actions.

---

## 🚀 PART 1 — INSTALL (one time, ~45 min)

> ⚠️ **Before you start:** make sure you have admin rights on the machine (to install software). If it's a locked company PC — contact IT.

---

### Step 1: Install Python (10 min)

Python is the language that runs the system's "engine." You don't program in Python; you just install it so the program can run.

**Actions:**

1. Open a browser → go to https://www.python.org/downloads/
2. Click **"Download Python 3.12.x"** (or 3.11+ — do not install Python 3.10 or lower)
3. Open the downloaded file (e.g. `python-3.12.x-amd64.exe`)
4. **VERY IMPORTANT:** check **"Add python.exe to PATH"** at the bottom of the install window
5. Click **"Install Now"**
6. Wait 2-3 minutes until you see "Setup was successful"
7. Click **Close**

**Verify it installed:**

1. Press **`Windows + R`** → type `powershell` → Enter
2. In the dark-blue PowerShell window, type:
   ```
   python --version
   ```
3. Press Enter. It must show: `Python 3.12.x` (or 3.11.x)

❌ If it shows "command not found" → Python isn't on PATH. Reinstall at step 4, making sure "Add to PATH" is checked.

---

### Step 2: Install Node.js (5 min)

Node.js runs MCP (how Claude connects to other tools).

**Actions:**

1. Go to https://nodejs.org
2. Click the **"LTS"** button (Long Term Support — the stable version)
3. Open the downloaded file (e.g. `node-v20.x.x-x64.msi`)
4. Click **Next** → **Next** → ... → **Install** (accept all defaults)
5. Wait for it to finish → **Finish**

**Verify:**

In PowerShell (open a new one):
```
node --version
```
It must show: `v20.x.x` or higher.

---

### Step 3: Install Obsidian + the Local REST API plugin (8 min)

Obsidian is a note-taking app. The system uses Obsidian as its "memory" to store all of the company's decisions + documents.

**3.1 — Download and install Obsidian:**

1. Go to https://obsidian.md → click **"Download"**
2. Choose the **Windows installer** (or 64-bit ZIP)
3. Open the file → install with defaults → Open Obsidian

**3.2 — Create a vault (note store) for the company:**

1. On first launch, click **"Create new vault"**
2. **Vault name:** your company's name, e.g. `Lone Star Coffee`, `My Cafe`, `Acme Co`
3. **Location:** pick a large drive, e.g. `F:\vaults` (create this folder if it doesn't exist)
4. Click **Create**

→ Obsidian opens an empty vault. The vault path will be `F:\vaults\<name>` (e.g. `F:\vaults\LoneStarCoffee`)

**3.3 — Enable community plugins:**

1. Click the ⚙️ Settings icon (bottom-left of Obsidian)
2. On the left: choose **"Community plugins"**
3. Click **"Turn on community plugins"** → click **"Turn on"** to confirm

**3.4 — Install the "Local REST API" plugin:**

1. Still on the Community plugins tab → click **"Browse"**
2. In the search box, type: `Local REST API`
3. Click the **"Local REST API"** plugin (author: coddingtonbear)
4. Click **"Install"**
5. After it installs → click **"Enable"**
6. Click **"Options"** (gear icon to the right of the plugin)

**3.5 — Get the plugin's API key:**

1. In the Local REST API plugin settings, find the **"API Key"** line
2. You'll see a long auto-generated string, e.g. `0e957bd6...`
3. **Copy this string** → paste into Notepad → save temporarily to `F:\setup-keys.txt` (delete later)
4. Make sure the plugin is **Enabled** (green toggle)

> ⚠️ **Security warning:** this API key lets anything read/write/delete your entire vault. **Don't share it.** Don't paste it into an AI chat or a public forum.

---

### Step 4: Download the Hardware Division OS repo (5 min)

This is the system's "engine" — it contains the code for 13 departments + 192 templates.

> 🚨 **CHOOSING THE FOLDER IS VERY IMPORTANT** — putting the repo in the wrong place causes 3 big problems:
>
> | ❌ ABSOLUTELY avoid | ✅ Recommended |
> |---|---|
> | `C:\Users\Admin\OneDrive\...` | `F:\.work\` |
> | `C:\Users\Admin\Google Drive\...` | `D:\code\` |
> | `C:\Users\Admin\Documents\...` (if Documents is OneDrive-synced) | `E:\dev\` |
> | A path with **spaces** (e.g. `My Projects`) | A path with **no spaces**, **no non-ASCII characters** |
>
> **Why:**
> - **OneDrive/GDrive sync** will randomly rename/move Python files → editable pip install breaks, `__pycache__` corrupts.
> - **Spaces in the path** → some Python tools parse it wrong, hard-to-debug errors.
> - **Non-ASCII characters in the path** → UTF-8 encoding issues in Windows PowerShell.

**Actions:**

1. **Create a root folder** for all your code projects (if you don't have one):
   ```powershell
   New-Item -ItemType Directory -Force -Path "F:\.work" | Out-Null
   ```
   (Change `F:` to your largest drive — it doesn't have to be F:)

2. Go to https://github.com/andyluu98/bd-business-os

3. Click the green **"Code"** button → **"Download ZIP"**

4. **Extract the ZIP into the root folder**, e.g. `F:\.work\` → you'll get `F:\.work\bd-business-os\`

5. **Verify** the final path (this matters — check that `README.md` is DIRECTLY inside the folder):
   ```powershell
   Test-Path "F:\.work\bd-business-os\README.md"
   ```
   → Must return `True`.

   ❌ If `False` → you may have a double-nested extract (`F:\.work\bd-business-os\bd-business-os-main\README.md`). Delete the outer folder, move the inner one up one level.

> 💡 **Tip for git users:** `cd "F:\.work" && git clone https://github.com/andyluu98/bd-business-os.git` — easier to update later.

---

### Step 5: Install the Python libraries for the repo (5 min)

**Actions:**

1. Open PowerShell (Windows + R → `powershell` → Enter)
2. Go to the repo folder:
   ```powershell
   cd "F:\.work\bd-business-os"
   ```
3. Create a Python virtual environment:
   ```powershell
   python -m venv .venv
   ```
   (Wait 30 seconds)
4. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   - If you get an "execution policy" error, run once:
     ```powershell
     Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
     ```
     (Answer `Y` when asked). Then re-run the activate command.
   - When it works, the prompt has `(.venv)` at the start.
5. **(Important if you installed an old version before)** Uninstall the old one first:
   ```powershell
   pip uninstall bd-business-os bd-business-os -y
   ```
   (If it says "not found" — skip, you haven't installed any.)

6. Install the libraries:
   ```powershell
   pip install -e .
   ```
   (Wait 3-5 minutes — you'll see many install lines)

7. Verify the install:
   ```powershell
   bd-os --version
   ```
   Must show: `bd-os, version 0.2.0` (or higher).

8. **Verify the install points to the right repo folder** (avoids "my code edits do nothing" later):
   ```powershell
   python -c "import json; from pathlib import Path; p = Path([d for d in __import__('site').getsitepackages() + [__import__('site').getusersitepackages()] if (Path(d) / 'bd_business_os-0.2.0.dist-info').exists()][0]) / 'bd_business_os-0.2.0.dist-info' / 'direct_url.json'; print(json.loads(p.read_text())['url'])"
   ```
   Must show: `file:///F:/.work/bd-business-os` (the repo path you extracted).

   ❌ If it shows another path (e.g. `file:///F:/OneDrive/.../bd-business-os`) → you still have an old install. Go back to step 5, uninstall, reinstall.

---

### Step 6: Sign up for DeepSeek + get the API key (5 min)

DeepSeek is an AI service that lets the departments "think." ~10x cheaper than the Claude API, with enough free credit for hundreds of tasks.

**Actions:**

1. Go to https://platform.deepseek.com → click **"Sign up"**
2. Sign up with email or Google
3. After logging in → go to **"API Keys"** (left menu)
4. Click **"Create new API key"** → name it e.g. `bd-business-os`
5. **COPY THE KEY NOW** (shown only once) → paste into `F:\setup-keys.txt` with the Obsidian key
6. The key looks like `sk-xxxxxxxxxxxxxxxxxxxx`

> ⚠️ **Security:** this key lets anyone spend money on DeepSeek. **Don't share it.** If it leaks → go back to API Keys → Delete the old key → create a new one.

> 💰 **Real cost:** DeepSeek's $5 free credit is enough for ~200-300 tasks. After that, top up about $5-10/month for an average company's usage.

---

### Step 6.5: Sign up for Tavily (recommended — 3 min)

Tavily is a search engine for the departments to look up **new laws**, **competitors**, and **local data** live on the web. **Without Tavily** → the decision report still comes out but relies only on the Brain + the LLM's training knowledge (which may be outdated).

**Actions:**

1. Go to https://app.tavily.com → click **"Sign up"** (free, email/Google)
2. After logging in → choose **"API Keys"** on the left
3. Click **"Generate API Key"** → name it e.g. `bd-business-os`
4. Copy the key (looks like `tvly-xxxxxxxxxxxxxxxxxxxxxxxxx`) → paste into `F:\setup-keys.txt` with the others

**Free tier:** 1000 searches/month. Enough for one company running the full pipeline ~50-80 tasks/month (each task uses 5-15 searches).

> 💡 **You can skip this for a quick test.** You can still run the full pipeline, but the 4 research tools (`web_search`, `us_law_search`, `us_local_regulation`, `competitor_research`) will be skipped. You can add the key anytime → edit `.env` → restart Claude Desktop.

---

### Step 7: Create the config files (5 min)

Two small files that tell the system where your company is + which AI to use.

**7.1 — The `.env` file in the vault:**

> 🚨 **VERY IMPORTANT:** `DEEPSEEK_API_KEY` is the main LLM provider. Without it → every `bd_draft`/`bd_run`/`bd_meeting` task errors with `Method not found` (because the code falls back to MCP sampling, which the Claude Code tab doesn't support).

In PowerShell, type (change `LoneStarCoffee` to your vault name):

```powershell
notepad "F:\vaults\LoneStarCoffee\.env"
```

Notepad opens an empty file. Paste:

```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxxx
```

→ Replace both keys with your real keys (from `F:\setup-keys.txt`).

→ If you don't have a Tavily key yet → leave it blank after the `=` (still runs, just skips the 4 research tools).

→ **Save** (Ctrl+S) → **Close**

**Verify .env loads correctly:**

```powershell
Get-Content "F:\vaults\LoneStarCoffee\.env"
```

→ You should see 2 key lines (no BOM, no trailing spaces).

**7.2 — The `.vncoderc` file in your home folder:**

In PowerShell, paste this whole block (everything from `@"` to `"@`):

```powershell
@"
llm:
  primary: deepseek-v4-pro
  secondary: deepseek-v4-flash
  max_retries: 3
  max_tokens_per_task: 100000

meeting:
  max_debate_rounds: 1
  total_max: 3

translator_mode: final_only
"@ | Out-File -FilePath "$HOME\.vncoderc" -Encoding utf8
```

Press Enter. No output — that means it worked.

---

### Step 8: Install Claude Desktop + the 2 MCP servers (5 min)

Claude Desktop is the AI chat app — where you say "draft an employment offer", "analyze a location"...

> 🎯 **IMPORTANT — Use the "Code" tab, not the "Chat" or "Cowork" tab.**
> Claude Desktop has 3 tabs: **Chat** | **Cowork** | **</> Code** (top-right).
> - **Code tab** = Claude Code, 10-minute timeout, can call **any MCP tool** (including a 2-3 minute multi-department debate).
> - **Cowork tab** = 60-second timeout — only light tools (bd_status, read/edit files). Heavy tasks (drafting docs, debate) will **fail**.
>
> → **After installing, always click the "</> Code" tab before chatting.**

**8.1 — Install Claude Desktop:**

1. Go to https://claude.ai/download → download Claude Desktop for Windows
2. Install → log in with your Claude Pro account
3. Open Claude Desktop → **click the "</> Code" tab** in the top-right (next to Chat / Cowork)

**8.2 — Install 2 MCP servers into Claude Desktop:**

> 🟡 **Students who already have MCP-Obsidian from before:** just **ADD** the `bd-business-os` entry to the existing config, **do NOT remove** the old `mcp-obsidian-*` entry.
> Open the config file:
> ```powershell
> notepad "$env:APPDATA\Claude\claude_desktop_config.json"
> ```
> In `mcpServers: { ... }`, add a new entry after the comma of the last entry:
> ```json
> "bd-business-os": {
>   "command": "F:\\.work\\bd-business-os\\.venv\\Scripts\\bd-os-mcp.exe"
> }
> ```
> → Skip the "Replace the whole content" part below.

**🆕 First-time install:** open PowerShell, paste:

```powershell
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"

# Create the config file if missing
if (!(Test-Path $configPath)) {
    New-Item -Path $configPath -ItemType File -Force | Out-Null
    '{"mcpServers": {}}' | Out-File -FilePath $configPath -Encoding utf8
}

# Open the config in Notepad
notepad $configPath
```

Notepad opens `claude_desktop_config.json`. **Replace the whole content** with:

```json
{
  "mcpServers": {
    "mcp-obsidian": {
      "command": "npx",
      "args": ["-y", "mcp-obsidian"],
      "env": {
        "OBSIDIAN_API_KEY": "PASTE_OBSIDIAN_KEY_HERE",
        "OBSIDIAN_HOST": "127.0.0.1",
        "OBSIDIAN_PORT": "27124"
      }
    },
    "bd-business-os": {
      "command": "F:\\.work\\bd-business-os\\.venv\\Scripts\\bd-os-mcp.exe",
      "args": []
    }
  }
}
```

→ Replace `PASTE_OBSIDIAN_KEY_HERE` with the Obsidian Local REST API key (from Step 3.5)

→ Save (Ctrl+S) → Close

**8.3 — Restart Claude Desktop THE RIGHT WAY:**

> ⚠️ **BIG WARNING:** clicking the X (close window) does **NOT quit** Claude Desktop — it only minimizes to the **system tray** (bottom-right). The old MCP server keeps running in the background → every code/config edit has no effect.

**The proper way to Quit:**

1. Look at the **bottom-right of the screen**, near the clock
2. Click the `^` "Show hidden icons" arrow (if needed)
3. Find the **Claude** icon (an orange flower)
4. **Right-click** the Claude icon → choose **"Quit"** (NOT Close)

**Verify everything quit (PowerShell):**

```powershell
Get-Process claude, bd-os-mcp -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count
```

→ Must print `0`. If > 0 → processes remain. Force kill:
```powershell
Get-Process claude, bd-os-mcp -ErrorAction SilentlyContinue | Stop-Process -Force
```

**Reopen Claude Desktop:**

1. Open Claude Desktop from the Start Menu
2. **Click the "</> Code" tab** in the top-right (next to Chat / Cowork)
3. **Important:** the Obsidian app must also be running (your vault open). If not → open Obsidian.

---

### Step 9: Verify everything works (3 min)

> Open Claude Desktop → **click the "</> Code" tab** → **"+ New session"** in the left sidebar → a new chat window appears.

**9.1 — Test MCP Obsidian:**

In the Claude Code session, type:

```
List the files in my Obsidian vault
```

→ Claude must call the `obsidian_list_files_in_vault` tool and return a list. If it works → **Obsidian MCP OK**.

❌ If you get `connection refused` → Obsidian isn't open or the Local REST API plugin is off. Recheck Step 3.

**9.2 — Test MCP bd-business-os:**

In the Claude Code session, type:

```
Run bd_status with vault F:\vaults\LoneStarCoffee
```

→ Claude calls the `bd_status` tool. The first time it'll say `Brain dir not found` — that's normal, the vault isn't initialized yet. But it means the MCP connected.

❌ If you get `Method not found` → the bd-business-os MCP didn't load. Restart Claude Desktop.

---

### ✅ Install done!

By now you have:

| Component | Status |
|---|---|
| Python 3.12 + Node.js 20 | ✅ |
| Obsidian + Local REST API plugin | ✅ |
| The bd-business-os repo + Python libraries | ✅ |
| DeepSeek API key in `.env` | ✅ |
| Tavily API key in `.env` (recommended) | ✅ |
| `.vncoderc` config for the model | ✅ |
| Claude Desktop + 2 MCP servers | ✅ |
| Know to use the **"</> Code"** tab in Claude Desktop | ✅ |

**Next:** Part 2 — Initialize the company (create the Brain + apply an industry pack).

---

## 🏢 PART 2 — INITIALIZE THE COMPANY (one time per company, ~30 min)

> This step creates the company's "brain" — 8 info files (strategy, products, budget, headcount, law, decision log, state, glossary) and the 13-department structure.
>
> After this, every time you chat with Claude, **the AI already knows who your company is and what stage it's at** — no re-entering context each time.

---

### Step 10: Create the Obsidian vault structure (5 min)

The Obsidian vault needs 5 main folders:

```
F:\vaults\<Company>\
├── 00-Brain/              ← 8 company info files (the AI reads these before each task)
├── 00-Templates-Custom/   ← Your own templates (optional)
├── 01-Departments/        ← 13 core departments + industry pack
├── 02-Tasks/              ← History of every task the Department Head assigned
├── 03-Outputs/            ← The generated .docx/.xlsx files
└── 99-Archive/            ← Archived old tasks
```

**Method 1 — Automatic (recommended):**

In a **Claude Code session** (the "</> Code" tab of Claude Desktop, after setting up MCP in Step 8), type:

```
Initialize a Hardware Division vault structure at F:\vaults\<Division>.
```

→ Claude calls the `bd_onboard` tool to auto-create the folders + copy templates.

**Method 2 — Manual (if Method 1 fails):**

1. Open **PowerShell** (Win+R → `powershell`)
2. Paste (change `LoneStarCoffee` to your vault name):

```powershell
$vault = "F:\vaults\LoneStarCoffee"
$repo = "F:\.work\bd-business-os"

# Create the 5 main folders
New-Item -ItemType Directory -Force -Path "$vault\00-Brain" | Out-Null
New-Item -ItemType Directory -Force -Path "$vault\00-Templates-Custom" | Out-Null
New-Item -ItemType Directory -Force -Path "$vault\01-Departments" | Out-Null
New-Item -ItemType Directory -Force -Path "$vault\02-Tasks" | Out-Null
New-Item -ItemType Directory -Force -Path "$vault\03-Outputs" | Out-Null
New-Item -ItemType Directory -Force -Path "$vault\99-Archive" | Out-Null

# Copy the 8 Brain template files
Copy-Item "$repo\vault-template\00-Brain\*.md" -Destination "$vault\00-Brain\" -Force

# Copy the 5 division departments
Copy-Item "$repo\departments\*" -Destination "$vault\01-Departments\" -Recurse -Force

Write-Host "Vault structure created at $vault"
```

**Verify:**

Open Obsidian, refresh (F5). You'll see 5 folders on the left + 8 `.md` files in `00-Brain/`.

---

### Step 11: (Optional) Apply a pack (5 min)

The 5 division departments are the core — **no packs ship by default**. If you've
built your own overlay pack (see `docs/how-to-create-pack.md`), apply it via PowerShell:

```powershell
$vault = "F:\vaults\MyDivision"
$repo = "F:\.work\bd-business-os"
$pack = "<your-pack-code>"

# Copy the pack's departments
Copy-Item "$repo\packs\$pack\departments\*" -Destination "$vault\01-Departments\" -Recurse -Force

# Apply the pack's brain template (merge with the general template)
Copy-Item "$repo\packs\$pack\brain-template\*" -Destination "$vault\00-Brain\" -Force

Write-Host "Applied pack $pack"
```

**Verify in Obsidian:**

The `01-Departments/` folder has 5 sub-folders (plus any pack departments you added).

---

### Step 12: Fill in the 8 Brain files — Interview with Claude (15 min)

This is the **most important** step. An empty Brain = the AI doesn't know your company → garbage output. A complete Brain = the AI makes accurate decisions.

**8 files to fill (in `00-Brain/`):**

| File | Content | Required? |
|---|---|---|
| `strategy.md` | 3-5 year vision, ICP (target customer), USP, annual goals | ✅ Required |
| `products.md` | Menu/products + price + margin | ✅ Required |
| `state.md` | Stage (pre-seed/seed/growth/mature), runway, current KPIs | ✅ Required |
| `headcount.md` | Founding team + hiring plan + active departments | ✅ Required |
| `budget.md` | Total annual budget, CAPEX, OPEX | 🟡 Recommended |
| `laws.md` | Industry laws/regulations to comply with | 🟡 Recommended |
| `decisions-log.md` | Log of big decisions (auto-grows as you use it) | 🟢 Auto |
| `glossary.md` | Company terms dictionary | 🟢 Auto |

> 💡 **How to do it:** read the 16 questions below + type your answers into the Brain files in Obsidian. It's manual but **100% safe** — you control exactly what info the system has about your company.
>
> *Why not let Claude fill it?* — the Brain is the foundation the AI uses for every later decision. Filling it yourself ensures the data is 100% correct + you understand exactly what the system knows about your company.
>
> *Quick tip:* if you're lazy, after reading the 16 questions you can chat with Claude Code: "Here are my answers: [paste 16]. Generate the 8 Brain files per the format in README-USER.md Step 12.2 and write them with obsidian_patch_content."

**Step 12.1 — Answer 16 questions (prepare content)**

Open **Notepad** (or any editor), create a temp file `brain-answers.txt`. Answer these 16 (keep it short; you'll paste into the real files later):

**🎯 ROUND 1 — Strategy (4 questions):**

1. **3-5 year vision** — What do you want to achieve in 3-5 years? *(e.g. "Become a 5-10 location mid-tier cafe chain in Austin")*
2. **ICP — Target customer** — Who's the ideal customer? Age? Income? Main pain point? *(e.g. "Austin office workers, 22-40, income $50-100k, hate waiting >5 minutes")*
3. **USP — Differentiator** — How are you different from competitors? Max 2 USPs. *(e.g. "Fast grab-and-go + high-quality mid-tier coffee")*
4. **First-year revenue goal** — USD/year? Customers/day? AOV (average order value)? *(e.g. "$120-250k/year, 80-150 cups/day, AOV $5-7")*

**💰 ROUND 2 — Finance & scale (4 questions):**

5. **Initial investment (CAPEX)** — Total capital you have to start? How much for the first location? *(e.g. "$200k total, $100-150k for the first location")*
6. **Funding source** — Self / loan / co-founder / investor? *(e.g. "100% self-funded")*
7. **Launch timeline** — How soon to open? *(e.g. "1-3 months, location secured")*
8. **Current stage** — Pick one of 5: `pre-seed` (idea/not open), `seed` (open, testing), `growth` (expanding), `mature` (stable), `pivot` (changing direction). *(e.g. "pre-seed")*

**🍳 ROUND 3 — Products & people (4 questions):**

9. **Main menu/products** — 5-10 main SKUs + price + estimated margin. *(e.g. "Black coffee $4 margin 70%, latte $5 margin 70%, sandwich $6 margin 50%")*
10. **Main suppliers** — Where do you buy ingredients/products? *(e.g. "Beans from a local Texas roaster. Baked goods from a local supplier")*
11. **First location/team staffing** — How many people? Roles? Pay? *(e.g. "5-7 people: 1 manager $55-65k, 1 lead barista $20-22/hr, 1-2 baristas $16-18/hr, 2-3 servers $14-16/hr")*
12. **Current founding team** — Solo or co-founder? *(e.g. "Solo founder, no co-founder yet")*

**📊 ROUND 4 — KPI & operations (4 questions):**

13. **Weekly priority KPIs** — Cups/day? AOV? Food cost %? Customer return rate? Revenue/sq ft? *(e.g. "Cups/day + AOV")*
14. **Franchise plan** — Yes / No / After Y3 / Undecided. *(e.g. "Yes, after proving the model with 2-3 self-owned locations")*
15. **Compliance — laws to follow** — List the industry rules. *(e.g. "FDA Food Code + Texas DSHS food permit, local fire code, FLSA, Texas DTPA")*
16. **Brand identity** — Brand name + slogan (if any) + positioning. *(e.g. "Name: Lone Star Coffee. Slogan: 'Texas roast. In your hand.' Positioning: a fast, convenient Texas cafe for office workers")*

---

**Step 12.2 — Open the 8 template files in Obsidian + paste your answers**

In Obsidian (with the vault open), open each file in `00-Brain/` and fill it per the guide below.

⚠️ **VERY IMPORTANT about heading format** — the parser requires the heading **EXACTLY**, no suffix. One wrong word and the parser can't read it.

---

**📄 File 1: `strategy.md`** *(uses Q1, 2, 3, 4)*

Open the file → delete everything → paste:

```markdown
---
type: brain
section: strategy
aliases: ["Strategy", "Vision"]
last_updated: 2026-05-08
---
# Company strategy — <Company>

## Vision
<Answer Q1 — no quotes, no "(3-5 years)" added to the heading>

## Mission
<1-2 sentences describing why the company exists>

## Target Customer (ICP)
- **Segment:** <from Q2>
- **Age:** <from Q2>
- **Income:** <from Q2>
- **Behavior:** <from Q2>
- **Pain point:** <from Q2>

## First-year goals
- Revenue: <from Q4>
- Customers/day: <from Q4>
- AOV: <from Q4>

## Brand positioning
<1 positioning sentence, from Q16 if any>

## USP
<from Q3, 1-2 bullet lines>
```

✅ **Required headings, exact:** `## Vision` and `## Target Customer (ICP)` — write them exactly.

---

**📄 File 2: `state.md`** *(uses Q8)*

```markdown
---
type: brain
section: state
last_updated: 2026-05-08
---
# Current company state

## Stage
[<from Q8 — pick 1: pre-seed / seed / growth / mature / pivot>]

<1-2 paragraphs describing the current situation>

## Current quarter
- Revenue: <number if any, or "0 (not open)">
- Main KPI: <from Q13>
- Hot issues: <list the 2-3 biggest>

## Runway / financial health
- Cash: <from Q5>
- Burn/month: <estimate>
- Runway: <# months>
```

✅ **Required:** the line `[pre-seed]` (or another stage in square brackets) — the parser looks for this string.

---

**📄 File 3: `products.md`** *(uses Q9)*

```markdown
---
type: brain
section: products
last_updated: 2026-05-08
---
# Products — <Company>

## Main menu

| Code | Name | Price | Margin | Status |
|---|---|---|---|---|
| CFB | Black coffee | 4 | 70 | active |
| CFL | Latte | 5 | 70 | active |
| SAN | Sandwich | 6 | 50 | active |
<add SKUs from Q9, one per line>

## Suppliers
<from Q10>
```

✅ **Required:** the table must have **5 columns: `Code | Name | Price | Margin | Status`**. Code in UPPERCASE (e.g. `CFB`, not `cfb`). Price in **whole dollars** (`4`, not `$4` and not `3.50` — the parser reads whole numbers; a decimal like `3.50` would be misread as `350`).

---

**📄 File 4: `headcount.md`** *(uses Q11, 12)*

```markdown
---
type: brain
section: headcount
last_updated: 2026-05-08
---
# People & Departments — <Division>

## Team
- Division manager: <name + email from Q12>
<list direct reports if any>

## Active departments

- 01-hardware-engineering — <who owns it, e.g. "VP direct">
- 02-npi-program-management — <role>
- 03-quality-reliability — <role>
- 04-mfg-supplier-quality — <role>
- 05-service-operations — <role>
<add pack departments if any>

## Staffing plan
<from Q11>
```

✅ **Required:** each department is a bullet line starting with `- <2-digit number>-<name>` (e.g. `- 01-hardware-engineering`). The parser uses a regex to find this pattern.

---

**📄 File 5: `budget.md`** *(uses Q5)*

```markdown
---
type: brain
section: budget
last_updated: 2026-05-08
---
# Budget — <Company>

Total budget: <whole-number USD, e.g. "200000" for $200k>

## CAPEX (first location)
<list items from Q5>

## OPEX (monthly operations)
<list rent, payroll, COGS, utilities...>

## Buffer / Runway
<based on remaining capital>
```

✅ **Required:** the line `Total budget: <number>` exactly (the parser looks for this pattern). The number is whole, no commas/periods/words like "k".

---

**📄 File 6: `laws.md`** *(uses Q15)*

```markdown
---
type: brain
section: laws
last_updated: 2026-05-08
---
# Law & Compliance — <Company>

## Group 1: Business registration
- [ ] Entity formation (Texas SOS) or sole proprietorship/DBA
- [ ] EIN (IRS)

## Group 2: Industry compliance
<from Q15, list>

## Group 3: Labor
- FLSA (federal wage/hour) + at-will employment (Texas)
- FICA + FUTA/SUTA payroll taxes

## Group 4: Tax
- Texas sales-and-use tax 6.25% (state) [verify local rate]
- Federal income + self-employment tax; no Texas personal income tax
```

> General information only — not legal/tax advice. Confirm with a licensed Texas attorney and CPA.

---

**📄 File 7: `decisions-log.md`** — *(empty at first; the AI appends after running tasks)*

```markdown
---
type: brain
section: decisions
last_updated: 2026-05-08
---
# Decision log

> Append-only. Each big decision is recorded here.

## [2026-05-08] Brain initialized
**Decision:** Set up the US Business OS with the <your industry> pack.
**Decision-maker:** Department Head
```

---

**📄 File 8: `glossary.md`** — *(minimal template; the AI adds new terms as it meets them)*

```markdown
---
type: brain
section: glossary
last_updated: 2026-05-08
---
# Terms dictionary

## Finance
- **AOV**: Average Order Value.
- **CAPEX**: Up-front investment, buying long-term assets.
- **OPEX**: Monthly operating cost.
- **COGS**: Cost of goods sold.
- **Break-even**: The point where revenue covers cost.
- **Runway**: Months you can last if revenue = 0.

## US legal
- **FDA Food Code**: Model food-safety code; Texas adopts it via DSHS.
- **DSHS**: Texas Department of State Health Services (food permits).
- **EIN**: Employer Identification Number (IRS).
- **Sales tax**: Texas sales-and-use tax (Comptroller).
- **Franchise tax**: Texas franchise (margin) tax.
- **SE tax**: Self-employment tax (federal).
- **ICP**: Ideal Customer Profile.
```

✅ **Required:** each term is formatted `- **Term**: definition` (a colon `:` right after the closing `**`). Don't use an em dash `—`.

---

**Step 12.3 — Save all files**

In Obsidian, after pasting content + replacing placeholders in each file, press **Ctrl+S** to save.

If Obsidian has "Auto-save" configured (on by default) → files save when you switch tabs.

---

### Step 13: Verify the Brain is complete (2 min)

In a **Claude Code session**, type:

```
Run bd_status with vault F:\vaults\LoneStarCoffee
```

**Expected result:**

```json
{
  "vault": "F:\\vaults\\MyDivision",
  "icp": "- Segment: mid-size US retailers...",                  ✅ MUST NOT be "(not filled)"
  "vision": "Leading supplier of rugged terminals...",           ✅ MUST NOT be "(not filled)"
  "products": 3,                                                  ✅ Must be > 0
  "active_departments": ["01-hardware-engineering", ...],         ✅ Must list the 5 departments
  "state": "growth",                                              ✅ MUST NOT be "unknown"
  "tools_live": ["web_search", "us_law_search", ...],             ✅ 6 tools if you have a Tavily key
  "packs": []
}
```

**If you see:**

- `vision: "(not filled)"` → the Brain isn't filled or the heading format is wrong. Go back to Step 12.
- `products: 0` → `products.md` is missing the table with schema `| Code | Name | Price | Margin | Status |`.
- `state: "unknown"` → `state.md` is missing the line `[growth]` (or another stage in square brackets).
- `active_departments: []` → `headcount.md` is missing the department bullet list like `- 01-hardware-engineering`.

---

### ✅ Initialization done!

By now you have:

| Component | Status |
|---|---|
| A vault with 5 standard folders | ✅ |
| The 5 division departments | ✅ |
| 8 Brain files filled with division info | ✅ |
| `bd_status` reports data in all fields | ✅ |

**Next:** Part 3 — Daily use, or read PART 2.5 below for a full workflow demo first.

---

## 🎬 PART 2.5 — END-TO-END DEMO (Misty Morning Café marketing plan)

> This shows one real task from A→Z. Read it → understand the workflow + know what the output looks like.

**Scenario:** You own Misty Morning Café (vault `OPC-K1`). The Brain already has:
- May 2026 revenue: $7,850 (target June: $9,000)
- The lead barista just quit → urgent hire
- Food cost up to 33%
- Wi-Fi drops 2-3 times/week

You want to plan June marketing on a $700 budget.

### Stage 1 — Brief + Clarification (~30s)

**You chat in the Claude Code tab:**
> Plan June 2026 marketing for Misty Morning Café, $700 budget. Goal: grow revenue $7,850 → $9,000, raise the ticket $7.80 → $9.00 via combo upsell. Constraints: lead barista just quit, food cost 33%, flaky Wi-Fi.

**Claude auto-calls `bd_run` → returns:**
> Created task folder `02-Tasks/2026-MM-DD-...-june-marketing-cafe/`. There are 5 clarification questions to answer in `03-clarification.md`. Open Obsidian to see them.

**5 sample questions the system asked (citing the Brain):**
1. Is the $700 budget already in the annual budget? (Q1 cites `budget.md`)
2. The pastry+coffee combo has a lower margin than a coffee alone → which direction do you pick to offset the 33% food cost? (Q2 CRITICAL cites `products.md`)
3. Hitting $9,000 needs +18% turns + 15% ticket, but the kitchen is short a barista. Which risk do you trade off? (Q3 CRITICAL cites `headcount.md`)
4. Wi-Fi is flaky, ICP "stays 1-2h on a laptop" — still launch work-friendly, or postpone? (Q4 cites `strategy.md:icp`)
5. Specific timing to hire a barista? (Q5 free-text)

→ The system read the Brain + found 3 contradictions in the brief: combo margin, kitchen risk, Wi-Fi.

### Stage 2 — You answer + Resume (<10s)

Open `03-clarification.md` in Obsidian, tick the checkboxes + write free-text for Q5. Save (Ctrl+S).

**You tell Claude:**
> Done, continue.

**Claude auto-calls `bd_resume`** → records the answers, ready for the meeting.

### Stage 3 — Multi-department meeting (~2 min)

**You:**
> Run a meeting for 6 departments: Marketing + Finance + Operations + Sales + Customer + Kitchen.

**Claude auto-calls `bd_meeting`** → 3 rounds of debate:
- **R1** (perspectives): each department gives its own view (~21KB output)
- **R2** (debate): Pro vs Con argue (~20KB)
- **R3** (synthesis): 3 views Growth/Cautious/Balanced (~31KB)
- → Synthesizer + Translator + Citation validator → `07-decision-report.md` (~16KB, 250 lines)

**A typical decision report output:**
- 30s TL;DR: cut the budget $700 → $250, focus upsell + loyalty, ROAS 5-6x
- Recommendation: **GO with revisions** (don't reject the brief, fix the numbers)
- Adjustments from the brief: combo $8.50 → $9.50 (because $8.50 sells the croissant at a loss), digital punch card → paper card $50, morning goal 20-25 → 8-10 new customers/day
- What each department says: Kitchen warns food cost 33% is "red zone", Finance warns on cash flow, Operations demands an SOP + BCP, Customer flags Wi-Fi = churn risk
- Caught Marketing's math error (wrong +$3,740 → actually +$1,400-1,600)
- 3 perspectives: Growth bold, Cautious careful (but miscalculated), Balanced most feasible
- Week-1 blockers: 4G backup Wi-Fi + hire a barista + cash check
- Weekly KPI gates with PAUSE conditions
- **22 claims missing citations** flagged at the end (internal Brain figures, Department Head to verify)

### Stage 4 — STOP 1: Department Head approves (~2 min reading)

Open `07-decision-report.md` in Obsidian. Read the 30s TL;DR + Recommendation + Blockers.

**3 choices:**

**A. OK with the recommendation** → tell Claude "approve" → Stage 5.

**B. Want to edit** → edit `07-decision-report.md` directly in Obsidian (e.g. "change combo $9.50 → $9.00"), save, tell Claude "approve, I changed the combo to $9.00".

**C. Reject** → discard the task, start a different brief.

### Stage 5 — Approve + Execute (~1 min)

**You:**
> Approve, make the execution plan.

**Claude auto-calls `bd_approve`** → generates `08-execution-plan.md`: action items + deadlines + owners + budget.

### STOP 2: Department Head approves the execution plan

Read the plan, if OK:

**You:**
> OK, execute.

**Claude auto-calls `bd_execute`** → renders `.docx`/`.xlsx` into `03-Outputs/<task>/`:
- `june-marketing-plan-misty-morning.docx`
- `budget-allocation.xlsx`
- `weekly-kpi-gates.xlsx`

**Done.** Total time: ~5-7 minutes for one strategic task.

### Files generated (see in Obsidian)

```
02-Tasks/2026-MM-DD-june-marketing-cafe/
├── 00-brief.md                       1 KB  (your original brief)
├── 01-routing.md                     1 KB  (which departments were invited)
├── 02-context.md                     3 KB  (the Brain context the AI read)
├── 03-clarification.md               4 KB  (5 questions citing the Brain)
├── 03-clarification-answered.md      2 KB  (your answers)
├── 03b-research-findings.md          1 KB  (research tools output)
├── 04-meeting-r1-perspectives.md    21 KB  (round 1)
├── 05-meeting-r2-debate.md          20 KB  (round 2)
├── 06-meeting-r3-perspectives.md    31 KB  (round 3)
├── 07-decision-report.md            16 KB  ⭐ STOP 1
└── 08-execution-plan.md             ?  KB  ⭐ STOP 2

03-Outputs/2026-MM-DD-june-marketing-cafe/
├── june-marketing-plan.docx
├── budget-allocation.xlsx
└── weekly-kpi-gates.xlsx
```

→ **Every decision + document** is stored permanently in the Obsidian vault + git auto-commit. Looking back 3 months later, you know why you decided what, who objected, and how it actually turned out.

---

## 💼 PART 3 — DAILY USE

> This is the part you'll re-read most. Parts 1-2 are done once; **Part 3 is how you run the company day to day.**

---

### 📌 The one rule — Always use the Code tab

Open Claude Desktop → click **"</> Code"** in the top-right → **"+ New session"**.

In a Code-tab session:
- ✅ Every MCP tool is callable directly (10-minute timeout)
- ✅ No need to distinguish "light" vs "heavy" tasks
- ✅ No need to open a separate PowerShell

> 🚫 **Don't use the Cowork tab for heavy tasks** (e.g. "Draft an offer letter", "Analyze a location"). Cowork has a 60s timeout → a multi-department debate (60-180s) will fail. Save Cowork for light things like "summarize the vault" or read/edit files.

**Illustration — the same task, 2 different tabs:**

| Your task | Code tab | Cowork tab |
|---|---|---|
| "Summarize the vault, what stage is my company at?" | ✅ OK | ✅ OK |
| "Open the decision-report.md of task X" | ✅ OK | ✅ OK |
| "Edit budget.md, add $1,000 marketing spend" | ✅ OK | ✅ OK |
| "Draft a barista JD" | ✅ OK (~30s) | ⚠️ Borderline |
| "Draft an offer for a store manager at $55k" | ✅ OK (~30s) | ⚠️ Borderline |
| "Brainstorm a slogan + visual identity" | ✅ OK (~3-5 min) | ❌ Timeout |
| "Analyze which neighborhood to open location 2" | ✅ OK (~5-10 min) | ❌ Timeout |
| "Plan a $2,000 holiday ad campaign" | ✅ OK (~5-10 min) | ❌ Timeout |

→ **Default to the Code tab.** Use Cowork only when multitasking with the Chat tab and the task is definitely light.

---

### 🎬 Standard workflow — 2 paths

In the Code tab, just chat naturally. Claude classifies the task and picks one of 2 paths:

#### Path A — Fast path (`bd_draft`) for doc boilerplate

For: offer letter, JD, work rules, receipt, simple SOP, meeting invite...

**You:**
> Draft a barista JD for Lone Star Coffee, $18/hr, Q1 Austin.

**Claude:** (auto-calls `bd_draft`, ~10-30s)
> Created a draft at `02-Tasks/2026-MM-DD-HHMM-barista-jd/draft.md`. Open Obsidian to see it. Summary: requires 6 months espresso experience, 8h shifts × 6 days/week, FLSA-compliant pay...

→ **One call, a file right away.** No debate, no decision report. Good for docs with a standard template.

---

#### Path B — Full 5-stage pipeline for strategic decisions

For: big decisions (open a location, ad budget, rebrand), high-legal-risk docs, brainstorms needing multiple views.

**5 sequential stages:**

| # | MCP tool | Output | Time |
|---|---|---|---|
| 1 | `bd_run(brief, vault)` | `01-routing.md`, `02-context.md`, (maybe) `03-clarification.md` | 20-50s |
| 2 | `bd_resume(task_folder)` (if needed) | `03-clarification-answered.md` | <10s |
| 3 | `bd_meeting(task_folder)` | `04..06-meeting-*.md`, **`07-decision-report.md`** ← Stop 1 | 60-180s |
| 4 | `bd_approve(task_folder)` | **`08-execution-plan.md`** ← Stop 2 | 10-30s |
| 5 | `bd_execute(task_folder)` | `.docx`/`.xlsx` files in `03-Outputs/<task>/` | 10-30s |

**Real example:**

**You:**
> I want to analyze whether to open Lone Star Coffee location 2 in Q1 or Q3.

**Claude:** (calls `bd_run` ~30s)
> Created task folder `02-Tasks/2026-MM-DD-HHMM-location-2/`. There are 5 clarification questions to answer in `03-clarification.md` (open Obsidian). I'll wait.

**You:** (open Obsidian, answer the 5 questions, save Ctrl+S)
> Done, continue.

**Claude:** (calls `bd_resume` → `bd_meeting` ~2-3 min)
> The decision report is generated at `07-decision-report.md`. Summary: the system recommends **Q3** with $130k CAPEX, 18-month payback. Main reasons: ... 3 warnings: ...
>
> **Stop 1 — you approve:** open `07-decision-report.md` and read carefully. Agree → I'll run `bd_approve`. Want to edit → edit the file directly and tell me.

**You:**
> OK, approve.

**Claude:** (calls `bd_approve` ~30s → `bd_execute` ~15s)
> The execution plan is at `08-execution-plan.md`. The final `.docx` deliverable is at `03-Outputs/location-2/location-analysis.docx`. Open it.

---

### 🛑 Stop 1 + Stop 2 — Why they matter

The system has **2 deliberate stops** for you (the Department Head) to approve:

- **Stop 1 — after `bd_meeting`**: you review `07-decision-report.md` before approving. This is your chance to **reject / edit the decision** before the system renders docx.
- **Stop 2 — after `bd_approve`**: you review `08-execution-plan.md` before executing. This is your chance to see the **detailed rollout plan** and edit it before spending render effort.

→ **Don't skip these 2 stops.** If the system proposes something bad → edit the file directly in Obsidian, save, then tell Claude to continue to the next stage.

**Files that appear after each stage:**

| Stage | New file in the task folder | What you do |
|---|---|---|
| `bd_run` | `00-brief.md`, `01-routing.md`, `02-context.md`, maybe `03-clarification.md` | If there's a `03-clarification.md` → open, answer, save |
| `bd_resume` | `03-clarification-answered.md` | (automatic) |
| `bd_meeting` | `04..06-meeting-*.md`, `07-decision-report.md` | **Open `07-decision-report.md`, read + approve** |
| `bd_approve` | `08-execution-plan.md` | Read the plan, OK? |
| `bd_execute` | `03-Outputs/<task>/<file>.docx` | **Open the .docx → the final deliverable** |

---

### 📖 How to review the decision report

`07-decision-report.md` has a standard structure:

```markdown
# Decision report: <topic>

## 📌 Bottom line (30-second read)
- 3-5 summary lines for the Department Head
- The main recommendation

## Recommendation
**Go / Go with revisions / Don't go** — <explanation>

## Detailed analysis
### What each department says
<Marketing says..., Finance says..., ...>

### Pro vs Con debate
| Side | Argument | Source |

### 3 perspectives (Growth / Cautious / Balanced)

## Action items (do now)
| # | Item | Who | Due | Cost |

## KPI gates
| Week X | KPI | Threshold | Action if fail |

## Questions for the Department Head to decide
A. ...  B. ...  C. ...  D. ...

## ⚠️ Warning: claims missing a source
<lists claims to verify>
```

**How to read quickly (5 minutes):**

1. Read the **TL;DR** at the top (30 seconds)
2. Read the **Recommendation** (does the system say "Go" or "Don't")
3. Scan the **Action items** (anything too expensive or too urgent?)
4. Read the **claims missing a source** warning — if it's an important figure → verify it yourself
5. Answer the **Questions for the Department Head** (A/B/C/D) → record in the decision log or edit the decision report directly

**When NOT to approve:**

- 🔴 Recommendation "Go" but claims lack citations for big figures (e.g. "revenue will grow 30%" with no source)
- 🔴 Action items cost more than the budget
- 🔴 The Con side has a strong argument the Pro side hasn't rebutted
- 🔴 You feel it's "off" — a founder's instinct is usually right

→ Edit `07-decision-report.md` directly (change the recommendation, add a note), then run `approve` after.

---

### ⏱️ Estimated timing table (Claude Code tab)

| Tool | Actual time |
|---|---|
| `bd_status` | < 1 second |
| Read/edit a file (obsidian_*) | 1-5 seconds |
| `bd_draft` | 10-30 seconds |
| `bd_run` (1 SIMPLE task) | 20-50 seconds |
| `bd_run` (needs clarification) | 20-50 seconds + your answer time |
| `bd_resume` | <10 seconds |
| `bd_meeting` (DeepSeek v4-pro) | 1-3 minutes |
| `bd_approve` | 10-30 seconds |
| `bd_execute` (render docx) | 10-30 seconds |
| **Total pipeline, 1 SIMPLE task** | **3-5 minutes** |
| **Total pipeline, 1 task with clarification** | **5-10 minutes** |

→ **If it's much slower than this** (e.g. meeting > 10 minutes) → it may be stuck. In the Code session, type `/abort`, check Obsidian to see which files were created, retry from the nearest stage.

---

### 🔄 "A workday with US OS" workflow

This is the pattern you'll do daily once you're used to it — **all in one Code tab, no app switching.**

**Morning (5 minutes):**
1. Open Claude Desktop → Code tab → **+ New session**
2. Type: "What's new in the Lone Star Coffee vault? This week's KPIs?"
3. Claude auto-calls `bd_status` + lists tasks → summarizes today's focus

**When there's a big task (3-10 minutes):**
1. In the open Code session, type naturally: "Draft an offer for a store manager at $55k"
2. Claude auto-picks the Fast path (`bd_draft`) or Full pipeline (`bd_run → meeting → ...`)
3. Wait (do something else — you're still in the same session, no PowerShell)
4. Claude says "done" → open Obsidian to see the deliverable file

**End of week (10 minutes):**
1. In the Code session: "List this week's big decisions in 02-Tasks/"
2. "Update `00-Brain/decisions-log.md` with the 3 most important decisions"
3. Claude edits the file via the Obsidian MCP

---

## 🔧 PART 4 — COMMON ERRORS & FIXES

### 🩺 30-second health check (run when you suspect a problem)

Open **PowerShell**, paste this whole block:

```powershell
Write-Host "`n=== VN OS Health Check ===" -ForegroundColor Cyan

Write-Host "`n[1/5] Python version:" -ForegroundColor Yellow
python --version

Write-Host "`n[2/5] Package install location:" -ForegroundColor Yellow
python -c "import json; from pathlib import Path; p = Path([d for d in __import__('site').getsitepackages() + [__import__('site').getusersitepackages()] if (Path(d) / 'bd_business_os-0.2.0.dist-info').exists()][0]) / 'bd_business_os-0.2.0.dist-info' / 'direct_url.json'; print(json.loads(p.read_text())['url'])"

Write-Host "`n[3/5] Claude Desktop processes:" -ForegroundColor Yellow
(Get-Process claude -ErrorAction SilentlyContinue | Measure-Object).Count

Write-Host "`n[4/5] bd-os-mcp processes:" -ForegroundColor Yellow
(Get-Process bd-os-mcp -ErrorAction SilentlyContinue | Measure-Object).Count

Write-Host "`n[5/5] Vault .env file:" -ForegroundColor Yellow
$envFile = Read-Host "  Enter the vault path (e.g. F:\vaults\LoneStarCoffee)"
if (Test-Path "$envFile\.env") {
    Get-Content "$envFile\.env" | ForEach-Object { if ($_ -match "^DEEPSEEK|^TAVILY") { ($_ -split "=")[0] + "=" + (($_ -split "=")[1].Substring(0,[Math]::Min(8,($_ -split "=")[1].Length))) + "..." } }
} else { Write-Host "  ❌ .env not found!" -ForegroundColor Red }
```

**Expected results:**
- [1/5] Python 3.11+ or 3.12+
- [2/5] `file:///F:/.work/bd-business-os` (the real repo path)
- [3/5] 1-12 (Claude Desktop running)
- [4/5] 1-3 (MCP running — multiple processes are normal with multiple sessions)
- [5/5] `DEEPSEEK_API_KEY=sk-xxxxx...` (a key, not blank)

If any is wrong → find the matching "Error" below.

---

### Error 1: MCP tool timeout / no response

**Symptom:** Claude calls `bd_meeting` but it doesn't return after > 5 minutes.

**Fix:**
1. Are you on the **"</> Code"** tab? If you're on **Cowork** → switch to Code.
2. Open Obsidian, go to `02-Tasks/<task_folder>/` and see which files were created:
   - Has `04-meeting-r1-perspectives.md` but not `07-decision-report.md` → meeting is running, wait more.
   - Has `07-decision-report.md` → meeting is done, tell Claude "I see the decision report, continue with `bd_approve`".
3. If truly stuck → in the Code session type `/abort`, then retry the stage.

### Error 2: `bd_status` reports `error: Brain dir not found`

**Symptom:** `{"error": "...00-Brain not found..."}`

**Fix:**
- Wrong vault path → check spelling, especially spaces (`"F:\vaults\LoneStarCoffee"` should be in quotes).
- Vault not onboarded → run `bd_onboard` (Step 10, Method 1).

### Error 3: `tools_skipped` contains `web_search / us_law_search`

**Symptom:** bd_status reports 4 tools skipped due to missing `TAVILY_API_KEY`.

**Fix:**
1. Sign up for free Tavily at https://app.tavily.com → Settings → API Keys → create a key (like `tvly-xxxxx`).
2. Open `F:\vaults\<Company>\.env`, add a line:
   ```
   TAVILY_API_KEY=tvly-xxxxxxxxxxx
   ```
3. Restart Claude Desktop (quit fully → reopen).
4. Test: `bd_status` → `tools_live` should have 6 tools.

> 💡 **You can still use it without a Tavily key** — the decision report just won't have live research (new laws, real competitors). The system still uses the Brain + LLM knowledge to debate.

### Error 4: `Method not found` when calling bd_draft / bd_run / bd_meeting

There are **2 different causes** for the same error message:

#### 4.A — The MCP server didn't load the tool

**Symptom:** Claude says "I don't have access to the bd_status tool" or Method not found on **every** bd_* tool.

**Fix:**
1. Check `claude_desktop_config.json` has a `bd-business-os` entry:
   ```powershell
   notepad "$env:APPDATA\Claude\claude_desktop_config.json"
   ```
2. Is the `bd-os-mcp.exe` path correct: `F:\\.work\\bd-business-os\\.venv\\Scripts\\bd-os-mcp.exe` (escape `\` as `\\`).
3. **Quit Claude Desktop THE RIGHT WAY** from the tray (see Step 8.3) — NOT just close the window.

#### 4.B — Missing DEEPSEEK_API_KEY (LLM sampling unavailable)

**Symptom:** `bd_status` runs OK, but `bd_draft` / `bd_run` / `bd_meeting` reports `Method not found`.

**Root cause:** the code falls back to MCP sampling when there's no `DEEPSEEK_API_KEY` / `ANTHROPIC_API_KEY`. But the Claude Code tab doesn't implement the MCP sampling protocol → `Method not found`.

**Fix:**
1. Open `F:\vaults\<Company>\.env`, make sure it has:
   ```
   DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
   ```
2. **Verify the key loads**: in Claude Code chat:
   > Run bd_status with vault F:\vaults\<Company>
   → The `tools_live` field should have `industry_benchmark`, `tax_calculator`. If both are missing → `.env` didn't load.
3. **Quit + restart Claude Desktop** from the tray (Step 8.3) so the MCP server picks up the new env vars.

### Error 4.5: Code edits don't take effect

**Symptom:** you edited a `.py` file in the repo, restarted Claude Desktop, called a tool — still the old code.

**Root cause:** the old `bd-os-mcp.exe` process is still running in the background (Claude Desktop "close" only minimizes to the tray).

**Fix:**
```powershell
# 1. Kill all old MCP processes
Get-Process bd-os-mcp -ErrorAction SilentlyContinue | Stop-Process -Force

# 2. Quit Claude Desktop from the tray (right-click icon → Quit)

# 3. Verify
Get-Process claude, bd-os-mcp -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count
# → must be 0

# 4. Reopen Claude Desktop → click the "</> Code" tab
```

### Error 4.6: Code edits don't take effect because the install points to another folder

**Symptom:** you edit files in `F:\.work\bd-business-os\` but the MCP server still loads old code from another folder (e.g. an OneDrive copy).

**How to check:**
```powershell
python -c "import json; from pathlib import Path; p = Path([d for d in __import__('site').getsitepackages() + [__import__('site').getusersitepackages()] if (Path(d) / 'bd_business_os-0.2.0.dist-info').exists()][0]) / 'bd_business_os-0.2.0.dist-info' / 'direct_url.json'; print(json.loads(p.read_text())['url'])"
```

If the output is **not** `file:///F:/.work/bd-business-os` → it's loading from another folder.

**Fix:**
```powershell
# Uninstall the old one
pip uninstall bd-business-os bd-business-os -y

# Kill the MCP process (so the exe file isn't locked)
Get-Process bd-os-mcp -ErrorAction SilentlyContinue | Stop-Process -Force

# Reinstall from the right folder
cd "F:\.work\bd-business-os"
pip install -e .

# Quit + restart Claude Desktop from the tray
```

### Error 5: DeepSeek `API key invalid`

**Symptom:** `bd_run` / `bd_draft` reports `Authentication failed`.

**Fix:**
1. Open `F:\vaults\<Company>\.env`, check `DEEPSEEK_API_KEY=sk-...` is the right key.
2. Go to https://platform.deepseek.com → API Keys → check the key is still active and has credit.
3. Fix the key → save .env → restart Claude Desktop.

### Error 6: Obsidian MCP `connection refused`

**Symptom:** `obsidian_list_files_in_vault` reports a connection error.

**Fix:**
1. The Obsidian app must be running (vault open).
2. The Local REST API plugin must be Enabled (Settings → Community plugins).
3. Is OBSIDIAN_API_KEY in `claude_desktop_config.json` correct? Re-copy it from Settings → Local REST API → API Key.

### Error 7: `pip install -e .` fails

**Symptom:** Step 5 fails with `error: subprocess-exited-with-error`.

**Fix:**
1. Python version ≥ 3.11? Check with `python --version`.
2. Is the venv activated? The prompt must have `(.venv)` at the start.
3. If you get `Microsoft Visual C++ 14.0 required` → install [VC++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

---

## 💡 PART 5 — BEST-PRACTICE TIPS

### Tip 1: The fuller the Brain, the better the decisions

Every line you fill in the Brain → Claude/DeepSeek uses it to debate. An empty Brain = the AI "guesses" → generic output. Investing 30 minutes filling the Brain well = saving hours fixing wrong decision reports later.

### Tip 2: Update the Brain every month

At each month's end, open the 8 Brain files and update:
- `state.md` — last month's actual revenue, new hot issues
- `budget.md` — actual spend vs. budget
- `decisions-log.md` — append the month's big decisions

A "living" Brain → every new task reflects the company's current situation, not the onboarding state.

### Tip 3: The more specific the brief, the better the output

❌ Bad brief: "Draft a JD"
✅ Good brief: "Draft a barista JD for Lone Star Coffee, $18/hr, Q1 Austin, requires 6 months espresso experience, 8h shifts × 6 days/week, FLSA-compliant, prefer candidates who know latte art"

A good brief = fewer clarification questions = the right output the first time.

### Tip 4: Use `bd_draft` for simple docs, the full pipeline for big decisions

| Task | Tool to use |
|---|---|
| Offer letter, JD, work rules, receipt, meeting invite, simple SOP | `bd_draft` |
| Strategic analysis, opening a location, big budget, rebrand | Full pipeline (`bd_run → meeting → approve → execute`) |
| High legal stakes (big partner contracts, IPO docs) | Full pipeline + hire a lawyer to review |

### Tip 5: At the end of a session, archive old tasks

After 30 days, move old tasks in `02-Tasks/` to `99-Archive/<year-month>/`:

> "Move the tasks in 02-Tasks/ created before 2026-04-01 to 99-Archive/2026-Q1/"

Claude auto-calls `obsidian_*` to move the files. Keeping `02-Tasks/` lean → the vault loads faster.

### Tip 6: Back up the vault periodically

The vault is your company's entire "brain." Losing it = losing all decisions + historical documents.

**Method 1 — Git private repo (recommended):**
```powershell
cd "F:\vaults\LoneStarCoffee"
git init
git add .
git commit -m "init vault"
# Create a private repo on GitHub → push
git remote add origin https://github.com/<you>/lone-star-vault.git
git push -u origin main
```
Each week: `git add . && git commit -m "weekly backup" && git push`.

**Method 2 — Manual copy:**
Periodically copy the `F:\vaults\LoneStarCoffee` folder to OneDrive/Google Drive.

---

### Tip 7: Workflow when updating the repo / editing code

When you pull a new version of the repo, or edit Python code yourself:

```powershell
# 1. Pull the new version (if using git)
cd "F:\.work\bd-business-os"
git pull

# 2. Kill old MCP processes
Get-Process bd-os-mcp -ErrorAction SilentlyContinue | Stop-Process -Force

# 3. (If pyproject.toml changed) reinstall:
pip install -e .

# 4. Quit Claude Desktop from the tray (right-click icon → Quit)

# 5. Reopen Claude Desktop → Code tab → test:
#    "Run bd_status with vault F:\vaults\<Company>"
```

> ⚠️ **Skipping any step can cause "code edits do nothing."** Especially step 2 (kill MCP) and step 4 (Quit tray) — these are the 2 students forget most.

---

## 🤝 PART 6 — FOR DEVELOPERS (advanced)

### Run the MCP server in debug mode

```powershell
cd "F:\.work\bd-business-os"
.\.venv\Scripts\Activate.ps1
$env:MCP_DEBUG = "1"
bd-os-mcp
```

Logs print directly to the console → you can debug tool calls.

### Override config via `.vncoderc`

The file `$HOME\.vncoderc` (created in Step 7.2), edit:

```yaml
llm:
  primary: deepseek-v4-pro          # or claude-sonnet-4-6
  secondary: deepseek-v4-flash
  max_retries: 3
  max_tokens_per_task: 100000

meeting:
  max_debate_rounds: 1     # 1 = fast, 2 = more thorough
  total_max: 3

translator_mode: final_only   # off | final_only | all_intermediate
```

### Test a new pack

Create `docs/packs/<your-pack>/` following the structure in `docs/how-to-create-pack.md`. Test:
```powershell
pytest docs/tests/ -k "your_pack" -v
```

### Contribute

PR at https://github.com/<owner>/bd-business-os. Especially needed:
- New packs: Real Estate, Healthcare, Education, Beauty
- Glossary: add terms
- Test coverage: real-LLM E2E

---

**Problem with Parts 1-6?** Open an issue at: https://github.com/<owner>/bd-business-os/issues
