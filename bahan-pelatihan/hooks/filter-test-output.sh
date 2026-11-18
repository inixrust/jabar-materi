#!/bin/bash
# Hook PreToolUse untuk Bash: jika perintah adalah pelari tes, saring keluarannya
# agar hanya baris kegagalan yang masuk ke konteks Claude. Mengurangi token.
# Memerlukan `jq`. Sesuaikan pola perintah di bawah dengan pelari tes proyekmu.
input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command')

pattern='^(npm test|pytest|go test)( [^;&|<>`$#\\[:cntrl:]]*)?$'
if [[ "$cmd" =~ $pattern ]]; then
  filtered_cmd="$cmd 2>&1 | grep -A 5 -E '(FAIL|ERROR|error:)' | head -100"
  echo "$input" | jq --arg filtered "$filtered_cmd" \
    '{hookSpecificOutput: {hookEventName: "PreToolUse", updatedInput: (.tool_input + {command: $filtered})}}'
else
  echo "{}"
fi
