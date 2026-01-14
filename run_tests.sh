#!/usr/bin/env bash

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Activate virtual environment
source venv/bin/activate

# Run pytest and capture exit code
if pytest test_app.py -v; then
    echo -e "${GREEN}✓ All tests passed successfully!${NC}"
    exit 0
else
    echo -e "${RED}✗ Tests failed. Please review the output above.${NC}"
    exit 1
fi
