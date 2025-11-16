# pynotifier

Lightweight Python utilities to send notifications for job start, success, failure, and duration. Designed to wrap functions (or be used as a decorator) and send formatted messages to a notifier backend. The repository includes a Discord notifier example.

**Project Summary**
- **Name:**: `pynotifier`
- **Purpose:**: Wrap Python functions to automatically send notifications when a job starts, fails, or finishes (with duration and timestamp).

**Features**
- **Decorator/Wrapper:**: Use `PrimaryNotifier.decorator(job_name="...")` or `PrimaryNotifier.wrap(...)` to automatically notify on start, failure (with traceback), and finish (with duration).
- **Notifier Base:**: `Notifier` is an abstract base class that provides default formatting, `notify()`, `wrap()` and `decorator()` helpers.
- **Discord Integration:**: `DiscordNotifier` implements `send()` to post messages to a Discord webhook using `requests`.

**Files**
- **`notifier.py`**: Contains `Notifier`, `DiscordNotifier`, and a `PrimaryNotifier` instance configured with a webhook string.
- **`discord_notifier.py`**: Example script demonstrating `@PrimaryNotifier.decorator(job_name="Test Job")` around a sample CPU-bound `test_job()`.

**Quick Usage**

1. Install dependency:

```bash
pip install requests
```

2. Replace the webhook in `notifier.py` with your own Discord webhook or (recommended) set an environment variable and update the code to read it.

3. Run the example:

```bash
python discord_notifier.py
```

**Example (decorator)**

```python
@PrimaryNotifier.decorator(job_name="My Job")
def my_job():
	# ... work ...
	return True

my_job()
```

**Formatting & Behavior**
- **Started:** sends `started 🚀` with the job name.
- **Failed:** sends `failed ❌` with a traceback block when an exception is raised.
- **Finished:** sends `finished ✅` with the elapsed duration and timestamp.

**Security / Notes**
- **HTTP errors:** `DiscordNotifier.send()` raises a `RuntimeError` when Discord returns an unexpected status code.