# Take-Home Assignment

**Time Expectations**: This assessment is designed to take approximately 2 hours, but it's fine to spend more or less time as needed. We're not looking for you to go wild here—focus on quality over quantity and demonstrate senior-level engineering judgment. Don't feel pressured to set a timer or rush if you're running a bit behind.

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

## Priority 1: Security Review & Fixes (45-60 minutes)

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

## Priority 2: Feature Implementation (40-50 minutes)

Choose **ONE** of the following to implement:

- **Filtering**: Add ability to filter todos by completion status (all, active, completed)
- **Search**: Implement search functionality to find todos by title

**Requirements:**
- **Must implement in the backend**: Add API endpoint(s) to support your feature
- **Must implement in the frontend**: Add UI components to use the new API
- Consider edge cases and error handling
- Document any design decisions or trade-offs

**Note**: Frontend-only implementations (e.g., filtering client-side) do not meet the requirements. The feature must be implemented in both frontend and backend.

## Priority 3: Documentation (15-20 minutes)

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

## LLM Assistance

If you choose to use LLM assistance (ChatGPT, Claude, Copilot, etc.), please disclose this in your `SOLUTION.md`:
- Which LLM(s) you used
- How you prompted it (brief description of your prompts)
- What contributions you made beyond the LLM output (what you had to fix, modify, or add)

We're evaluating your problem-solving approach and engineering judgment, so understanding how you worked with tools is valuable context.

## SOLUTION.md

Fill in the `SOLUTION.md` file in the root directory with your findings and approach. The file already exists with a template structure - simply replace the placeholder text with your answers.

Good luck!

