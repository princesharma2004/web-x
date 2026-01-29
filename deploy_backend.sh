#!/bin/bash
set -e

# ================= CONFIG =================
REPO_URL="https://github.com/princesharma2004/web-x.git"
REPO_DIR="web-x"
BACKEND_DIR="backend"
APP_PORT=8000
# ==========================================

echo "🚀 Starting backend deployment..."

# 1️⃣ Install git if missing
if ! command -v git >/dev/null 2>&1; then
  echo "📦 Installing git..."
  sudo apt update
  sudo apt install git -y
fi

# 2️⃣ Clone or update repository
if [ -d "$REPO_DIR" ]; then
  echo "🔄 Repository exists, pulling latest changes..."
  cd "$REPO_DIR"
  git pull
else
  echo "📥 Cloning repository..."
  git clone "$REPO_URL"
  cd "$REPO_DIR"
fi

# 3️⃣ Move to backend directory
cd "$BACKEND_DIR"

# 4️⃣ Stop old containers (safe)
echo "🧹 Cleaning old containers..."
docker compose down -v || true

# 5️⃣ Build & run backend
echo "🐳 Building and starting backend..."
docker compose up -d --build

# 6️⃣ Fetch public IP
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)

# 7️⃣ Print execution links
echo ""
echo "✅ BACKEND DEPLOYED SUCCESSFULLY"
echo "--------------------------------------------"
echo "🌍 API Root     : http://$PUBLIC_IP:$APP_PORT/"
echo "📘 Swagger Docs : http://$PUBLIC_IP:$APP_PORT/docs"
echo "❤️ Health Check : http://$PUBLIC_IP:$APP_PORT/health"
echo "🗄 DB Check     : http://$PUBLIC_IP:$APP_PORT/db-check"
echo "--------------------------------------------"
echo "🎯 Ready for hackathon demo"
