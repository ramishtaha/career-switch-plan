#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────
# DEV SETUP — Java + Spring Boot dev environment for Ramish's career switch
# ──────────────────────────────────────────────────────────────────────────
# WHAT IT DOES:
#   1. Installs JDK 17 (LTS — required for Spring Boot 4.x)
#   2. Installs Maven (build tool)
#   3. Installs IntelliJ IDEA Community (via snap or tarball fallback)
#   4. Sets JAVA_HOME, configures git user if missing
#   5. Clones career-switch-plan repo (if not already present)
#   6. Scaffolds a Spring Boot starter project ready to open in IntelliJ
#
# WHY: Day 1 is tomorrow. You should open IntelliJ to a ready project,
#      not spend your first day fighting installs. The first win builds momentum.
#
# USAGE (on your laptop):
#   chmod +x scripts/02-dev-setup.sh
#   ./scripts/02-dev-setup.sh
#
# RUNS ON: Ubuntu/Debian. For other distros, see the manual steps at the bottom.
# ──────────────────────────────────────────────────────────────────────────
set -euo pipefail

color_green() { printf '\033[0;32m%s\033[0m\n' "$1"; }
color_yellow(){ printf '\033[0;33m%s\033[0m\n' "$1"; }
color_red()   { printf '\033[0;31m%s\033[0m\n' "$1"; }

step() { echo ""; color_yellow "▶ $1"; }

# --- Pre-flight: detect OS ----------------------------------------------------
detect_os() {
  if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_ID="${ID:-unknown}"
    OS_LIKE="${ID_LIKE:-}"
  else
    OS_ID="unknown"
    OS_LIKE=""
  fi
  if echo "$OS_ID $OS_LIKE" | grep -qiE "ubuntu|debian"; then
    PKG_MGR="apt"
  elif echo "$OS_ID $OS_LIKE" | grep -qiE "fedora|rhel|centos"; then
    PKG_MGR="dnf"
  elif echo "$OS_ID $OS_LIKE" | grep -qiE "arch"; then
    PKG_MGR="pacman"
  else
    PKG_MGR="unknown"
  fi
  echo "Detected OS: $OS_ID (package manager: $PKG_MGR)"
}

# --- Step 1: JDK 17 -----------------------------------------------------------
install_jdk17() {
  step "Step 1/6: JDK 17 (LTS — Spring Boot 4.x requirement)"
  if command -v java >/dev/null 2>&1; then
    local ver
    ver=$(java -version 2>&1 | head -1 | awk -F\" '{print $2}')
    if [[ "$ver" == 17* ]]; then
      color_green "✅ JDK 17 already installed ($ver). Skipping."
      return
    else
      color_yellow "Found Java $ver, but need 17. Installing 17 alongside..."
    fi
  fi

  case "$PKG_MGR" in
    apt) sudo apt-get update -qq && sudo apt-get install -y openjdk-17-jdk ;;
    dnf) sudo dnf install -y java-17-openjdk-devel ;;
    pacman) sudo pacman -S --noconfirm jdk17-openjdk ;;
    *)
      color_red "Unknown package manager. Install JDK 17 manually:"
      echo "  Ubuntu/Debian: sudo apt install openjdk-17-jdk"
      echo "  Fedora/RHEL:   sudo dnf install java-17-openjdk-devel"
      echo "  Arch:          sudo pacman -S jdk17-openjdk"
      echo "  Or download:   https://adoptium.net/temurin/releases/?version=17"
      return 1
      ;;
  esac

  # Set JAVA_HOME via alternatives (Ubuntu) or direct path
  if [ -d "/usr/lib/jvm/java-17-openjdk-amd64" ]; then
    export JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
  elif [ -d "/usr/lib/jvm/java-17-openjdk" ]; then
    export JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
  fi
  color_green "✅ JDK 17 installed. Verify with: java -version"
}

