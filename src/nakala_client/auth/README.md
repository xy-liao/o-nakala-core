# O-Nakala Core Authentication System

## 🔐 Comprehensive SSO and Institutional Authentication

Complete authentication system supporting SAML 2.0, OAuth 2.0, and institutional user management for digital humanities institutions.

## 📋 Features

### 🏛️ Institutional SSO Support
- **SAML 2.0**: Full SAML authentication with institutional Identity Providers
- **OAuth 2.0**: Modern OAuth flow with OIDC support
- **Pre-configured institutions**: EFEO, BnF, Université de Strasbourg, Huma-Num
- **Custom configurations**: Support for additional institutions

### 👥 User Management
- **Institutional roles**: Student, Researcher, Professor, Librarian, Archivist, Curator, Admin
- **Role-based permissions**: Fine-grained access control for different operations
- **User profiles**: Complete user context with institutional affiliation
- **Activity tracking**: Comprehensive audit trail for all user actions

### 🔑 Session Management
- **Secure sessions**: JWT and session cookie support
- **Session limits**: Configurable concurrent session limits per user
- **Auto-expiration**: Automatic cleanup of expired sessions
- **Cross-platform**: Works with CLI tools and web interfaces

### 🛡️ Security Features
- **2FA support**: Two-factor authentication for sensitive institutions
- **Domain validation**: Email domain restrictions for institutional users
- **API key management**: Secure API key generation and validation
- **Audit logging**: Complete activity logs for compliance

## 🚀 Quick Start

### Basic Usage

```python
from nakala_client.auth import InstitutionalAuthManager, AuthMiddleware

# Initialize authentication
auth_manager = InstitutionalAuthManager()
auth_middleware = AuthMiddleware()

# Authenticate user via SSO
auth_result = auth_manager.authenticate_user('efeo', callback_data)
if auth_result.success:
    user_profile = auth_result.user_profile
    print(f"Welcome {user_profile.name} from {user_profile.institution}")
```

### CLI Authentication

```python
from nakala_client.auth import require_researcher_role

@require_researcher_role
def upload_data(api_key: str, dataset_path: str, user_profile=None):
    print(f"User {user_profile.name} uploading data...")
    # Your upload logic here
```

### Web Authentication

```python
from nakala_client.auth import AuthMiddleware

auth = AuthMiddleware()

@auth.require_auth(required_roles=['researcher', 'professor'])
def create_collection(request, user_profile=None):
    print(f"Creating collection for {user_profile.institution}")
    # Your collection creation logic here
```

## 🏛️ Supported Institutions

### École française d'Extrême-Orient (EFEO)
```python
# Pre-configured SAML authentication
auth_url = auth_manager.get_auth_url('efeo', redirect_uri)
```

### Bibliothèque nationale de France (BnF)
```python
# Pre-configured OAuth 2.0 authentication
auth_url = auth_manager.get_auth_url('bnf', redirect_uri)
```

### Université de Strasbourg
```python
# University SAML authentication
auth_url = auth_manager.get_auth_url('unistra', redirect_uri)
```

### Huma-Num
```python
# Research consortium OAuth authentication
auth_url = auth_manager.get_auth_url('huma_num', redirect_uri)
```

## 📊 User Roles and Permissions

### Role Hierarchy
- **Admin**: Full system access
- **Professor**: Research + teaching permissions
- **Researcher**: Data upload + collection management
- **Curator**: Metadata curation + quality control
- **Librarian**: Collection organization + access management
- **Archivist**: Long-term preservation + metadata standards
- **Student**: Basic data upload + viewing
- **Guest**: Read-only access

### Permission Matrix
| Action | Student | Researcher | Professor | Librarian | Admin |
|--------|---------|------------|-----------|-----------|-------|
| Upload Data | ✅ | ✅ | ✅ | ✅ | ✅ |
| Create Collections | ❌ | ✅ | ✅ | ✅ | ✅ |
| Modify Metadata | ❌ | ✅ | ✅ | ✅ | ✅ |
| Delete Data | ❌ | ❌ | ❌ | ❌ | ✅ |
| Manage Users | ❌ | ❌ | ❌ | ❌ | ✅ |
| View Analytics | ❌ | ✅ | ✅ | ✅ | ✅ |

## 🔧 Configuration

### Institutional Policy Configuration

```python
from nakala_client.auth import InstitutionalPolicy, InstitutionalRole

# Create custom institutional policy
policy = InstitutionalPolicy(
    institution='my_university',
    require_2fa=True,
    allowed_domains=['university.edu'],
    session_timeout=3600,
    default_roles=[InstitutionalRole.STUDENT],
    role_mapping={
        'faculty': [InstitutionalRole.PROFESSOR, InstitutionalRole.RESEARCHER],
        'grad_student': [InstitutionalRole.RESEARCHER],
        'undergrad': [InstitutionalRole.STUDENT]
    },
    max_upload_size=50 * 1024 * 1024 * 1024,  # 50GB
    allowed_file_types=['pdf', 'doc', 'jpg', 'png', 'csv']
)

# Add to authentication manager
auth_manager.add_institution('my_university', policy, sso_config)
```

### SAML Configuration

