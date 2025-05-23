#!/bin/bash

extensions=("*.py" "*.cpp" "*.h" "*.gitignore" ".md" )

temp_file=$(mktemp)

echo "🔍 掃描檔案中..."


for ext in "${extensions[@]}"; do
    
    find . -type f -name "$ext" ! -path "*/.git/*" | while read file; do
        echo "📁 分析檔案：$file"
        
        git blame --line-porcelain "$file" 2>/dev/null | \
            grep "^author " | \
            sed 's/^author //' >> "$temp_file"
    done
done

echo ""
echo "📊 統計每位作者的貢獻行數："
sort "$temp_file" | uniq -c | sort -nr


rm "$temp_file"
