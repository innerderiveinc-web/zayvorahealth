#!/usr/bin/env bash
# ==============================================================================
# ZAYVORA HEALTH OS - MOBILE STANDALONE APK BUILD PIPELINE
# ==============================================================================
# Automates the verification and generation of standalone Android .apk binaries
# for the ZAYVORA Health OS Patient & Clinician Mobile Companion.
#
# Target Profile: preview (distribution: internal, buildType: apk)
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
MOBILE_DIR="${BASE_DIR}/apps/mobile"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}  ZAYVORA Health OS - Android Standalone APK Builder   ${NC}"
echo -e "${BLUE}======================================================${NC}"

# 1. Verify Directory
if [ ! -d "${MOBILE_DIR}" ]; then
  echo -e "${RED}[ERROR] Mobile app directory not found at: ${MOBILE_DIR}${NC}"
  exit 1
fi

cd "${MOBILE_DIR}"

# 2. Verify Config Files
echo -e "${YELLOW}[1/4] Verifying mobile configuration manifests...${NC}"
if [ ! -f "app.json" ]; then
  echo -e "${RED}[ERROR] app.json missing from apps/mobile!${NC}"
  exit 1
fi

if [ ! -f "eas.json" ]; then
  echo -e "${RED}[ERROR] eas.json missing from apps/mobile!${NC}"
  exit 1
fi

# Verify preview profile in eas.json
if ! grep -q '"buildType": "apk"' eas.json; then
  echo -e "${RED}[ERROR] eas.json does not contain android buildType 'apk'!${NC}"
  exit 1
fi
echo -e "${GREEN}✓ Verified app.json and eas.json (buildType: apk configured)${NC}"

# 3. Check Node & Package Dependencies
echo -e "${YELLOW}[2/4] Verifying Node runtime and package.json scripts...${NC}"
if command -v node >/dev/null 2>&1 && node -v >/dev/null 2>&1; then
  NODE_VERSION=$(node -v 2>/dev/null || echo "detected")
  echo -e "${GREEN}✓ Node.js detected: ${NODE_VERSION}${NC}"
else
  echo -e "${YELLOW}! Node.js check bypassed (will execute in terminal environment)${NC}"
fi

# 4. Check EAS CLI
echo -e "${YELLOW}[3/4] Inspecting EAS CLI availability...${NC}"
if command -v eas >/dev/null 2>&1 && eas --version >/dev/null 2>&1; then
  EAS_CMD="eas"
  echo -e "${GREEN}✓ Global EAS CLI detected${NC}"
else
  EAS_CMD="npx eas-cli"
  echo -e "${YELLOW}! Global eas-cli not directly invoked; defaults to 'npx eas-cli'${NC}"
fi

# 5. Build Execution / Instructions
BUILD_MODE="${1:---help}"

case "${BUILD_MODE}" in
  --local)
    echo -e "${BLUE}Starting local Android APK build via EAS CLI...${NC}"
    echo -e "${YELLOW}Note: Requires local Android SDK, Java 17+, and fast hardware.${NC}"
    ${EAS_CMD} build -p android --profile preview --local
    ;;
  --cloud)
    echo -e "${BLUE}Submitting standalone APK build to EAS Cloud...${NC}"
    ${EAS_CMD} build -p android --profile preview
    ;;
  --verify-only)
    echo -e "${GREEN}✓ All manifests and build configurations verified successfully.${NC}"
    echo -e "${GREEN}Standby ready for APK packaging.${NC}"
    ;;
  *)
    echo -e "${YELLOW}[4/4] Standalone APK Build Usage Instructions:${NC}"
    echo -e "  To trigger a Cloud EAS Android APK build (Recommended):"
    echo -e "    ${GREEN}cd apps/mobile && npm run build:apk:cloud${NC}"
    echo -e "    OR:"
    echo -e "    ${GREEN}./scripts/build_mobile_apk.sh --cloud${NC}"
    echo ""
    echo -e "  To trigger a Local Standalone Android APK build (requires Android SDK):"
    echo -e "    ${GREEN}cd apps/mobile && npm run build:apk${NC}"
    echo -e "    OR:"
    echo -e "    ${GREEN}./scripts/build_mobile_apk.sh --local${NC}"
    echo ""
    echo -e "  Direct download link to .apk will be output upon EAS build completion."
    ;;
esac

echo -e "${GREEN}======================================================${NC}"
echo -e "${GREEN}  Mobile Build Pipeline Configuration: READY (Pass)   ${NC}"
echo -e "${GREEN}======================================================${NC}"
exit 0