```python
saml_config = {
    'name': 'My University',
    'type': 'saml',
    'entity_id': 'https://nakala.university.edu',
    'sso_url': 'https://idp.university.edu/saml2/sso',
    'certificate': '/path/to/certificate.pem',
    'attribute_map': {
        'user_id': 'eduPersonPrincipalName',
        'email': 'mail',
        'name': 'displayName',
        'institution': 'schacHomeOrganization',
        'roles': 'eduPersonAffiliation'
    }
}
```

### OAuth 2.0 Configuration

```python
oauth_config = {
    'name': 'My Institution',
    'type': 'oauth',
    'client_id': 'your_client_id',
    'client_secret': 'your_client_secret',
    'auth_url': 'https://auth.institution.org/oauth2/authorize',
    'token_url': 'https://auth.institution.org/oauth2/token',
    'userinfo_url': 'https://auth.institution.org/oauth2/userinfo',
    'scope': 'openid profile email institution'
}
```

## 🔌 Integration Examples

### CLI Tool Integration

```python
#!/usr/bin/env python3
"""CLI tool with institutional authentication."""

import click
from nakala_client.auth import AuthMiddleware, require_upload_permissions

@click.command()
@click.option('--api-key', help='API key or use SSO')
@click.option('--institution', help='Institution for SSO')
@require_upload_permissions
def upload_command(api_key, institution, user_profile=None):
    """Upload data with authentication."""
    print(f"Authenticated as {user_profile.name} ({user_profile.institution})")
    # Upload logic here
```

### Web Application Integration

```python
from flask import Flask, request, session
from nakala_client.auth import AuthMiddleware

app = Flask(__name__)
auth = AuthMiddleware()

@app.route('/api/collections', methods=['POST'])
@auth.require_auth(required_permissions=['create_collection'])
def create_collection_api(user_profile=None):
    """Create collection via web API."""
    data = request.json
    
    # Log user activity
    auth.log_user_activity(
        user_profile=user_profile,
        action='collection_created',
        resource=data.get('title', ''),
        metadata={'collection_type': data.get('type')}
    )
    
    return {'status': 'success', 'user': user_profile.name}
```

## 📈 Analytics and Monitoring

### User Activity Tracking

```python
from nakala_client.auth import UserManager

user_manager = UserManager()

# Get user activity
activities = user_manager.get_user_activity(
    user_id='user123',
    limit=50,
    start_date=datetime.now() - timedelta(days=30)
)

# Get user statistics
stats = user_manager.get_user_stats('user123')
print(f"Total uploads: {stats.total_uploads}")
print(f"Quality score: {stats.quality_score}")
```

### Session Analytics

```python
from nakala_client.auth import SessionManager

session_manager = SessionManager()

# Get session statistics
stats = session_manager.get_session_stats()
print(f"Active sessions: {stats['active_sessions']}")
print(f"Sessions by institution: {stats['sessions_by_institution']}")
```

## 🛠️ Advanced Features

### Custom Authentication Providers

```python
from nakala_client.auth import SSOProvider, AuthenticationResult

class CustomSSOProvider(SSOProvider):
    """Custom institutional authentication provider."""
    
    def handle_callback(self, callback_data):
        # Custom authentication logic
        return AuthenticationResult(
            success=True,
            user_id=user_id,
            email=email,
            name=name,
            institution=self.provider_name,
            roles=roles,
            attributes=attributes
        )
```

### Role-based Decorators

```python
from nakala_client.auth import require_admin_role, require_efeo_auth

@require_admin_role
def delete_user(user_id: str, user_profile=None):
    """Admin-only function."""
    pass

@require_efeo_auth
def efeo_specific_function(data: dict, user_profile=None):
    """EFEO institution-specific function."""
    pass
```

## 🔍 Troubleshooting

### Common Issues

1. **SAML Certificate Validation**
   ```python
   # Disable certificate validation for testing
   provider.verify_ssl = False
   ```

2. **OAuth Scope Issues**
   ```python
   # Add additional scopes
   oauth_config['scope'] = 'openid profile email groups'
   ```

3. **Session Timeout**
   ```python
   # Extend session timeout
   session_manager.default_session_timeout = 7200  # 2 hours
   ```

### Debug Mode

```python
import logging
logging.getLogger('nakala_client.auth').setLevel(logging.DEBUG)
```

## 📚 Dependencies

- `PyJWT`: JWT token handling
- `requests`: HTTP client for OAuth
- `lxml`: XML processing for SAML
- `cryptography`: Security functions

## 🔐 Security Considerations

- Store JWT secrets securely (`~/.nakala/jwt_secret`)
- Use HTTPS for all authentication endpoints
- Implement proper CSRF protection for web interfaces
- Regular rotation of API keys and certificates
- Monitor failed authentication attempts

## 📖 API Reference

### Core Classes

- `InstitutionalAuthManager`: Main authentication coordinator
- `SSOProvider`: Base class for authentication providers
- `SAMLProvider`: SAML 2.0 authentication
- `OAuthProvider`: OAuth 2.0 authentication
- `UserManager`: User profile and activity management
- `SessionManager`: Session lifecycle management
- `AuthMiddleware`: Request authentication middleware

### Decorators

- `@require_auth()`: Basic authentication requirement
- `@require_institutional_auth()`: Institutional authentication
- `@require_researcher_role`: Researcher role requirement
- `@require_admin_role`: Admin role requirement
- `@require_upload_permissions`: Upload permission requirement

---

**Production Ready**: This authentication system is designed for institutional use with enterprise-grade security features and comprehensive audit capabilities.