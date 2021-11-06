## Slow requests:
  Many APIs will throttle and potentially ban users for hitting their endpoints to fast or often.
  Don't get yourself throttled or banned, slow your requests down.

### Features: 
  - concurrent requests
  - single dependency (requests)


### Installation:
```
  pip install slow-requests
```

### Usage:

#### Set per second threshold
```python
  from slow_requests import SlowRequests

  # 10 requests per second
  sl = SlowRequests(offset=10, per_second=True)

  url = "https://jsonplaceholder.typicode.com/todos/1"
  urls = [url] * 100

  for response in sl.execute(requests=urls):
    # do what you like with the response
```

#### Wait per request
```python
  from slow_requests import SlowRequests

  # wait 2 seconds per request
  sl = SlowRequests(offset=2)

  url = "https://jsonplaceholder.typicode.com/todos/1"
  urls = [url] * 100

  for response in sl.execute(requests=urls):
    # do what you like with the response
```