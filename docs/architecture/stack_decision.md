# Stack Decision Record (M0)

## Decision

Use a single-language implementation for v1:

- Numerical backend: Python (`numpy`, `scipy`)
- UI: Python web UI (Streamlit)

## Why This Is Recommended

- Lowest risk for a 7-week schedule.
- Best fit for matrix-heavy algorithms and rapid iteration.
- Cross-platform by default through browser access.
- Simplifies onboarding for teammates new to toolchains.

## Options Compared

### Option A: Python backend + Python web UI (Chosen)

Pros:
- Fast development for GS/NR/fault methods.
- Simple deployment (`pip install` + run command).
- Easier debugging and testing.

Cons:
- UI styling flexibility is lower than native frameworks.

### Option B: Python backend + C++ UI (Deferred)

Pros:
- Potentially richer native desktop UX.
- Strong performance for UI rendering.

Cons:
- Two-language integration overhead.
- API/IPC boundary design and testing effort.
- More complex multi-platform packaging.

## If C++ UI Is Required Later

Use this boundary:

- Python process owns all engineering math and data model.
- C++ UI talks to Python via local HTTP/JSON API.
- Keep protocol stable and versioned.

This keeps solver correctness centralized while allowing future UI replacement.
