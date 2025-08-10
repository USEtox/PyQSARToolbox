import pytest
from pyqsartoolbox import QSARToolbox


class _Resp:
    def __init__(self, status_code=200, text="", json_data=None):
        self.status_code = status_code
        self.text = text
        self._json_data = json_data

    def json(self):  # pragma: no cover - trivial
        return self._json_data


@pytest.fixture()
def fake_requests(monkeypatch):
    """Patch requests.get with a dispatcher covering subset of endpoints used in tests."""

    def fake_get(url, *_, **__):
        if url.endswith("/about/toolbox/version"):
            return _Resp(200, text="1.2.3")
        if "/search/cas/" in url:
            parts = url.split("/search/cas/")[-1].split("/")
            cas = int(parts[0])
            ignore = parts[1]
            return _Resp(200, json_data=[{"Cas": cas, "IgnoreStereo": ignore == "true"}])
        return _Resp(404, text="not found")

    import requests  # inline to ensure available
    monkeypatch.setattr(requests, "get", fake_get)
    return requests


def test_initialization_and_version(fake_requests):
    qs = QSARToolbox(port=12345)
    assert qs.toolbox_version() == "1.2.3"
    assert qs.base_url.endswith(":12345/api/v6")


def test_search_cas_string_with_dashes(fake_requests):
    qs = QSARToolbox(port=12345)
    data = qs.search_CAS("123-45-67")
    assert isinstance(data, list) and data
    assert data[0]["Cas"] == 1234567


def test_search_cas_int(fake_requests):
    qs = QSARToolbox(port=12345)
    data = qs.search_CAS(7654321)
    assert data[0]["Cas"] == 7654321
