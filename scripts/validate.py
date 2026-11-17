#!/usr/bin/env python3
"""Validate the static demo with Python's standard library (Python >= 3.9)."""
import argparse
import hashlib
import json
import re
import sys
import time
import wave
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal, ROUND_HALF_UP
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
METHODS = [
    ("original", "Original", 16000, 2),
    ("audioseal", "AudioSeal", 16000, 3),
    ("timbre", "TimbreWatermarking", 22050, 3),
    ("wavmark", "WavMark", 16000, 3),
    ("TFMark", "TFMark", 22050, 3),
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


class DemoHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.refs, self.players, self.transcripts, self.meta = [], [], [], [], []
        self.wav_links, self.current, self.capture, self.buffer = [], None, None, []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for key in ("src", "href"):
            if key in attrs:
                self.refs.append(attrs[key])
        if tag == "audio":
            self.current = {"attrs": attrs, "sources": []}
            self.players.append(self.current)
        if tag == "source" and self.current is not None:
            self.current["sources"].append(attrs)
        if tag == "a" and attrs.get("class") == "audio-file":
            self.wav_links.append(attrs.get("href"))
        if tag == "span" and attrs.get("class") in ("transcript", "sample-meta"):
            self.capture, self.buffer = attrs["class"], []
        if tag == "img":
            require(bool(attrs.get("alt")), "Image is missing alternate text")

    def handle_data(self, data):
        if self.capture:
            self.buffer.append(data)

    def handle_endtag(self, tag):
        if tag == "audio":
            self.current = None
        if tag == "span" and self.capture:
            target = self.transcripts if self.capture == "transcript" else self.meta
            target.append("".join(self.buffer))
            self.capture = None


def local_checks():
    page = (ROOT / "index.html").read_text(encoding="utf-8")
    parsed = DemoHTML()
    parsed.feed(page)
    require(len(parsed.ids) == len(set(parsed.ids)), "Duplicate HTML IDs")
    require("playback-status" in parsed.ids, "Playback status region is missing")
    require((ROOT / ".nojekyll").exists(), ".nojekyll is missing")
    files = {"index.html", "samples.json", "asset-manifest.json"}
    for ref in parsed.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            require(url.scheme in ("https", "mailto"), "Unexpected link scheme: " + ref)
            continue
        if url.path:
            require(not url.path.startswith("/"), "Use project-relative paths: " + ref)
            path = unquote(url.path)
            require((ROOT / path).resolve().is_relative_to(ROOT), "Path escapes repository: " + ref)
            require((ROOT / path).is_file(), "Missing linked file: " + ref)
            files.add(path)
        elif url.fragment:
            require(unquote(url.fragment) in parsed.ids, "Missing anchor: " + ref)

    samples = json.loads((ROOT / "samples.json").read_text(encoding="utf-8"))
    require(len(samples) == 6, "Expected six listening examples")
    require(len(parsed.players) == 30, "Expected thirty audio players")
    require(len(parsed.transcripts) == len(parsed.meta) == 6, "Incomplete table rows")
    require(len({s["sample_id"] for s in samples}) == 6, "Duplicate sample IDs")
    require([s["gender"] for s in samples] == ["F"] * 3 + ["M"] * 3, "Unexpected speaker ordering")
    expected_paths = []
    for row, sample in enumerate(samples):
        require(sample["order"] == row + 1, "Sample order is not sequential")
        require(set(sample["audio"]) == {m[0] for m in METHODS}, "Missing or extra method")
        require(parsed.transcripts[row].upper() == sample["text"].upper(), "Transcript mismatch: " + sample["sample_id"])
        duration = str(Decimal(str(sample["duration_seconds"])).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))
        gender = "Female" if sample["gender"] == "F" else "Male"
        label = f"Sample {row + 1:02d} · {gender} · {duration} s · {sample['sample_id']}"
        require(parsed.meta[row] == label, "Visible sample label mismatch: " + sample["sample_id"])
        for col, (key, name, rate, width) in enumerate(METHODS):
            path = sample["audio"][key]
            expected_paths.append(path)
            player = parsed.players[row * 5 + col]
            attrs = player["attrs"]
            require("controls" in attrs and "autoplay" not in attrs, "Unsafe/missing playback controls")
            require(attrs.get("aria-label") == f"{name}, sample {row + 1}", "Incorrect audio label")
            require(attrs.get("data-method") == name and attrs.get("data-sample") == f"{row + 1:02d}", "Playback label mismatch")
            require(player["sources"] == [{"src": path, "type": "audio/wav"}], "Audio table / JSON mismatch: " + path)
            require(Path(path).stem == sample["sample_id"], "Audio filename / sample ID mismatch")
            with wave.open(str(ROOT / path), "rb") as audio:
                require(audio.getnchannels() == 1, "Expected mono audio: " + path)
                require(audio.getframerate() == rate and audio.getsampwidth() == width, "WAV format mismatch: " + path)
                require(audio.getcomptype() == "NONE", "Expected PCM audio: " + path)
                require(abs(audio.getnframes() / rate - sample["duration_seconds"]) < .001, "Audio duration mismatch: " + path)
                require(len(audio.readframes(audio.getnframes())) == audio.getnframes() * width, "Truncated WAV: " + path)
    require(parsed.wav_links == expected_paths, "Missing or mismatched visible WAV links")
    require({p.relative_to(ROOT).as_posix() for p in ROOT.glob("audio/*/*.wav")} == set(expected_paths), "Missing or orphaned WAV files")
    manifest = json.loads((ROOT / "asset-manifest.json").read_text(encoding="utf-8"))
    expected_assets = set(expected_paths) | {"assets/images/architecture.png", "assets/pdf/architecture.pdf"}
    require(manifest["algorithm"] == "sha256" and set(manifest["files"]) == expected_assets, "Incomplete asset manifest")
    for path, expected_hash in manifest["files"].items():
        require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected_hash, "SHA-256 mismatch: " + path)
    for path in files:
        if Path(path).suffix in (".html", ".json", ".css", ".js"):
            text = (ROOT / path).read_text(encoding="utf-8")
            require(not re.search(r"/(?:Users|home4T_2|root/autodl-tmp)/|file://", text), "Private/local path in public asset: " + path)
    print("PASS: 6 matched rows, 30 complete mono PCM WAVs, transcriptions, durations, labels, links, and 32 asset checksums.")
    return sorted(files)


