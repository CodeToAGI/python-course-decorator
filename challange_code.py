"""
╔══════════════════════════════════════════════════════════════════╗
║  CodeToAGI — Episode 17 Challenge                                ║
║  Build @retry(n) — Auto-retry any function on failure            ║
║  youtube.com/@CodeToAGI  |  Mahaz Abbasi                         ║
╚══════════════════════════════════════════════════════════════════╝
"""

import functools
import random
import time


# ══════════════════════════════════════════════════════════════════
#  CHALLENGE SOLUTION — @retry(n)
# ══════════════════════════════════════════════════════════════════

def retry(n):
    """
    Decorator factory: retries the wrapped function up to n times on failure.

    Steps implemented:
      ✅ Step 1 — retry a failing function up to n times
      ✅ Step 2 — print the attempt number on every retry
      ✅ Step 3 — if all n retries fail, raise the original exception
      ✅ Step 4 — uses @functools.wraps to preserve function identity
      ✅ Step 5 — tested with a function that randomly raises ValueError
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, n + 1):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 1:
                        print(f"  ✓  '{func.__name__}' succeeded on attempt {attempt}/{n}")
                    return result
                except Exception as e:
                    last_exception = e
                    print(f"  ✗  Attempt {attempt}/{n} failed: {e}")
                    if attempt < n:
                        print(f"     Retrying...")
            # All n attempts exhausted — re-raise the last exception
            print(f"  ✗  '{func.__name__}' failed after {n} attempt(s). Giving up.")
            raise last_exception
        return wrapper
    return decorator


# ══════════════════════════════════════════════════════════════════
#  TEST 1 — Random failure (Step 5 requirement)
# ══════════════════════════════════════════════════════════════════

@retry(5)
def unstable_api_call():
    """Simulates an API call that randomly fails 70% of the time."""
    if random.random() < 0.7:
        raise ValueError("API timeout — server not responding")
    return {"status": "ok", "data": "user profile loaded"}


# ══════════════════════════════════════════════════════════════════
#  TEST 2 — Always fails (proves exception is re-raised after n tries)
# ══════════════════════════════════════════════════════════════════

@retry(3)
def always_fails():
    """Simulates a broken endpoint that never recovers."""
    raise ConnectionError("Database connection refused")


# ══════════════════════════════════════════════════════════════════
#  TEST 3 — Succeeds on 3rd attempt (deterministic)
# ══════════════════════════════════════════════════════════════════

_call_count = 0

@retry(5)
def succeeds_on_third():
    """Fails twice, then succeeds — tests the retry counter."""
    global _call_count
    _call_count += 1
    if _call_count < 3:
        raise RuntimeError(f"Not ready yet (internal count: {_call_count})")
    _call_count = 0   # reset for re-use
    return "Ready! Returning data on attempt 3."


# ══════════════════════════════════════════════════════════════════
#  BONUS — @retry with delay between retries
# ══════════════════════════════════════════════════════════════════

def retry_with_delay(n, delay=1.0):
    """
    Extended version: waits `delay` seconds between each retry.
    Useful for rate-limited APIs or transient network errors.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, n + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"  ✗  Attempt {attempt}/{n} failed: {e}")
                    if attempt < n:
                        print(f"     Waiting {delay}s before retry...")
                        time.sleep(delay)
            print(f"  ✗  '{func.__name__}' failed after {n} attempt(s). Giving up.")
            raise last_exception
        return wrapper
    return decorator


@retry_with_delay(n=3, delay=0.5)
def flaky_database_write(record):
    """Simulates a database write that randomly fails."""
    if random.random() < 0.6:
        raise IOError("Deadlock detected — transaction rolled back")
    return f"Record '{record}' written successfully."


# ══════════════════════════════════════════════════════════════════
#  VERIFY: @functools.wraps preserves function identity
# ══════════════════════════════════════════════════════════════════

def check_identity():
    print("\n── Identity check (@functools.wraps) ──────────────────────")
    print(f"  unstable_api_call.__name__ = '{unstable_api_call.__name__}'")
    print(f"  unstable_api_call.__doc__  = '{unstable_api_call.__doc__[:45]}...'")
    print(f"  Expected name: 'unstable_api_call'  ✓" 
          if unstable_api_call.__name__ == "unstable_api_call" else "  ✗ wraps not applied!")


# ══════════════════════════════════════════════════════════════════
#  RUNNER
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    print("\n╔══════════════════════════════════════════╗")
    print("║  @retry(n) — Challenge Demo               ║")
    print("║  CodeToAGI  Episode 17                    ║")
    print("╚══════════════════════════════════════════╝\n")

    # ── Test 1: random failures ──────────────────────────────────
    print("── Test 1: unstable_api_call() — random 70% failure rate ──")
    try:
        result = unstable_api_call()
        print(f"  Result: {result}\n")
    except ValueError as e:
        print(f"  Final error: {e}\n")

    # ── Test 2: always fails ─────────────────────────────────────
    print("── Test 2: always_fails() — expects ConnectionError ────────")
    try:
        always_fails()
    except ConnectionError as e:
        print(f"  Caught expected error: {e}\n")

    # ── Test 3: deterministic 3rd-attempt success ────────────────
    print("── Test 3: succeeds_on_third() — fails twice then passes ───")
    try:
        result = succeeds_on_third()
        print(f"  Result: {result}\n")
    except RuntimeError as e:
        print(f"  Unexpected failure: {e}\n")

    # ── Bonus: retry with delay ──────────────────────────────────
    print("── Bonus: flaky_database_write() — 0.5s delay between tries ")
    try:
        result = flaky_database_write("user_42")
        print(f"  Result: {result}\n")
    except IOError as e:
        print(f"  Final error after retries: {e}\n")

    # ── Identity verification ────────────────────────────────────
    check_identity()

    print("\n  Done! Drop your own version in the YouTube comments 👇")
    print("  youtube.com/@CodeToAGI\n")
