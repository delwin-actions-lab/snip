"""HTTP routes."""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

from snip_api.store import InMemoryStore

app = FastAPI(title="snip")
store = InMemoryStore()


class LinkIn(BaseModel):
    url: HttpUrl


class LinkOut(BaseModel):
    code: str
    url: str
    clicks: int


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/links", status_code=status.HTTP_201_CREATED, response_model=LinkOut)
def create_link(body: LinkIn) -> LinkOut:
    link = store.create(str(body.url))
    return LinkOut(code=link.code, url=link.url, clicks=link.clicks)


@app.get("/links/{code}", response_model=LinkOut)
def link_stats(code: str) -> LinkOut:
    link = store.get(code)
    if link is None:
        raise HTTPException(status_code=404, detail="unknown code")
    return LinkOut(code=link.code, url=link.url, clicks=link.clicks)


@app.get("/{code}")
def follow(code: str) -> RedirectResponse:
    link = store.hit(code)
    if link is None:
        raise HTTPException(status_code=404, detail="unknown code")
    return RedirectResponse(link.url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
