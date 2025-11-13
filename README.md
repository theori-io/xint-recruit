# Take-Home Assignment

A simple full-stack application with React frontend, FastAPI backend, and Redis database.

## Project Structure

```
xint-recruit/
├── frontend/          # React + TypeScript + Vite
├── backend/           # FastAPI + Python
├── compose.yaml       # Docker Compose configuration
└── README.md
```

## Features

- **Frontend**: React application with TypeScript
- **Backend**: FastAPI REST API with JWT authentication
- **Database**: Redis for data storage
- **Containerized**: Docker Compose setup for easy development

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 22+ (for local frontend development)
- Python 3.13+ (for local backend development)

### Running with Docker Compose

```bash
docker compose up
```

This will start:
- Frontend on http://localhost:3000
- Backend API on http://localhost:8000
- Redis on localhost:6379

### Running Locally

#### Backend

```bash
cd backend
uv sync  # Install dependencies
uv run python -m uvicorn main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Authentication

The application uses JWT-based authentication. A default test user is created on startup:

- **Username**: `testuser`
- **Password**: `testpass123`

You can log in through the frontend interface. The authentication system is already implemented, but you may need to review and improve it as part of the assignment.

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

## Assignment

**Time Expectations**: This assessment is designed to take approximately 2 hours, but it's fine to spend more or less time as needed. We're not looking for you to go wild here—focus on quality over quantity and demonstrate senior-level engineering judgment. Don't feel pressured to set a timer or rush if you're running a bit behind.

### Priority 1: Security Review & Fixes (45-60 minutes)

The codebase has security vulnerabilities that need to be identified and fixed. Please address the following:

1. **Authorization Issue**: Users report seeing todos that don't belong to them. Investigate and fix this issue.
   - Test with multiple user accounts (see "Testing with Multiple Users" below)
   - Ensure users can only access their own todos
   - Fix this in the backend API

2. **XSS Vulnerability**: Review the frontend code for cross-site scripting vulnerabilities and fix any issues you find.
   - Implement proper sanitization or use safe rendering methods

**What to do:**
- Review both frontend and backend code
- Fix both security issues
- Document how you discovered each issue and how you fixed it
- Feel free to document any additional security issues you find (though fixing them is optional)

### Priority 2: Feature Implementation (40-50 minutes)

Choose **ONE** of the following to implement:

- **Filtering**: Add ability to filter todos by completion status (all, active, completed)
- **Search**: Implement search functionality to find todos by title

**Requirements:**
- **Must implement in the backend**: Add API endpoint(s) to support your feature
- **Must implement in the frontend**: Add UI components to use the new API
- Consider edge cases and error handling
- Document any design decisions or trade-offs

**Note**: Frontend-only implementations (e.g., filtering client-side) do not meet the requirements. The feature must be implemented in both frontend and backend.

### Priority 3: Documentation (15-20 minutes)

Create a `SOLUTION.md` file documenting:

1. **Security Issues Found & Fixed**:
   - Authorization issue: How you discovered it, why it's a problem, and how you fixed it
   - XSS vulnerability: How you discovered it, why it's a problem, and how you fixed it
   - Any additional security issues you found (optional)

2. **Feature Implementation**:
   - Design decisions and rationale
   - Trade-offs considered
   - How it scales or handles edge cases

3. **Testing & Validation**:
   - How you tested your changes
   - Edge cases considered
   - What you'd test in production

## Testing with Multiple Users

To test authorization issues, you'll need multiple user accounts. A second test user is available:

- **Username**: `testuser2`
- **Password**: `testpass123`

You can also create additional test users using the helper script:

```bash
cd backend
uv run python scripts/create_user.py <username> <password>
```

Or create users programmatically via the API (if you implement user registration) or directly in Redis.

## Known Issues & Areas for Improvement

The following areas are known to need attention (this is intentional for the assessment):

- Authentication and authorization may have some edge cases
- Input validation could be more robust
- Some security best practices may not be fully implemented
- Error handling could be improved

## Getting Started with the Assignment

1. **Create a private repository** from this template:
   - Click "Use this template" → "Create a new repository"
   - Make sure the repository is **private**
   - Clone your new private repository locally

2. **Complete the assignment** (see priorities below)

3. **Create `SOLUTION.md`** with your findings and approach (see template below)

4. **Submit your solution**:
   - Add [@aspcanada](https://github.com/aspcanada) as a collaborator to your private repository

**Privacy Note**: To keep submissions private, please create a private repository from the template rather than forking publicly or creating pull requests.

## LLM Assistance

If you choose to use LLM assistance (ChatGPT, Claude, Copilot, etc.), please disclose this in your `SOLUTION.md`:
- Which LLM(s) you used
- How you prompted it (brief description of your prompts)
- What contributions you made beyond the LLM output (what you had to fix, modify, or add)

We're evaluating your problem-solving approach and engineering judgment, so understanding how you worked with tools is valuable context.

## SOLUTION.md Template

Create a `SOLUTION.md` file in the root directory with the following structure:

```markdown
# Solution Summary

## Security Issues Found & Fixed

### Authorization Issue

- **How I discovered it**: [Code review / Testing with multiple users / etc.]
- **Why it's a problem**: [Brief explanation of risk and impact]
- **How I fixed it**: [Brief description]
- **Location**: [File and line numbers]

### XSS Vulnerability

- **How I discovered it**: [Code review / etc.]
- **Why it's a problem**: [Brief explanation of risk and impact]
- **How I fixed it**: [Brief description]
- **Location**: [File and line numbers]

### Additional Security Issues (Optional)

[If you found any other security issues, document them here]


## Feature Implementation

**Feature**: [Filtering / Search]

**Design Decisions**:
- [Why you chose this approach]
- [API design considerations]
- [Data model changes]

**Trade-offs**:
- [Alternatives considered]
- [Why this approach was chosen]

**Scalability & Edge Cases**:
- [How it handles scale]
- [Edge cases considered]

## Testing & Validation

- **Testing approach**: [How you tested your changes]
- **Edge cases**: [Edge cases tested]
- **Production considerations**: [What you'd test in production]

## Time Spent

- Security review & fixes: [X] minutes
- Feature implementation: [X] minutes  
- Documentation: [X] minutes

## LLM Assistance (if used)

- **LLM(s) used**: [ChatGPT, Claude, Copilot, etc.]
- **How I prompted it**: [Brief description of prompts used]
- **My contributions**: [What I fixed, modified, or added beyond the LLM output]
```

## Evaluation Criteria

Your solution will be evaluated on:

- **Problem-Solving & Judgment (30%)**: 
  - Ability to identify issues (security, code quality, architecture)
  - Prioritization and time management
  - Understanding of trade-offs

- **Code Quality & Engineering (30%)**:
  - Clean, maintainable, well-structured code
  - Proper error handling and edge case consideration
  - Refactoring and code improvements

- **Security Awareness (25%)**:
  - Ability to identify and fix security vulnerabilities
  - Understanding of security implications
  - Application of security best practices

- **Feature Implementation (10%)**:
  - Correct and complete feature implementation
  - Design decisions and API design
  - Consideration of scalability and edge cases

- **Documentation & Communication (5%)**:
  - Clear explanation of findings, decisions, and rationale
  - Ability to articulate trade-offs and considerations

**Note**: For a senior role, we value your engineering judgment. Focus on demonstrating thoughtful problem-solving, clean code, and sound architectural decisions.

Good luck!
