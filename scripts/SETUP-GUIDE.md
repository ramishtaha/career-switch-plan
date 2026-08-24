# 🖥️ Laptop Setup Guide — Day 1 Ready

> **Goal**: Turn your laptop from a relapse vehicle into a dev machine.
> Two scripts, run in order. ~30-45 min total. Do this tonight (Aug 24).

---

## Why this matters

Your relapse chain is: **web-series/reels → no sleep → freeze → guilt → nothing**.
Your laptop is both your **learning tool** (IntelliJ, Spring Boot) AND your **relapse trigger**.

These two scripts fix both sides:
1. **Block the distractions** at the DNS level (no willpower needed).
2. **Install the dev tools** so Day 1 starts with code, not config fighting.

---

## Prerequisites

- Laptop running Ubuntu (tested on 24.04). Windows/Mac users: see [Manual Setup](#manual-setup-other-os) below.
- Internet connection.
- Sudo access (your own laptop, so yes).
- ~2 GB free disk space (IntelliJ is big).

---

## Step 1: Focus Shield (Block Distractions)

```bash
cd ~/career-switch-plan
chmod +x scripts/01-focus-shield.sh
sudo ./scripts/01-focus-shield.sh install
```

**What it does:**
- Blocks Instagram, YouTube, Netflix, Prime, Hotstar, Facebook, web-series sites, TikTok via `/etc/hosts`.
- Flushes DNS cache so it takes effect immediately.
- Creates two toggle scripts in `scripts/`:
  - `focus-on.sh` — re-enable blocking (frictionless).
  - `focus-off.sh` — disable blocking (**30-second delay + intent log**).

**Why the delay on focus-off?**
The 30s delay turns an impulse into a conscious decision. You have to type a reason and wait. That friction is the point — it breaks the automatic "just one episode" loop.

**Test it:** Try opening youtube.com or instagram.com in your browser. Should fail to load.

**If you need YouTube for a learning video:**
```bash
./scripts/focus-off.sh     # 30s delay, type reason
# watch the video
./scripts/focus-on.sh      # re-block immediately
```

---

## Step 2: Dev Environment (JDK 17 + IntelliJ + Spring Boot)

```bash
cd ~/career-switch-plan
chmod +x scripts/02-dev-setup.sh
./scripts/02-dev-setup.sh
```

**What it does (6 steps):**
1. Installs **JDK 17** (LTS — required for Spring Boot).
2. Installs **Maven** (Java build tool).
3. Installs **IntelliJ IDEA Community** (via snap).
4. Configures **git** (asks for your name/email if not set).
5. Clones your `career-switch-plan` repo to `~/career-switch-plan`.
6. Scaffolds a **Spring Boot starter project** at `study-materials/springboot-hello`.

**After it finishes:**
1. Open IntelliJ: run `idea.sh` or find "IntelliJ IDEA" in your app menu.
2. `File > Open` → select `~/career-switch-plan/study-materials/springboot-hello`
3. Wait for Maven to import dependencies (~2-5 min, first time).
4. Run `SpringbootHelloApplication` → console shows `Started ... on port 8080`.
5. Visit `http://localhost:8080` — a 404 page is normal (no endpoints yet).

That's your first win. Alhamdulillah.

---

## Step 3: Open IntelliJ for the Spring Boot project

The script creates a starter project with:
- `SpringbootHelloApplication.java` — the main class (entry point).
- `pom.xml` — Maven config with `spring-boot-starter-web` dependency.
- `application.properties` — basic config (port 8080).

When Hermes (me) says "Type continue" in your next session, we'll add your first REST endpoint — a `GET /hello` that returns a message. That's where the real learning starts.

---

## Troubleshooting

### `java: command not found` after install
```bash
sudo update-alternatives --config java
# select the JDK 17 option
```

### IntelliJ won't launch from terminal
```bash
/snap/intellij-idea-community/current/bin/idea.sh
# or launch from your app menu
```

### Spring Initializr download failed (no internet / blocked)
The script falls back to creating the project manually, so you'll still have a working project. If you want the full Initializr version later:
```bash
./scripts/focus-off.sh   # unblock (Spring Initializr isn't blocked, but if your DNS is weird)
cd ~/career-switch-plan/study-materials/springboot-hello
rm -rf src pom.xml
curl https://start.spring.io/starter.zip -d type=maven-project -d language=java -d bootVersion=3.4.0 -d groupId=com.ramish -d artifactId=springboot-hello -d name=springboot-hello -d packageName=com.ramish.springboot -d javaVersion=17 -d dependencies=web -o starter.zip
unzip starter.zip && rm starter.zip
./scripts/focus-on.sh
```

### Focus shield didn't block sites
```bash
# Check if the block is in /etc/hosts
grep FOCUS-SHIELD /etc/hosts
# Flush DNS again
sudo resolvectl flush-caches
# Restart your browser (close fully, reopen)
```

### I want to add/remove a blocked site
Edit the `DISTRACTION_DOMAINS` array in `scripts/01-focus-shield.sh`, then:
```bash
sudo ./scripts/01-focus-shield.sh uninstall
sudo ./scripts/01-focus-shield.sh install
```

---

## Manual Setup (Other OS)

### Windows
- **JDK 17**: Download from [Adoptium](https://adoptium.net/temurin/releases/?version=17). Set `JAVA_HOME` env var.
- **IntelliJ**: Download from [jetbrains.com](https://www.jetbrains.com/idea/download/?section=windows).
- **Git**: Download from [git-scm.com](https://git-scm.com/download/win).
- **Focus shield**: Edit `C:\Windows\System32\drivers\etc\hosts` as Administrator. Add `127.0.0.1 instagram.com` etc. (same domains as the script).
- **Repo**: `git clone https://github.com/ramishtaha/career-switch-plan.git`

### macOS
- **JDK 17**: `brew install openjdk@17` (install Homebrew first if needed).
- **IntelliJ**: `brew install --cask intellij-idea-ce`
- **Git**: `brew install git` (or use the built-in one).
- **Focus shield**: Edit `/etc/hosts` with `sudo nano /etc/hosts`. Add the same domains. Flush DNS: `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`.
- **Repo**: `git clone https://github.com/ramishtaha/career-switch-plan.git`

---

## Daily Workflow (after setup)

This is how your laptop fits into your day:

| Time | Activity | Tool |
|------|----------|------|
| Fajr → Sunrise | DSA revision + 1 new problem | IntelliJ or browser (LeetCode) |
| Sunrise + 15min | Spring Boot theory (45 min) | IntelliJ |
| 10:45–18:00 | Office (TCS laptop) | Phone only (Office Mode) |
| 21:15–22:30 | Spring Boot practice (60 min) | IntelliJ |
| 22:30 | Sleep | Charger OUT of bedroom |

**Key rule**: The focus shield stays ON during all learning blocks. If you need YouTube for a tutorial, use `focus-off.sh` → watch → `focus-on.sh`. The friction keeps you honest.

---

## Checklist (do tonight, Aug 24)

- [ ] Run `sudo ./scripts/01-focus-shield.sh install`
- [ ] Verify youtube.com is blocked in browser
- [ ] Run `./scripts/02-dev-setup.sh`
- [ ] Open IntelliJ, open the springboot-hello project
- [ ] Run the app, see "Started on port 8080"
- [ ] Charger OUT of bedroom, phone greyscale ON
- [ ] Sleep by 22:30 — Day 1 is tomorrow (Aug 25)
