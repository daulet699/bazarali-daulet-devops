#!/usr/bin/env bash
set -eu
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
INFO_FILE="$ROOT_DIR/Bazarali_Daulet_info.txt"
echo '=============================='
echo 'Student Information'
echo '=============================='
echo 'Name: Daulet'
echo 'Surname: Bazarali'
echo 'Group: IT2-2308'
echo 'Student ID: 37392'
echo '=============================='
echo 'System Information'
echo '=============================='
echo "Username: $(whoami)"
echo "Hostname: $(hostname)"
echo "Current Date: $(date)"
echo "Operating System: $(uname -a)"
echo 'Disk Usage:'
df -h .
echo 'Memory Usage:'
if command -v free >/dev/null 2>&1; then
  free -h
elif command -v vm_stat >/dev/null 2>&1; then
  vm_stat
else
  echo 'No supported memory info command found'
fi
if [[ -f "$INFO_FILE" ]]; then
  echo 'Student information file exists.'
else
  echo 'Student information file does not exist.'
fi
