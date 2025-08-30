#!/bin/bash
# check-docs.sh - Local documentation quality checking script
# Run this before committing documentation changes

set -e

echo "🔍 O-Nakala Core Documentation Quality Check"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Check if we're in the right directory
if [[ ! -f "START_HERE.md" ]]; then
    print_status $RED "❌ Error: Must be run from o-nakala-core root directory"
    exit 1
fi

print_status $GREEN "✅ Running from correct directory"

# 1. Check required files exist
echo ""
echo "1. Checking required documentation files..."

required_files=(
    "START_HERE.md"
    "docs/GETTING_STARTED.md"
    "docs/API_REFERENCE.md"
    "docs/CSV_FORMAT_GUIDE.md"
    "docs/user-guides/01-upload-guide.md"
    "docs/user-guides/02-collection-guide.md"
    "docs/user-guides/03-workflow-guide.md"
    "docs/user-guides/05-troubleshooting.md"
    "examples/workflow_documentation/best-practices.md"
    "examples/workflow_documentation/institutional-setup.md"
)

missing_files=0
for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        print_status $GREEN "  ✅ $file"
    else
        print_status $RED "  ❌ $file - MISSING"
        missing_files=$((missing_files + 1))
    fi
done

if [[ $missing_files -gt 0 ]]; then
    print_status $RED "❌ $missing_files required files missing"
    exit 1
fi

print_status $GREEN "✅ All required files present"

# 2. Check internal link integrity
echo ""
echo "2. Checking internal links..."

broken_links=0

