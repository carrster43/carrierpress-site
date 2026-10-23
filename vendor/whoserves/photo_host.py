"""Which portraits the feeds may carry. The twin of lib/photo-host.ts.

A portrait ships only when the government that seats the officeholder
publishes it; anything else is dropped and the app draws initials (R6 H9).
test/photo-host.test.ts checks this list and the TypeScript one are the same,
so edit both together.

A party caucus site (misenategop.com, senatedems.com) is NOT the legislature,
even when it hosts the member's official portrait. Never add one.
"""
from urllib.parse import urlparse

SUFFIXES = (".gov", ".us", ".mil")

OFFICIAL_HOSTS = (
    "senate.mn",
    "usgovcloudapi.net",
    "flgov.com",
    "myfloridalegal.com",
    "myfloridacfo.com",
    "kyagr.com",
)


def official_photo(url):
    """The url if its host is a government's own, else None."""
    if not url:
        return None
    try:
        parsed = urlparse(url)
    except ValueError:
        return None
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not host:
        return None
    if host.endswith(SUFFIXES):
        return url
    if any(host == d or host.endswith("." + d) for d in OFFICIAL_HOSTS):
        return url
    return None