def online_checks(base_url, paths, wait_seconds=0):
    require(base_url.startswith("https://"), "Online checks require an HTTPS base URL")
    base_url = base_url.rstrip("/") + "/"

    # Pages and this workflow run concurrently. Wait for this commit's homepage
    # before checking all assets; no privileged workflow_run chain is needed.
    if wait_seconds:
        expected_page = hashlib.sha256((ROOT / "index.html").read_bytes()).digest()
        deadline = time.monotonic() + wait_seconds
        while True:
            try:
                req = Request(base_url, headers={"User-Agent": "TFMark-demo-validation", "Cache-Control": "no-cache"})
                with urlopen(req, timeout=15) as response:
                    require(hashlib.sha256(response.read()).digest() == expected_page, "Waiting for the current homepage")
                break
            except Exception:
                if time.monotonic() >= deadline:
                    raise ValueError("Timed out waiting for Pages to publish this checkout")
                print("Waiting for the current Pages deployment...", flush=True)
                time.sleep(5)

    def check(path):
        expected = hashlib.sha256((ROOT / path).read_bytes()).digest()
        url = base_url if path == "index.html" else urljoin(base_url, path)
        for attempt in range(4):
            try:
                req = Request(url, headers={"User-Agent": "TFMark-demo-validation", "Cache-Control": "no-cache"})
                with urlopen(req, timeout=30) as response:
                    require(response.status == 200, "HTTP failure: " + path)
                    require(hashlib.sha256(response.read()).digest() == expected, "Published bytes differ: " + path)
                return path
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(5)

    with ThreadPoolExecutor(max_workers=4) as pool:
        for path in pool.map(check, paths):
            print("HTTP + SHA-256 OK:", path)
    print(f"PASS: {len(paths)} deployed files match this checkout byte-for-byte.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", help="Also compare all page assets with this published site")
    parser.add_argument("--wait", type=int, default=0, help="Seconds to wait for the current homepage before online checks")
    args = parser.parse_args()
    paths = local_checks()
    if args.url:
        online_checks(args.url, paths, args.wait)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, wave.Error) as error:
        print("FAIL:", error, file=sys.stderr)
        sys.exit(1)
