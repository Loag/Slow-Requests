import requests
from urllib.parse import urlparse
import warnings
from time import sleep

class SlowRequests:
  '''
    PARAMS:
    * offset: Float Time to wait in ms between requests
    * per_second: Boolean, if true than offset is the amount of requests to make per second instead of waiting per request.
  '''
  def __init__(self, offset=0.1, per_second=False, headers=None):
    self.__eval_setup(offset, per_second)

    self.headers = headers # the headers to use for each request
    self.offset = offset
    self.per_second = per_second

    self.__requests = [] # the requests

  # get the url currently being executed
  @property
  def current(self):
      print("This is the current request being executed")

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
    * request: can be single request object, a list of request objects, a string path, or a list of string paths..?
  '''
  def add(self, request):

    if isinstance(request, list):
      if all([self.__is_request(req) for req in request]):
        self.__requests.extend(request)

      elif all([self.__is_string(req) for req in request]):
        self.__requests.extend([self.create_request(req) for req in request])
    
    elif self.__is_request(request):
      self.__requests.append(request)

    elif self.__is_string(request):
      self.__requests.append(self.create_request(request))

    else:
      raise TypeError("Requests must be instance of request object or string")

  def __is_request(self, input):
    return isinstance(input, requests)

  def __is_string(self, input):
    return isinstance(input, str)

  def __is_url(self, url):
    try:
      result = urlparse(url)
      return all([result.scheme, result.netloc])
    except ValueError:
      raise ValueError("Input is not a valid url")
      
  '''
    PARAMS:
    * input: valid string url
  '''
  def create_request(self, input):
    if self.__is_string(input):
      if self.__is_url(input):
        return requests(input, headers=self.headers)

    raise TypeError("Input must be a string url")

  def execute(self, input_requests=None):
    if not requests or input_requests:
      raise IndexError("No Requests")
    
    elif input_requests:
      self.add(input_requests)
    
    # execute each request here w/ offset
    if self.per_second:
      return self.__execute_per_second()

  
  # if we are doing a per second run
  def __execute_per_second(self):
    pass

  def __execute_per_request(self):
    for req in requests:
      pass

  '''
    get a specific response for an input? 
  '''
  def response(self, id):
    pass

