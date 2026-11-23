"""Link storage. In-memory for now; Postgres arrives later."""

import secrets
import string
from dataclasses import dataclass

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 7


@dataclass
class Link:
    code: str
    url: str
    clicks: int = 0


class InMemoryStore:
    def __init__(self) -> None:
        self._links: dict[str, Link] = {}

    def create(self, url: str) -> Link:
        while True:
            code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))
            if code not in self._links:
                break
        link = Link(code=code, url=url)
        self._links[code] = link
        return link

    def get(self, code: str) -> Link | None:
        return self._links.get(code)

    def hit(self, code: str) -> Link | None:
        link = self._links.get(code)
        if link is not None:
            link.clicks += 1
        return link
