from abc import ABC, abstractmethod
import requests

class Notifier(ABC):
    @abstractmethod
    def send(self, message: str):
        pass

    def notify(self, message: str, job_name: str = "Job"):
        """Default formatting; subclasses may override."""
        from datetime import datetime
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.send(f"{job_name}: {message}\n{ts}")

    def wrap(self, func, job_name="Job"):
        import traceback
        from datetime import datetime

        def wrapped(*args, **kwargs):
            start = datetime.now()
            self.notify("started 🚀", job_name)

            try:
                result = func(*args, **kwargs)
            except Exception:
                self.notify(
                    f"failed ❌\n```\n{traceback.format_exc()}\n```",
                    job_name
                )
                raise

            end = datetime.now()
            duration = end - start
            self.notify(f"finished ✅\nDuration: {duration}", job_name)
            return result

        return wrapped

    def decorator(self, job_name="Job"):
        def wrapper(func):
            return self.wrap(func, job_name)
        return wrapper
    
class DiscordNotifier(Notifier):
    def __init__(self, webhook: str):
        self.webhook = webhook

    def send(self, message: str):
        r = requests.post(self.webhook, json={"content": message})
        if r.status_code not in (200, 204):
            raise RuntimeError(
                f"Discord returned {r.status_code}: {r.text}"
            )
        
PrimaryNotifier = DiscordNotifier(webhook="your_discord_webhook_url_here")

if __name__ == "__main__":
    @PrimaryNotifier.decorator("Example Job")
    def example_job():
        import time
        time.sleep(30)
        print("Job is running...")
        # Uncomment the next line to simulate a failure
        # raise ValueError("Simulated error")

    example_job()