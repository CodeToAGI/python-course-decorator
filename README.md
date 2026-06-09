# Episode 17 Challenge — `@retry(n)` Decorator

> **CodeToAGI** · Python to Agentic AI — Free Course  
> 📺 [Watch Episode 17 on YouTube](https://youtube.com/@CodeToAGI) · Mahaz Abbasi

---

## 🎯 The Challenge

Build a `@retry(n)` decorator that **automatically retries any failing function** up to `n` times before giving up.

This is a **real production pattern** — used in API clients, database connectors, and cloud SDKs everywhere.

---

## ✅ Requirements

| Step | Requirement |
|------|-------------|
| 1 | `@retry(n)` retries a failing function up to `n` times |
| 2 | Print the attempt number every time it retries |
| 3 | If all `n` retries fail, raise the original exception |
| 4 | Use `@functools.wraps` inside the decorator |
| 5 | Test with a function that randomly raises `ValueError` |

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/codetoagi-ep17-challenge.git
cd codetoagi-ep17-challenge

# No dependencies — pure Python 3.x
python retry_decorator.py
```

### Expected output

```
── Test 1: unstable_api_call() — random 70% failure rate ──
  ✗  Attempt 1/5 failed: API timeout — server not responding
     Retrying...
  ✗  Attempt 2/5 failed: API timeout — server not responding
     Retrying...
  ✓  'unstable_api_call' succeeded on attempt 3/5
  Result: {'status': 'ok', 'data': 'user profile loaded'}

── Test 2: always_fails() — expects ConnectionError ────────
  ✗  Attempt 1/3 failed: Database connection refused
     Retrying...
  ✗  Attempt 2/3 failed: Database connection refused
     Retrying...
  ✗  Attempt 3/3 failed: Database connection refused
  ✗  'always_fails' failed after 3 attempt(s). Giving up.
  Caught expected error: Database connection refused

── Test 3: succeeds_on_third() — fails twice then passes ───
  ✗  Attempt 1/5 failed: Not ready yet (internal count: 1)
     Retrying...
  ✗  Attempt 2/5 failed: Not ready yet (internal count: 2)
     Retrying...
  ✓  'succeeds_on_third' succeeded on attempt 3/5
  Result: Ready! Returning data on attempt 3.
```

---

## 🧠 How It Works

```
@retry(3)
def my_function():
    ...
```

```
retry(3)          ← factory: returns a decorator
  └── decorator   ← outer: receives the function
        └── wrapper  ← inner: runs before & after
              └── func()  ← original function call
```

`retry(n)` needs **three layers** because it takes an argument:

```python
def retry(n):                      # Layer 1 — factory (takes n)
    def decorator(func):           # Layer 2 — outer  (takes func)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # Layer 3 — inner (runs on call)
            for attempt in range(1, n + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt}/{n} failed: {e}")
            raise last_exception
        return wrapper
    return decorator
```

---

## 📁 Files

```
ep17-challenge/
├── retry_decorator.py   ← complete solution + 4 test cases + bonus
└── README.md            ← this file
```

### What's inside `retry_decorator.py`

| Section | What it covers |
|---------|---------------|
| `@retry(n)` | Core solution — all 5 challenge steps |
| `unstable_api_call` | Random 70% failure — simulates a flaky API |
| `always_fails` | Proves exception is re-raised after `n` attempts |
| `succeeds_on_third` | Deterministic — fails twice, succeeds on attempt 3 |
| `@retry_with_delay` | **Bonus** — adds a delay between retries |
| `check_identity()` | Verifies `@functools.wraps` preserved `__name__` and `__doc__` |

---

## 💡 Real-World Uses

- **API calls** — retry on `429 Too Many Requests` or `503 Service Unavailable`
- **Database writes** — retry on deadlocks or connection drops
- **File I/O** — retry on temporary lock errors
- **Cloud SDKs** — AWS, GCP, Azure all use this pattern internally

```python
# Real usage example
import requests

@retry(n=3)
def fetch_user(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    response.raise_for_status()   # raises on 4xx/5xx — triggers retry
    return response.json()
```

---

## 📚 Full Series — Python to Agentic AI

| Episode | Topic |
|---------|-------|
| EP 14 | OOP Basics |
| EP 15 | OOP Part 2 |
| EP 16 | Iterators & Generators |
| **EP 17** | **Decorators ← you are here** |
| EP 18 | Async & Await *(coming next)* |
| EP 19 | Context Managers |
| ... | → AGI |

🔔 **Subscribe** — new episode every day → [youtube.com/@CodeToAGI](https://youtube.com/@CodeToAGI)

---

## 💬 Share Your Solution

Paste your `@retry` code in the **YouTube comments** — Mahaz replies to every one.

---

*CodeToAGI · Mahaz Abbasi*
