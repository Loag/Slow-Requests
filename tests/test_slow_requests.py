import pytest
import warnings
from slow_requests import __version__
from slow_requests.main import SlowRequests


def test_version():
    assert __version__ == '0.1.0'

def test_instantiation_success_with_defaults():
    sl = SlowRequests()
    assert isinstance(sl, SlowRequests) == True
    assert sl.offset == 0.1
    assert sl.per_second == False
    assert sl.current == None


def test_instantiation_success_with_params():
    sl = SlowRequests(offset=3, per_second=True)
    assert isinstance(sl, SlowRequests) == True
    assert sl.offset == 3
    assert sl.per_second == True
    assert sl.current == None

def test_instantiation_fail():
    with pytest.raises(Exception):
        sl = SlowRequests(offset=0.01, per_second=True)
        
def test_instantiation_fast_warning():
    with pytest.warns(UserWarning):
        sl = SlowRequests(offset=101, per_second=True)
        
def test_instantiation_slow_warning():
    with pytest.warns(UserWarning):
        sl = SlowRequests(offset=301, per_second=False)