# --- Step 2: Maven ------------------------------------------------------------
install_maven() {
  step "Step 2/6: Maven (build tool)"
  if command -v mvn >/dev/null 2>&1; then
    color_green "✅ Maven already installed ($(mvn -version 2>&1 | head -1)). Skipping."
    return
  fi
  case "$PKG_MGR" in
    apt) sudo apt-get install -y maven ;;
    dnf) sudo dnf install -y maven ;;
    pacman) sudo pacman -S --noconfirm maven ;;
    *) color_yellow "Install Maven manually: https://maven.apache.org/download.cgi"; return ;;
  esac
  color_green "✅ Maven installed."
}

# --- Step 3: IntelliJ IDEA Community ------------------------------------------
install_intellij() {
  step "Step 3/6: IntelliJ IDEA Community Edition"
  if command -v idea >/dev/null 2>&1 || snap list intellij-idea-community >/dev/null 2>&1 2>&1; then
    color_green "✅ IntelliJ IDEA Community already installed. Skipping."
    return
  fi
  if command -v snap >/dev/null 2>&1; then
    sudo snap install intellij-idea-community --classic
    color_green "✅ IntelliJ IDEA Community installed via snap."
  else
    color_yellow "snap not found. Manual install options:"
    echo "  1. Download: https://www.jetbrains.com/idea/download/?section=linux"
    echo "  2. Extract to /opt/intellij-idea-community"
    echo "  3. Run: /opt/intellij-idea-community/bin/idea.sh"
    echo "  Or install snap first: sudo apt install snapd"
  fi
}

# --- Step 4: Git config -------------------------------------------------------
configure_git() {
  step "Step 4/6: Git config"
  if [ -z "$(git config --global user.name)" ]; then
    read -rp "Enter your git name (e.g. Ramish Taha): " git_name
    git config --global user.name "$git_name"
    color_green "  ✅ git user.name set to: $git_name"
  else
    color_green "  ✅ git user.name = $(git config --global user.name)"
  fi
  if [ -z "$(git config --global user.email)" ]; then
    read -rp "Enter your git email: " git_email
    git config --global user.email "$git_email"
    color_green "  ✅ git user.email set to: $git_email"
  else
    color_green "  ✅ git user.email = $(git config --global user.email)"
  fi
  git config --global init.defaultBranch main
  git config --global core.editor nano
  color_green "✅ Git configured."
}

# --- Step 5: Clone repo ------------------------------------------------------
clone_repo() {
  step "Step 5/6: Clone career-switch-plan repo"
  local repo_dir="$HOME/career-switch-plan"
  if [ -d "$repo_dir/.git" ]; then
    color_green "✅ Repo already cloned at $repo_dir. Pulling latest..."
    cd "$repo_dir" && git pull --ff-only
    return
  fi
  git clone https://github.com/ramishtaha/career-switch-plan.git "$repo_dir"
  color_green "✅ Repo cloned to $repo_dir"
}

# --- Step 6: Scaffold Spring Boot starter project -----------------------------
scaffold_springboot() {
  step "Step 6/6: Scaffold Spring Boot starter project"
  local project_dir="$HOME/career-switch-plan/study-materials/springboot-hello"

  if [ -d "$project_dir" ]; then
    color_green "✅ Spring Boot project already exists at $project_dir. Skipping."
    return
  fi
  mkdir -p "$project_dir"

  # Check if Spring Initializr curl is possible, else create manually
  if curl --connect-timeout 10 -sf "https://start.spring.io" -o /dev/null 2>&1; then
    color_yellow "  Fetching project from Spring Initializr..."
    curl -s "https://start.spring.io/starter.zip" \
      -d "type=maven-project" \
      -d "language=java" \
      -d "bootVersion=4.0.0" \
      -d "baseDir=springboot-hello" \
      -d "groupId=com.ramish" \
      -d "artifactId=springboot-hello" \
      -d "name=springboot-hello" \
      -d "packageName=com.ramish.springboot" \
      -d "packaging=jar" \
      -d "javaVersion=17" \
      -d "dependencies=web" \
      -o "$project_dir/springboot-hello.zip"
    if [ -s "$project_dir/springboot-hello.zip" ]; then
      cd "$project_dir" && unzip -o springboot-hello.zip && rm springboot-hello.zip
      color_green "✅ Spring Boot project scaffolded via Spring Initializr."
      echo "   Location: $project_dir"
      echo "   Open in IntelliJ: File > Open > select $project_dir"
      return
    fi
  fi

  # Fallback: create minimal project manually
  color_yellow "  No internet for Spring Initializr. Creating minimal project manually..."
  create_manual_project "$project_dir"
  color_green "✅ Minimal Spring Boot project created at $project_dir"
  echo "   Open in IntelliJ: File > Open > select $project_dir"
}

