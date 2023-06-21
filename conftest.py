import pytest

from myio import HttpCache

ODLS = "https://licenses.opendefinition.org/licenses/groups/{}.json"


def assert_log(caplog, msg: str, lvl: str = ""):
    if lvl:
        assert caplog.records[-1].levelname == lvl
    assert msg in caplog.text


@pytest.fixture
def http_cache(request):
    # request: special object to parametrize fixtures
    http_cache = HttpCache(request.param)
    yield http_cache
    try:  # remove cache before next test
        http_cache.remove()
    except FileNotFoundError:
        # some tests do not create a cache; the safeguard is probably not
        # really required because HttpCache.remove() uses glob, which returns
        # an empty iterator when there are no files.
        pass


@pytest.fixture
def clean_odls_cache():
    # hack to cleanup cache files
    yield
    http_cache = HttpCache(ODLS)
    http_cache.remove()


@pytest.fixture
def pkg_meta():
    return {
        "name": "foobarbaz",
        "title": "Foo Bar Baz",
        "licenses": "CC0-1.0",
        "keywords": ["foo", "bar", "baz"],
    }
