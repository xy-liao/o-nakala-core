⏺ Strategic Development Plan for O-Nakala Core

  Phase 1: Foundation Stabilization (Priority 1)

  1.1 Code Quality & Standards

  # Immediate actions
  black src/                          # Auto-fix formatting
  flake8 src/ --extend-ignore=E501   # Check remaining issues
  mypy src/ --ignore-missing-imports # Type checking

  Benefits: Clean, maintainable codebase foundation

  1.2 Core Module Testing

  Focus on critical paths first:
  - src/nakala_client/upload.py (0% coverage → 80%+)
  - src/nakala_client/collection.py (0% coverage → 80%+)
  - src/nakala_client/common/config.py (54% → 90%+)
  - src/nakala_client/common/utils.py (41% → 80%+)

  Phase 2: Feature Completion (Priority 2)

  2.1 CLI Implementation

  Current CLI modules are stubs (33% coverage). Complete:
  # Priority order:
  1. nakala-upload     # Core functionality
  2. nakala-collection # Collection management  
  3. nakala-curator    # Metadata management
  4. nakala-user-info  # User operations

  2.2 Integration Testing

  # Test with real API endpoints
  export NAKALA_API_KEY="test-key"
  export NAKALA_BASE_URL="https://apitest.nakala.fr"

  # End-to-end workflow tests
  pytest tests/integration/ -v --real-api

  Phase 3: Advanced Features (Priority 3)

  3.1 Authentication System

  Currently 0% coverage on auth modules:
  - auth/session_manager.py
  - auth/institutional_auth.py
  - auth/sso_provider.py

  3.2 AI/ML Features

  Lower priority advanced modules:
  - autonomous_generator.py (19% coverage)
  - collaborative_intelligence.py (16% coverage)
  - predictive_analytics.py (19% coverage)

  Recommended Action Plan

  Week 1-2: Quality Foundation

  # 1. Fix code formatting
  black src/ && git commit -am "Fix code formatting"

  # 2. Address critical linting issues  
  flake8 src/ --select=E9,F63,F7,F82 # Critical errors only

  # 3. Add basic type annotations
  mypy src/nakala_client/common/ --strict

  Week 3-4: Core Functionality

  # 1. Complete upload module
  pytest tests/unit/test_upload.py -v --cov=src/nakala_client/upload.py

  # 2. Complete collection module  
  pytest tests/unit/test_collection.py -v --cov=src/nakala_client/collection.py

  # 3. End-to-end workflow testing
  python examples/sample_dataset/test_complete_workflow.py

  Week 5-6: CLI & Integration

  # 1. Complete CLI implementations
  nakala-upload --dataset examples/sample_dataset/folder_data_items.csv --dry-run

  # 2. Integration testing with test API
  pytest tests/integration/ -v --api-endpoint=test

  # 3. Documentation update

  Development Priorities Matrix

  | Priority | Component         | Current Status | Target        | Business Impact      |
  |----------|-------------------|----------------|---------------|----------------------|
  | P0       | Code formatting   | Many issues    | Clean         | Developer efficiency |
  | P0       | Upload module     | 0% coverage    | 80%           | Core functionality   |
  | P0       | Collection module | 0% coverage    | 80%           | Core functionality   |
  | P1       | CLI commands      | 33% coverage   | 90%           | User experience      |
  | P1       | Integration tests | Minimal        | Comprehensive | Reliability          |
  | P2       | Auth system       | 0% coverage    | 60%           | Security             |
  | P3       | AI/ML features    | 16-19%         | 40%           | Advanced features    |

  Success Metrics

  Short-term (1 month):
  - Code coverage: 14% → 60%
  - Linting violations: 400+ → <50
  - Working CLI commands: 4/4 functional

  Medium-term (3 months):
  - Complete upload/collection workflows
  - Integration test suite
  - Documentation completion

  Long-term (6 months):
  - Authentication system
  - Advanced AI features
  - Production readiness