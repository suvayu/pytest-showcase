from pathlib import Path
import sys

import pytest
import requests

from myio import copy_files
from myio import dwim_file
from myio import relpaths

ODLS = "https://licenses.opendefinition.org/licenses/groups/{}.json"


@pytest.mark.parametrize("anchored", [True, False])
def test_copy_files(tmp_path, anchored):
    pkgdir = Path("testing/files/mini-ex")
    src = list(pkgdir.rglob("*.csv"))
    if anchored:
        res = copy_files(src, tmp_path, pkgdir)
        assert len(list(tmp_path.rglob("*.csv"))) == len(res) == len(src)
        assert len(list(tmp_path.glob("*.csv"))) == 0  # no CSV in top-level dir
    else:
        res = copy_files(src, tmp_path)  # paths not anchored
        assert len(list(tmp_path.glob("*.csv"))) == len(res) == len(src)
    assert all(map(lambda fp: fp.exists(), res))


def test_relpaths():
    basepath = Path("testing/files/random")
    pattern = "data/*.csv"
    res = relpaths(basepath, pattern)
    assert len(res)
    assert all(map(lambda p: isinstance(p, str), res))
    assert all(map(lambda p: str(basepath) not in p, res))


@pytest.mark.parametrize("ext", [".yaml", ".yml", ".json"])
def test_dwim_file_read(ext):
    fpath = Path(f"testing/files/indices/index{ext}")
    res = dwim_file(fpath)
    assert isinstance(res, list)
    assert len(res) == 3
    assert isinstance(res[0], dict)


@pytest.mark.xfail(reason="typo")
@pytest.mark.parametrize("ext", [".yaml", ".yml", ".json"])
def test_dwim_file_read_extended(ext):
    fpath = Path(f"testing/files/indices/index{ext}")
    res = dwim_file(fpath)
    expected = {"path": "file1", "namee": "dst1", "idxcols": ["cola", "colb"]}
    assert res[0] == expected


@pytest.mark.parametrize("ext", [".yaml", ".yml", ".json"])
def test_dwim_file_write(tmp_path, ext):
    fpath = tmp_path / f"index{ext}"
    data = {"foo": 1, "bar": 2}
    dwim_file(fpath, data)
    assert fpath.exists()


@pytest.mark.example
@pytest.mark.parametrize("http_cache", [ODLS], indirect=["http_cache"])
def test_http_cache_file(http_cache):
    assert http_cache.cachedir.exists()
    assert http_cache.cachefile("foo")[0] == http_cache.cachefile("foo")[0]
    assert http_cache.cachefile("foo")[0] != http_cache.cachefile("bar")[0]


@pytest.mark.example
@pytest.mark.parametrize("http_cache", [ODLS], indirect=["http_cache"])
def test_http_cache_fetch(http_cache):
    grp = "all"
    contents = http_cache.fetch(http_cache.cachefile(grp)[1])
    assert contents
    assert isinstance(contents, bytes)
    assert not http_cache.cachefile(grp)[0].exists()  # cache not created


# incorrect url
@pytest.mark.parametrize("http_cache", [ODLS[:-1]], indirect=["http_cache"])
def test_http_cache_fetch_bad_url(caplog, http_cache):
    grp = "all"
    with pytest.raises(ValueError, match=f"error: {ODLS[:-1]} ".format(grp)):
        http_cache.fetch(http_cache.cachefile(grp)[1])


# non-existent domain / no network
@pytest.mark.parametrize(
    "http_cache", ["https://iamnota.site/{}"], indirect=["http_cache"]
)
def test_http_cache_fetch_no_conn(http_cache):
    grp = "all"
    with pytest.raises(requests.ConnectionError):
        http_cache.fetch(http_cache.cachefile(grp)[1])


@pytest.mark.parametrize("http_cache", [ODLS], indirect=["http_cache"])
def test_http_cache_get(http_cache):
    grp = "all"
    contents = http_cache.get(grp)
    assert contents
    assert isinstance(contents, bytes)
    assert http_cache.cachefile(grp)[0].exists()  # cache created


@pytest.mark.parametrize("http_cache", [ODLS], indirect=["http_cache"])
def test_http_cache_many_gets(http_cache):
    grps = ["all", "osi"]
    contents, caches = [], []
    for grp in grps:
        contents += [http_cache.get(grp)]
        caches += [http_cache.cachefile(grp)[0]]

    assert contents[0] != contents[1]
    assert caches[0] != caches[1]
    assert caches[0].read_bytes() != caches[1].read_bytes()


@pytest.mark.parametrize("http_cache", [ODLS], indirect=["http_cache"])
def test_http_cache_remove(http_cache):
    def _cache_file(count: int):
        caches = tuple(http_cache.cachedir.glob(f"http-{http_cache.url_t_hex}-*"))
        assert len(caches) == count

    n = len(tuple(map(http_cache.get, ["all", "osi", "od"])))
    _cache_file(n)

    http_cache.remove("all")  # remove one
    _cache_file(n - 1)

    http_cache.remove()  # remove the rest
    _cache_file(0)

    with pytest.raises(FileNotFoundError):
        http_cache.remove("not-there")


def test_echo(capsys):
    print("I'm loud")
    print("I'm annoying", file=sys.stderr)
    out, err = capsys.readouterr()
    assert out == "I'm loud\n"
    assert err == "I'm annoying\n"
