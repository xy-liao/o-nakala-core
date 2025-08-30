# Documentation Maintenance Guide

This guide covers the automated tools and procedures for maintaining O-Nakala Core documentation quality.

## Overview

The documentation system includes automated quality assurance to prevent link rot, maintain navigation consistency, and ensure content quality as the project evolves.

## Automated Tools

### 1. Local Quality Checking

#### Quick Check Script
```bash
# Run before committing documentation changes
./scripts/check-docs.sh
```

**Features:**
- Validates all required files exist
- Checks internal link integrity  
- Verifies navigation structure consistency
- Detects content quality issues
- Generates documentation metrics

#### Comprehensive Maintenance Tool
```bash
# Generate full maintenance report
python3 scripts/maintain-docs.py --report --output maintenance-report.md

# Check links only
python3 scripts/maintain-docs.py --check-links

# Attempt to fix broken links
python3 scripts/maintain-docs.py --fix-links --dry-run
python3 scripts/maintain-docs.py --fix-links  # Actually apply fixes
```

**Features:**
- Link graph analysis and broken link detection
- Navigation consistency validation
- Comprehensive documentation metrics
- Orphaned file identification
- Automatic link repair (where possible)
- Improvement suggestions

### 2. GitHub Actions Integration

The repository includes automated quality assurance that runs on:
- Every push to main/develop branches
- Pull requests affecting documentation
- Weekly scheduled runs

**Workflow file:** `.github/workflows/documentation-quality.yml`

**Includes:**
- Link integrity checking with markdown-link-check
- Documentation structure validation
- Content quality analysis
- Accessibility checks

## Quality Standards

### Required Files
The system enforces the existence of key navigation files:

**Core Navigation:**
- `START_HERE.md` - Single entry point
- `docs/GETTING_STARTED.md` - Consolidated setup guide
- `docs/API_REFERENCE.md` - Technical reference
- `docs/CSV_FORMAT_GUIDE.md` - Format specifications

**User Workflows:**
- `docs/user-guides/01-upload-guide.md`
- `docs/user-guides/02-collection-guide.md` 
- `docs/user-guides/03-workflow-guide.md`
- `docs/user-guides/05-troubleshooting.md`

**Production Documentation:**
- `examples/workflow_documentation/best-practices.md`
- `examples/workflow_documentation/institutional-setup.md`

### Navigation Standards

#### Breadcrumb Requirements
Key documentation files must include navigation breadcrumbs:

```markdown
**📍 You are here:** [START_HERE](../START_HERE.md) → [Section] → Current Guide

**⏱️ Time:** X minutes | **👥 Audience:** Target audience | **📈 Level:** Beginner/Intermediate/Advanced
```

#### Footer Navigation
All guides should include consistent footer navigation:

```markdown
---

## 🧭 Navigation

### ⬅️ Previous Steps
- [Previous Guide](link) - Brief description

### ➡️ Next Steps  
- **Recommended next**: [Next Guide](link) - Brief description

### 🔍 Related Resources
- [Quick Reference](link) - Essential commands
- [Troubleshooting](link) - Problem solving

### 🆘 Need Help?
- **Quick issues**: [Troubleshooting Guide](../user-guides/05-troubleshooting.md)
- **Community support**: [GitHub Issues](https://github.com/xy-liao/o-nakala-core/issues)

---

*📍 **You are here:** [START_HERE](../START_HERE.md) → [Section] → Current Guide*
```

### Link Quality Standards

#### Internal Links
- All internal links must point to existing files
- Use relative paths from the source file
- Include descriptive link text (not "click here")
- Test anchors in large files

#### External Links
- External links should be stable and authoritative
- NAKALA platform links should use current URLs
- Include backup/alternative links where appropriate

## Maintenance Procedures

### Weekly Tasks (Automated)
- Link integrity checking
- Documentation structure validation
- Content quality analysis
- Metrics generation

### Monthly Tasks (Manual Review)
```bash
# Generate comprehensive report
python3 scripts/maintain-docs.py --report

# Review suggestions and implement improvements
# Check for new content gaps
# Update navigation if structure changes
```

### When Adding New Documentation

1. **Follow naming conventions**:
   - Use descriptive, hyphenated filenames
   - Place in appropriate directory structure
   - Follow existing organizational patterns

2. **Include required elements**:
   - Navigation breadcrumbs for key files
   - Cross-references to related content
   - Clear audience and time indicators
   - Footer navigation section

3. **Test before committing**:
   ```bash
   ./scripts/check-docs.sh
   ```

4. **Update navigation**:
   - Add to relevant navigation hubs
   - Update START_HERE.md if creating new learning paths
   - Ensure discoverability

### When Removing/Moving Files

1. **Update references**:
   ```bash
   # Find all references to the file
   grep -r "filename.md" . --include="*.md"
   
   # Update or remove references
   ```

2. **Create redirects for important files**:
   ```markdown
   # MOVED: Content Consolidated
   
   This file has been moved to [New Location](new-location.md).
   ```

3. **Run maintenance tools**:
   ```bash
   python3 scripts/maintain-docs.py --check-links
   ```

### Emergency Link Repair

If the automated systems detect widespread broken links:

1. **Assess the scope**:
   ```bash
   python3 scripts/maintain-docs.py --check-links
   ```

2. **Attempt automatic repair**:
   ```bash
   python3 scripts/maintain-docs.py --fix-links --dry-run
   python3 scripts/maintain-docs.py --fix-links
   ```

3. **Manual review and fixes**:
   - Check the maintenance report for unfixable links
   - Determine if files were moved, renamed, or deleted
   - Update references or create appropriate redirects

## Monitoring and Metrics

### Key Metrics Tracked
- Total documentation files and word count
- Link health (broken links, orphaned files)
- Navigation consistency scores
- Content quality indicators
- User journey completeness

### Quality Thresholds
- **Link health**: 0 broken internal links
- **Navigation consistency**: Key files must have breadcrumbs
- **File size warnings**: Files >1000 lines flagged for review
- **Orphaned files**: Minimize files not linked from anywhere

### Reporting
- Automated weekly quality reports
- Monthly comprehensive maintenance reports  
- Trend analysis for documentation growth and health
- Issue tracking for systematic problems

## Integration with Development Workflow

### Pre-commit Hooks
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
if [[ $(git diff --cached --name-only | grep -c "\.md$") -gt 0 ]]; then
    ./scripts/check-docs.sh
fi
```

### CI/CD Integration
The documentation quality workflow automatically:
- Validates all documentation on pushes
- Blocks merges with broken links
- Generates quality reports
- Maintains documentation health metrics

### Release Process
Before each release:
1. Run comprehensive maintenance report
2. Address any quality issues
3. Update documentation to reflect new features
4. Validate all examples and commands work with current version

## Future Enhancements

### Planned Improvements
- **Content freshness tracking**: Identify outdated content
- **User journey analytics**: Track which paths users actually follow
- **Automated content suggestions**: AI-powered content gap identification
- **Performance monitoring**: Documentation load times and accessibility
- **Multi-language support**: Framework for internationalization

### Community Contributions
- Templates for community documentation contributions
- Style guide for consistent voice and formatting
- Review process for community-submitted documentation
- Recognition system for documentation contributors

This maintenance framework ensures O-Nakala Core documentation remains high-quality, navigable, and useful as the project evolves.