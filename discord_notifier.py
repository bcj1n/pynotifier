import requests

from notifier import PrimaryNotifier

@PrimaryNotifier.decorator(job_name="Test Job")
def test_job():
    sum = 0
    for i in range(500000):
        for j in range(100):
            sum += i - j*100
    print(  f"Sum of is {sum}" )
    return sum

if __name__ == "__main__":
    test_job()