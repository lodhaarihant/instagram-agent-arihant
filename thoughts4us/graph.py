"""
Tiny Instagram Graph API client, standard library only so it runs in GitHub
Actions without a pip install.

Reads IG_USER_ID and IG_ACCESS_TOKEN from the environment. Never put either
in a file in this repo: they go in GitHub -> Settings -> Secrets.
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = json.load(open(os.path.join(HERE, "config.json")))


class GraphError(Exception):
    pass


class Graph:
    def __init__(self):
        self.user = os.environ.get("IG_USER_ID", "").strip()
        self.token = os.environ.get("IG_ACCESS_TOKEN", "").strip()
        if not self.user or not self.token:
            raise GraphError("IG_USER_ID and IG_ACCESS_TOKEN must be set (GitHub secrets or your shell).")
        host = (os.environ.get("GRAPH_HOST") or CONFIG["graph_host"]).rstrip("/")
        self.base = f"{host}/{os.environ.get('GRAPH_VERSION') or CONFIG['graph_version']}"

    def _call(self, method, path, params=None):
        params = dict(params or {})
        params["access_token"] = self.token
        url = f"{self.base}/{path.lstrip('/')}"
        data = None
        if method == "GET":
            url += "?" + urllib.parse.urlencode(params)
        else:
            data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(url, data=data, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            try:
                msg = json.loads(body).get("error", {}).get("message", body)
            except ValueError:
                msg = body
            raise GraphError(f"{method} {path}: HTTP {e.code}: {msg}") from None

    def get(self, path, **params):
        return self._call("GET", path, params)

    def post(self, path, **params):
        return self._call("POST", path, params)

    # ---------------------------------------------------------------- publishing

    def wait(self, container, timeout=300):
        """Poll a container until Instagram has fetched and processed the media."""
        start = time.time()
        while True:
            st = self.get(container, fields="status_code,status").get("status_code")
            if st in ("FINISHED", "PUBLISHED"):
                return
            if st in ("ERROR", "EXPIRED"):
                info = self.get(container, fields="status")
                raise GraphError(f"container {container} {st}: {info.get('status')}")
            if time.time() - start > timeout:
                raise GraphError(f"container {container} still {st} after {timeout}s")
            time.sleep(5)

    def publish(self, container):
        self.wait(container)
        media = self.post(f"{self.user}/media_publish", creation_id=container)["id"]
        link = self.get(media, fields="permalink").get("permalink", "")
        return media, link

    def image(self, url, caption=None, story=False, carousel_item=False):
        p = {"image_url": url}
        if story:
            p["media_type"] = "STORIES"
        if carousel_item:
            p["is_carousel_item"] = "true"
        if caption:
            p["caption"] = caption
        return self.post(f"{self.user}/media", **p)["id"]

    def story_video(self, url):
        return self.post(f"{self.user}/media", media_type="STORIES", video_url=url)["id"]

    def carousel(self, urls, caption):
        children = [self.image(u, carousel_item=True) for u in urls]
        for c in children:
            self.wait(c)
        return self.post(f"{self.user}/media", media_type="CAROUSEL",
                         children=",".join(children), caption=caption)["id"]

    def reel(self, video_url, caption, cover_url=None):
        p = {"media_type": "REELS", "video_url": video_url, "caption": caption, "share_to_feed": "true"}
        if cover_url:
            p["cover_url"] = cover_url
        return self.post(f"{self.user}/media", **p)["id"]

    def quota(self):
        d = self.get(f"{self.user}/content_publishing_limit", fields="quota_usage,config").get("data", [{}])[0]
        return d.get("quota_usage", 0), d.get("config", {}).get("quota_total")


def load_json(path, default):
    try:
        return json.load(open(path))
    except (OSError, ValueError):
        return default


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    json.dump(data, open(tmp, "w"), indent=1, ensure_ascii=False)
    os.replace(tmp, path)