create_manual_project() {
  local dir="$1"
  mkdir -p "$dir/src/main/java/com/ramish/springboot" "$dir/src/main/resources"

  cat > "$dir/pom.xml" <<'POM_EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.4.0</version>
        <relativePath/>
    </parent>
    <groupId>com.ramish</groupId>
    <artifactId>springboot-hello</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>springboot-hello</name>
    <description>Day 1 Spring Boot starter — Ramish career switch</description>
    <properties>
        <java.version>17</java.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
POM_EOF

  cat > "$dir/src/main/java/com/ramish/springboot/SpringbootHelloApplication.java" <<'JAVA_EOF'
package com.ramish.springboot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class SpringbootHelloApplication {
    public static void main(String[] args) {
        SpringApplication.run(SpringbootHelloApplication.class, args);
    }
}
JAVA_EOF

  cat > "$dir/src/main/resources/application.properties" <<'PROP_EOF'
# Spring Boot Day 1 — default config
server.port=8080
spring.application.name=springboot-hello
PROP_EOF
}

# --- Verify -------------------------------------------------------------------
verify_setup() {
  step "Verification"
  echo "Java:   $(java -version 2>&1 | head -1 || echo 'NOT FOUND')"
  echo "Maven:  $(mvn -version 2>&1 | head -1 || echo 'NOT FOUND')"
  echo "Git:    $(git --version)"
  echo "IntelliJ: $(command -v idea >/dev/null 2>&1 && echo 'installed' || snap list intellij-idea-community >/dev/null 2>&1 && echo 'installed (snap)' || echo 'check manually')"
}

# --- Main ---------------------------------------------------------------------
usage() {
  echo "Usage: $0"
  echo "  Installs JDK 17, Maven, IntelliJ Community, git config,"
  echo "  clones the repo, and scaffolds a Spring Boot starter project."
  echo ""
  echo "Options:"
  echo "  --skip-intellij   skip IntelliJ install (install manually later)"
  echo "  --skip-clone      skip repo clone (already cloned)"
}

SKIP_INTELLIJ=false
SKIP_CLONE=false
for arg in "$@"; do
  case "$arg" in
    --skip-intellij) SKIP_INTELLIJ=true ;;
    --skip-clone) SKIP_CLONE=true ;;
    *) usage; exit 0 ;;
  esac
done

echo "═══════════════════════════════════════════════════════════════"
echo "  DEV SETUP — Java + Spring Boot environment for Day 1"
echo "  Goal: open IntelliJ to a ready project, not fight installs"
echo "═══════════════════════════════════════════════════════════════"
echo ""
detect_os

install_jdk17
install_maven
[ "$SKIP_INTELLIJ" = false ] && install_intellij || color_yellow "Skipping IntelliJ (manual install later)"
configure_git
[ "$SKIP_CLONE" = false ] && clone_repo || color_yellow "Skipping repo clone"
scaffold_springboot
verify_setup

echo ""
color_green "═══════════════════════════════════════════════════════════════"
color_green "  ✅ DEV SETUP COMPLETE — ready for Day 1"
color_green "═══════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "  1. Open IntelliJ: idea.sh  (or launch from app menu)"
echo "  2. File > Open > ~/career-switch-plan/study-materials/springboot-hello"
echo "  3. Wait for Maven to import dependencies (first time, ~2-5 min)"
echo "  4. Run SpringbootHelloApplication — should see 'Started ... on port 8080'"
echo "  5. Visit http://localhost:8080 — 404 is normal (no endpoints yet)"
echo ""
echo "When Hermes asks 'Type continue', we'll add your first REST endpoint."
