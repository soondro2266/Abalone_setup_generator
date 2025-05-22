#!/bin/bash

extensions="py|cpp|h|md|gitignore"  # 請改成你的副檔名

git log --pretty="%an" --numstat | awk -v ext="$extensions" '
  # 作者行：沒有 tab 字元，且不以數字或 - 開頭
  /^[^-0-9]/ && index($0, "\t") == 0 {
    author = $0
    next
  }

  # 檔案行：三欄，且第一欄是數字或 "-"
  NF == 3 && ( $1 ~ /^[0-9-]+$/ ) {
    # 忽略新增與刪除是 "-" 或 0 的行（通常為 rename 或無改動）
    if ($1 == "-" || $2 == "-" || ($1 == 0 && $2 == 0)) {
      next
    }

    file = $3

    # 過濾副檔名
    if (file ~ "\\.(" ext ")$") {
      add[author] += $1
      del[author] += $2
    }
  }

  END {
    printf "---------------------------------------------\n"
    for (a in add) {
      total = add[a] - del[a]
      printf "👤 %-15s\t+%d\t-%d\t= %d\n", a, add[a], del[a], total
    }
  }
' | sort -k5 -nr
