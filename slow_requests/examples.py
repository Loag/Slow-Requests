from slow_requests import SlowRequests
from timeit import default_timer as timer
from datetime import timedelta

def ten_gets_per_second():
  # setup to do 10 per second
  sl = SlowRequests(offset=10, per_second=True)

  url = "https://jsonplaceholder.typicode.com/todos/1"
  test_data = [url] * 100

  start = timer()
  count = 0
  for res in sl.execute(requests=test_data):
    end = timer()
    # if the total execution has been less than 1 second decrement the count
    print(timedelta(seconds=end-start).total_seconds())
    count += 1

  end = timer()
  print("******************************************")
  print(timedelta(seconds=end-start).total_seconds())
  print("******************************************")



if __name__ == '__main__':
  ten_gets_per_second()