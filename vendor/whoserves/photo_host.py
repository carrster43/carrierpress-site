"""Which portraits the feeds may carry. The twin of lib/photo-host.ts.

A portrait ships only when the government that seats the officeholder
publishes it; anything else is dropped and the app draws initials (R6 H9).
test/photo-host.test.ts checks this list and the TypeScript one are the same,
so edit both together.

A party caucus site (misenategop.com, senatedems.com) is NOT the legislature,
even when it hosts the member's official portrait. Never add one.
"""
from urllib.parse import urlparse

SUFFIXES = (".gov", ".mil")

# .us is open to anyone: only the locality tree under a two-letter state code
# is a government's (legislature.state.al.us, ci.durham.nh.us). R7 H10:
# digitalequity.us, an advocacy site, carried an NH representative's portrait.
STATE_CODES = frozenset("al ak az ar ca co ct de dc fl ga hi id il in ia ks ky la me md ma mi mn ms mo mt ne nv nh nj nm ny nc nd oh ok or pa ri sc sd tn tx ut vt va wa wv wi wy as gu mp pr vi".split())


def locality_us(host):
    labels = host.split(".")
    return len(labels) >= 3 and labels[-1] == "us" and labels[-2] in STATE_CODES


OFFICIAL_HOSTS = (
    "senate.mn",
    "usgovcloudapi.net",
    "flgov.com",
    "myfloridalegal.com",
    "myfloridacfo.com",
    "kyagr.com",
    "palegis.us",
    "clackamas.us",
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
    if host.endswith(SUFFIXES) or locality_us(host):
        return url
    if any(host == d or host.endswith("." + d) for d in OFFICIAL_HOSTS):
        return url
    return None
