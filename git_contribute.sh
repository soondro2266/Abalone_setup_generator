#!/bin/bash

extensions="py|cpp|h|md|gitignore"

git log --pretty="%an" --numstat | awk -v ext="$extensions" '
  /^[^-0-9]/ && index($0, "\t") == 0 {
    author = $0
    next
  }

  NF == 3 && ( $1 ~ /^[0-9-]+$/ ) {
    if ($1 == "-" || $2 == "-" || ($1 == 0 && $2 == 0)) {
      next
    }

    file = $3

    if (file ~ "\\.(" ext ")$") {
      add[author] += $1
      del[author] += $2
    }
  }

  END {
    printf "---------------------------------------------\n"
    for (a in add) {
      printf "> %-15s\t+%d\t-%d\n", a, add[a], del[a]
    }
  }
' | sort -k5 -nr
