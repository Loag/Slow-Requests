from requests import Request, Session
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import warnings
from time import sleep
from timeit import default_timer as timer
from datetime import timedelta
from threading import local

class SlowRequests:
  '''
    PARAMS:
    * offset: Float Time to wait in ms between requests
    * per_second: Boolean, if true than offset is the amount of requests to make per second instead of waiting per request.
  '''
  def __init__(self, offset=0.1, per_second=False):
    self.__eval_setup(offset, per_second)

    self.offset = offset
    self.per_second = per_second

    self.__requests = [] # the requests

  def __eval_setup(self, offset, per_second):
    if offset < 1 and per_second:
      # turn off per second if you wish to do less than one request per second
      raise ValueError("Turn off per second if you wish to do less than one request per second")

    elif offset > 100 and per_second:
      warnings.warn("You are trying to do over 100 requests per second.")

    elif offset > 300 and not per_second:
      warnings.warn("You are waiting over 5 minutes per request.")

  '''
    PARAMS:
    * url: The URL to make a request to
    * method: HTTP method (optional)
    * body: the request body (optional)
    * headers: request headers (optional)
  '''
  def add(self, url, method=None, body=None, headers=None):
    in_req = InputReqFactory.create(url, method=method, body=body, headers=headers)
    self.__requests.append(in_req)

  '''
    PARAMS:
    * urls: The URLs to request
    * method: HTTP method (optional)
    * bodies: the request bodies to map to urls (optional)
    * headers: request headers to map to urls (optional)
  '''
  def add_many(self, urls, method=None, bodies=None, headers=None):
    in_reqs = InputReqFactory.create_many(urls, method=method, bodies=bodies, headers=headers)
    self.__requests.extend(in_reqs)

  '''
    PARAMS:
    * input_requests: user can just input the requests here instead of having to use add
  '''
  def execute(self, requests=None):
    if not self.__requests and not requests:
      raise IndexError("No Requests")
    
    elif requests:
      self.add_many(requests)
    
    # if in per second mode then use the offset as the amount of req to run per second
    if self.per_second:
      return self.__execute_per_second()

    return self.__execute_per_request()

  '''
    If per second choice was selected, try and execute the reqs concurrently per secoond.

    returns:
      * a generator of request responses
  '''
  def __execute_per_second(self):

    executor = ThreadPoolExecutor()
    thread_local = local()

    def get_session():
        if not hasattr(thread_local, "session"):
            thread_local.session = Session()
        return thread_local.session

    # while there are requests
    while self.__requests:

      # start a new timer:
      start = timer()
      # get a new count
      count = self.offset

      # while we can make requests for this second
      while count:
        # if we run out of requests half way through the count
        if not self.__requests:
          break
        
        # get a request
        req = self.__requests.pop()

        # submit to the executor 
        ex = executor.submit(get_session().send, req.to_req())

        # try to yield the result
        try:
          yield ex.result()      

        except Exception as e:
          print(e)

        # get the ending time
        end = timer()
        # if the total execution has been less than 1 second decrement the count
        if timedelta(seconds=end-start).total_seconds() < 1:
          count -= 1

        # if it has been equal or longer, break out. We will inevitably fall behind here
        else:
          break
      
      # if we completed all of the requests per second before a second elapsed
      end = timer()

      # sleep the rest of the second
      if timedelta(seconds=end-start).total_seconds() < 1:
        sleep(1 - (end-start))

  '''
    if per second not selected, just time out per request.
    returns:
      * a generator of request response
  '''
  def __execute_per_request(self):
    while self.__requests:
      req = self.__requests.pop() # this is a request object 
      yield self.sender_session.send(req.to_req())
      sleep(self.offset)

  '''
    get a specific response for an input? 
  '''
  def response(self, id):
    pass

class InputReqFactory:

  @staticmethod
  def create(url, **input):
    # remove any empty args
    args = {k: v for k, v in input.items() if v is not None}
    return InputReq(url, **args)

  @staticmethod
  def create_many(urls, **input):
    if not isinstance(urls, list):
      raise TypeError("Input must be a list")

    args = {k: v for k, v in input.items() if v is not None}
    return [InputReq(url, **args) for url in urls]


class InputReq:
  '''
    PARAMS:
    * url: String url
    * method: http method to perform
    * headers: header dict for this request
    * body: body to send if post or put
  '''
  def __init__(self, url, method='GET', headers=None, body=None):
    self.url = self.__check_url(url)
    self.method = self.__check_method(method)
    self.headers = self.__check_headers(headers) 
    self.body = self.__check_body(method, body)

  # returned a prepared request object
  def to_req(self):
    req = Request(url=self.url, method=self.method, headers=self.headers)
    p_req = req.prepare()

    if self.body:
      p_req.body = self.body

    return p_req

  def __check_method(self, method):
    method = method.upper()
    if method not in ["GET", "POST", "PUT", "DELETE"]:
      raise TypeError("Unsupported method: " + method)
    return method

  def __check_headers(self, headers):
    if headers:
      if isinstance(headers, dict):
        return headers
      raise TypeError("Headers must be a dict")

  def __check_body(self, method, body):
    if body and method.upper() not in ["POST", "PUT"]:
      raise RuntimeError("Body required post or put method")
    return body

  def __check_url(self, url):
    if self.__is_string(url) and self.__is_url(url):
      return url

  def __is_string(self, input):
    if isinstance(input, str):
      return True
    raise TypeError("input url must be a string")

  def __is_url(self, url):
    try:
      result = urlparse(url)
      return all([result.scheme, result.netloc])
    except ValueError:
      raise ValueError("Input is not a valid url")
      