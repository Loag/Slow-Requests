import pytest
from slow_requests.slow_requests import InputReq, SlowRequests

def test_InputReq_instantiation_success():
    inp_req = InputReq("https://google.com")
    assert isinstance(inp_req, InputReq) == True


def test_instantiation_success_with_defaults():
    sl = SlowRequests()
    assert isinstance(sl, SlowRequests) == True
    assert sl.offset == 0.1
    assert sl.per_second == False


def test_instantiation_success_with_params():
    sl = SlowRequests(offset=3, per_second=True)
    assert isinstance(sl, SlowRequests) == True
    assert sl.offset == 3
    assert sl.per_second == True

def test_instantiation_fail():
    with pytest.raises(Exception):
        sl = SlowRequests(offset=0.01, per_second=True)
        
def test_instantiation_fast_warning():
    with pytest.warns(UserWarning):
        sl = SlowRequests(offset=101, per_second=True)
        
def test_instantiation_slow_warning():
    with pytest.warns(UserWarning):
        sl = SlowRequests(offset=301, per_second=False)

# not ideal
def test_get_with_add():
    sl = SlowRequests()
    sl.add("https://jsonplaceholder.typicode.com/todos/1")

    for res in sl.execute():
        assert res.status_code == 200

# # not ideal
# def test_get_with_execute():
#     sl = SlowRequests()
#     for res in sl.execute(requests=["https://jsonplaceholder.typicode.com/todos/1", "https://jsonplaceholder.typicode.com/todos/1", "https://jsonplaceholder.typicode.com/todos/1"]):
#         assert res.status_code == 200

# def test_concurrent_get_with_execute():
#     sl = SlowRequests(offset=5, per_second=True)
#     for res in sl.execute(requests=["https://jsonplaceholder.typicode.com/todos/1", "https://jsonplaceholder.typicode.com/todos/1", "https://jsonplaceholder.typicode.com/todos/1"]):
#         assert res.status_code == 200