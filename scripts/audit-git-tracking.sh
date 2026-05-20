#!/bin/sh
set -eu

usage() {
  cat <<'USAGE'
Usage: ./scripts/audit-git-tracking.sh [--strict-local]

Checks that repository tracking is safe for publication:
  - tracked and staged files do not include local/runtime artifacts or secrets
  - untracked local-only artifacts are ignored by .gitignore
  - nested Git repositories and gitlinks are absent
  - whitespace checks pass

Options:
  --strict-local  Fail if ignored local/runtime artifacts are present.
                  Use this for a fully clean release workspace.
USAGE
}

strict_local=false
case "${1:-}" in
  "")
    ;;
  --strict-local)
    strict_local=true
    ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    echo "error: unknown option: $1" >&2
    usage >&2
    exit 2
    ;;
esac

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "error: not inside a Git repository" >&2
  exit 1
fi

cd "$(git rev-parse --show-toplevel)"

for required_command in git grep find awk wc tr; do
  if ! command -v "$required_command" >/dev/null 2>&1; then
    echo "error: required command not found: $required_command" >&2
    exit 1
  fi
done

bad_path_pattern='(^|/)(node_modules|\.DS_Store|\.AppleDouble|\.LSOverride|Thumbs\.db|\.next|out|\.vercel|test-results|playwright-report|coverage|\.cache|\.turbo|\.parcel-cache|\.nyc_output|\.direnv)(/|$)|(^|/)\._|\.tsbuildinfo$|(^|/)next-env\.d\.ts$|\.(db|db-journal|sqlite|sqlite3|sqlite3-journal|log|tmp|temp|pem|key|p12|pfx)$|(^|/)(npm-debug|yarn-debug|yarn-error|pnpm-debug)\.log|(^|/)\.env($|[./_-])|(^|/)\.envrc$'
allowed_bad_path_pattern='(^|/)\.env\.example$'

match_bad_paths() {
  grep -E "$bad_path_pattern" | grep -Ev "$allowed_bad_path_pattern" || true
}

count_lines() {
  if [ -z "$1" ]; then
    printf '0'
  else
    printf '%s\n' "$1" | wc -l | tr -d ' '
  fi
}

echo "== Git status =="
git status --short --branch

echo
echo "== Tracked local artifact and secret scan =="
tracked_hits="$(git ls-files | match_bad_paths)"
if [ -n "$tracked_hits" ]; then
  echo "$tracked_hits"
  echo "error: local/runtime artifacts or secret-like files are tracked" >&2
  exit 1
fi
echo "ok: no tracked local/runtime artifacts or secret-like files"

echo
echo "== Staged local artifact and secret scan =="
staged_hits="$(git diff --cached --name-only --diff-filter=ACMRTUXB --no-renames | match_bad_paths)"
if [ -n "$staged_hits" ]; then
  echo "$staged_hits"
  echo "error: local/runtime artifacts or secret-like files are staged" >&2
  exit 1
fi
echo "ok: no staged local/runtime artifacts or secret-like files"

echo
echo "== Untracked local artifact and secret scan =="
untracked_hits="$(git ls-files --others --exclude-standard | match_bad_paths)"
if [ -n "$untracked_hits" ]; then
  echo "$untracked_hits"
  echo "error: untracked local/runtime artifacts or secret-like files are not ignored" >&2
  echo "hint: remove them or add a safe ignore rule before publishing" >&2
  exit 1
fi
echo "ok: untracked local/runtime artifacts and secret-like files are ignored"

echo
echo "== Ignored local artifact inventory =="
ignored_hits="$(git ls-files --others --ignored --exclude-standard | match_bad_paths)"
if [ -n "$ignored_hits" ]; then
  echo "$ignored_hits"
  ignored_count="$(count_lines "$ignored_hits")"
  if [ "$strict_local" = true ]; then
    echo "error: $ignored_count ignored local/runtime artifact(s) present in strict mode" >&2
    exit 1
  fi
  echo "ok: $ignored_count ignored local/runtime artifact(s) present and excluded from Git"
else
  echo "ok: no ignored local/runtime artifacts present"
fi

echo
echo "== Nested Git directory scan =="
nested_git_hits="$(find . \
  -path './.git' -prune -o \
  -path './.git.nested-backup*' -prune -o \
  -path '*/.git.nested-backup*' -prune -o \
  -type d -name .git -print)"
if [ -n "$nested_git_hits" ]; then
  echo "$nested_git_hits"
  echo "error: nested Git directories found; import project files as normal tracked files" >&2
  exit 1
fi
echo "ok: no nested Git directories found"

echo
echo "== Submodule/gitlink scan =="
gitlink_hits="$(git ls-files -s | awk '$1 == "160000" {print $4}')"
if [ -n "$gitlink_hits" ]; then
  echo "$gitlink_hits"
  echo "error: gitlinks found; website should be tracked as normal files" >&2
  exit 1
fi
echo "ok: no gitlinks found"

echo
echo "== Whitespace check =="
git diff --check
git diff --cached --check
echo "ok: whitespace checks passed"

echo
echo "Git tracking audit passed."