# Function to check if a file exists relative to another file
check_link() {
    local source_file=$1
    local link_target=$2
    local source_dir=$(dirname "$source_file")
    
    # Remove anchor fragments
    local file_part=$(echo "$link_target" | cut -d'#' -f1)
    
    # Skip external links
    if [[ "$file_part" =~ ^https?:// ]]; then
        return 0
    fi
    
    # Skip empty links
    if [[ -z "$file_part" ]]; then
        return 0
    fi
    
    # Resolve relative path
    local full_path
    if [[ "$file_part" = /* ]]; then
        # Absolute path (from repo root)
        full_path=".$file_part"
    else
        # Relative path
        full_path="$source_dir/$file_part"
    fi
    
    # Normalize path and check if file exists
    if [[ ! -f "$full_path" ]]; then
        print_status $RED "  ❌ Broken link in $source_file: $link_target"
        return 1
    fi
    
    return 0
}

# Check links in all markdown files
while IFS= read -r -d '' file; do
    # Extract markdown links [text](link)
    while IFS= read -r link; do
        if ! check_link "$file" "$link"; then
            broken_links=$((broken_links + 1))
        fi
    done < <(grep -oP '\[.*?\]\(\K[^)]*(?=\))' "$file" 2>/dev/null || true)
done < <(find . -name "*.md" -not -path "./.git/*" -not -path "./node_modules/*" -print0)

if [[ $broken_links -gt 0 ]]; then
    print_status $RED "❌ $broken_links broken internal links found"
    exit 1
fi

print_status $GREEN "✅ All internal links valid"

# 3. Check navigation structure
echo ""
echo "3. Checking navigation structure..."

# Check START_HERE.md has role-based navigation
if grep -q "Digital Humanities Researcher\|Data Manager\|Developer\|Administrator" START_HERE.md; then
    print_status $GREEN "  ✅ START_HERE.md has role-based navigation"
else
    print_status $RED "  ❌ START_HERE.md missing role-based navigation"
    exit 1
fi

# Check README.md links to START_HERE.md
if grep -q "START_HERE.md" README.md; then
    print_status $GREEN "  ✅ README.md links to START_HERE.md"
else
    print_status $RED "  ❌ README.md doesn't link to START_HERE.md"
    exit 1
fi

# Check key files have navigation breadcrumbs
key_files=("docs/GETTING_STARTED.md" "docs/API_REFERENCE.md" "docs/CSV_FORMAT_GUIDE.md")
for file in "${key_files[@]}"; do
    if grep -q "📍 You are here:\|START_HERE" "$file"; then
        print_status $GREEN "  ✅ $file has navigation breadcrumbs"
    else
        print_status $YELLOW "  ⚠️  $file missing navigation breadcrumbs"
    fi
done

print_status $GREEN "✅ Navigation structure valid"

# 4. Check for common content issues
echo ""
echo "4. Checking content quality..."

content_issues=0

# Check for TODO/FIXME markers in key files
while IFS= read -r -d '' file; do
    if grep -i "TODO\|FIXME\|XXX" "$file" >/dev/null 2>&1; then
        todos=$(grep -in "TODO\|FIXME\|XXX" "$file" | head -3)
        print_status $YELLOW "  ⚠️  TODOs in $file:"
        echo "$todos" | while read -r line; do
            echo "    $line"
        done
        content_issues=$((content_issues + 1))
    fi
done < <(find . -name "*.md" -not -path "./.git/*" -not -path "./node_modules/*" -print0)

# Check for consistent header structure
inconsistent_headers=0
while IFS= read -r -d '' file; do
    # Check if file starts with h1
    if [[ $(head -n 5 "$file" | grep -c "^# ") -eq 0 ]]; then
        if [[ "$file" != "./README.md" ]] && [[ "$file" != *"/archived/"* ]] && [[ "$file" != *"examples/sample_dataset/files/"* ]]; then
            print_status $YELLOW "  ⚠️  $file doesn't start with h1 header"
            inconsistent_headers=$((inconsistent_headers + 1))
        fi
    fi
done < <(find . -name "*.md" -not -path "./.git/*" -not -path "./node_modules/*" -print0)

if [[ $content_issues -gt 0 ]]; then
    print_status $YELLOW "⚠️  $content_issues files with TODOs (consider resolving)"
fi

if [[ $inconsistent_headers -gt 0 ]]; then
    print_status $YELLOW "⚠️  $inconsistent_headers files with inconsistent headers"
fi

print_status $GREEN "✅ Content quality checks completed"

# 5. Generate documentation metrics
echo ""
echo "5. Documentation metrics..."

total_md_files=$(find . -name "*.md" -not -path "./.git/*" -not -path "./node_modules/*" | wc -l)
echo "  📊 Total markdown files: $total_md_files"

# Count words in key documentation
key_docs_words=0
for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        words=$(wc -w < "$file")
        key_docs_words=$((key_docs_words + words))
    fi
done

echo "  📊 Words in key documentation: $key_docs_words"

# Check file sizes (warn about very large files)
large_files=0
while IFS= read -r -d '' file; do
    size=$(wc -l < "$file")
    if [[ $size -gt 1000 ]]; then
        print_status $YELLOW "  ⚠️  Large file: $file ($size lines)"
        large_files=$((large_files + 1))
    fi
done < <(find . -name "*.md" -not -path "./.git/*" -not -path "./node_modules/*" -print0)

if [[ $large_files -gt 0 ]]; then
    print_status $YELLOW "⚠️  $large_files large files detected (>1000 lines)"
fi

# Final summary
echo ""
echo "📋 Summary"
echo "=========="
print_status $GREEN "✅ Required files: All present"
print_status $GREEN "✅ Internal links: All valid"  
print_status $GREEN "✅ Navigation: Properly structured"
print_status $GREEN "✅ Content: Quality checks passed"

if [[ $content_issues -gt 0 ]] || [[ $inconsistent_headers -gt 0 ]] || [[ $large_files -gt 0 ]]; then
    print_status $YELLOW "⚠️  Minor issues detected but documentation is functional"
    echo ""
    echo "To run this check automatically before commits, add to .git/hooks/pre-commit:"
    echo "#!/bin/bash"
    echo "./scripts/check-docs.sh"
else
    print_status $GREEN "🎉 All documentation quality checks passed!"
fi

echo ""
echo "💡 Tip: Run 'scripts/check-docs.sh' before committing documentation changes"