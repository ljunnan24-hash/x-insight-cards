#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd "${script_dir}/.." && pwd)"
source_dir="${repo_dir}/skills/x-insight-cards"
codex_root="${CODEX_HOME:-${HOME}/.codex}"
target_dir="${codex_root}/skills/x-insight-cards"

if [[ ! -f "${source_dir}/SKILL.md" ]]; then
  echo "Skill source not found: ${source_dir}" >&2
  exit 1
fi

mkdir -p "${codex_root}/skills"
if [[ -e "${target_dir}" ]]; then
  backup_dir="${target_dir}.backup.$(date +%Y%m%d%H%M%S)"
  mv "${target_dir}" "${backup_dir}"
  echo "Backed up existing skill to ${backup_dir}"
fi

cp -R "${source_dir}" "${target_dir}"
echo "Installed x-insight-cards to ${target_dir}"
