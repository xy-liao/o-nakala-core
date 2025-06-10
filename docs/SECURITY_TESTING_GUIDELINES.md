# Security Testing Guidelines

## 🔒 Secure Temporary Directory Usage

### ❌ **NEVER DO THIS** (Security Vulnerability)
```python
# VULNERABLE CODE - DO NOT USE
@pytest.fixture
def config():
    return NakalaConfig(
        api_key="test-key",
        api_url="https://apitest.nakala.fr",
        base_path="/tmp"  # ❌ SECURITY RISK
    )
```

### ✅ **DO THIS INSTEAD** (Secure)
```python
# SECURE CODE - USE THIS PATTERN
@pytest.fixture
def config():
    """Configuration with secure temporary directory."""
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        yield NakalaConfig(
            api_key="test-key",
            api_url="https://apitest.nakala.fr",
            base_path=temp_dir  # ✅ SECURE
        )
```

## 🚨 Security Vulnerabilities of `/tmp`

### Race Condition Attacks
- `/tmp` is world-writable (permissions 1777)
- Multiple processes can create files with the same name
- Attackers can predict temporary file names

### Symlink Attacks
- Malicious users can create symbolic links in `/tmp`
- Links can point to sensitive system files
- Code following symlinks may read/write unintended files

### Information Disclosure
- Files in `/tmp` may be readable by other users
- Sensitive test data could be exposed
- Temporary files may persist after test completion

## 🛡️ Secure Alternatives

### 1. `tempfile.TemporaryDirectory()` (Recommended)
```python
import tempfile

# Creates secure directory with proper permissions (700)
with tempfile.TemporaryDirectory() as temp_dir:
    # temp_dir is automatically cleaned up
    config = NakalaConfig(base_path=temp_dir)
```

### 2. `tempfile.mkdtemp()` (Manual Cleanup)
```python
import tempfile
import shutil

# Creates secure directory but requires manual cleanup
temp_dir = tempfile.mkdtemp()
try:
    config = NakalaConfig(base_path=temp_dir)
    # ... test code ...
finally:
    shutil.rmtree(temp_dir)  # Manual cleanup required
```

### 3. Pytest's `tmp_path` Fixture (Built-in)
```python
def test_function(tmp_path):
    """Use pytest's built-in secure temporary directory."""
    config = NakalaConfig(base_path=str(tmp_path))
    # tmp_path is automatically cleaned up
```

## 🔍 Security Checklist for Tests

### File Operations
- [ ] Never use `/tmp` directly
- [ ] Use `tempfile.TemporaryDirectory()` or `tmp_path`
- [ ] Ensure proper file permissions (600 for files, 700 for directories)
- [ ] Clean up temporary files after tests

### Path Handling
- [ ] Validate all user-provided paths
- [ ] Use absolute paths to prevent directory traversal
- [ ] Sanitize filenames to prevent injection attacks
- [ ] Never trust user input for file paths

### Permission Management
- [ ] Store original permissions before modification
- [ ] Restore original permissions after testing
- [ ] Use least privilege principle (minimum required permissions)
- [ ] Never set world-readable/writable permissions unnecessarily

## 📋 Security Code Review Checklist

When reviewing test code, check for:

1. **Temporary Directory Usage**
   - [ ] No hardcoded `/tmp` paths
   - [ ] Uses secure temporary directory creation
   - [ ] Proper cleanup mechanisms in place

2. **File Permission Handling**
   - [ ] No overly permissive permissions (like 0o777)
   - [ ] Original permissions preserved and restored
   - [ ] Test isolation maintained

3. **Path Validation**
   - [ ] No path traversal vulnerabilities
   - [ ] Input sanitization for user-provided paths
   - [ ] Absolute path usage where appropriate

4. **Cleanup and Resource Management**
   - [ ] Temporary resources properly cleaned up
   - [ ] No resource leaks in error conditions
   - [ ] Exception handling includes cleanup

## 🚨 Emergency Response

If you discover a security vulnerability in tests:

1. **Immediate Action**
   - Stop using the vulnerable code immediately
   - Do not commit the vulnerable code
   - Replace with secure alternatives

2. **Assessment**
   - Determine scope of vulnerability
   - Check if issue exists in production code
   - Document the security impact

3. **Remediation**
   - Apply secure coding patterns
   - Test the fix thoroughly
   - Update documentation and guidelines

## 📚 Additional Resources

- [Python `tempfile` Documentation](https://docs.python.org/3/library/tempfile.html)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [CWE-377: Insecure Temporary File](https://cwe.mitre.org/data/definitions/377.html)
- [CWE-59: Improper Link Resolution](https://cwe.mitre.org/data/definitions/59.html)

---

**Remember: Security in testing is as important as security in production code!** 🔒