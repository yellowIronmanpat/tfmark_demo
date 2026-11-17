# TFMark audio demo

**TFMark: Robust Speech Watermarking via Time–Frequency Embedding**

Shaoqi Tang, Liping Chen, Kong Aik Lee, and Zhenhua Ling.

This static page contains six LibriSpeech test-clean utterances, each presented as Original, AudioSeal, TimbreWatermarking, WavMark, and TFMark (30 WAV files). It follows the presentation structure of the [DuraMark demo](https://muzw.github.io/duramark_demo/). The HTML, CSS, and JavaScript were written for TFMark.

## Preview

Open `index.html` in a browser. No build, package installation, or server is required. Alternatively:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Publish on GitHub Pages

Use a public repository named `tfmark_demo` under `yellowIronmanpat`. Place the contents of this directory at the repository root, with `index.html` alongside the CSS, JavaScript, architecture figure, and WAV files.

In **Settings → Pages**, choose **Deploy from a branch**, select **main** and **/(root)**, and save. No custom Actions workflow is needed. `.nojekyll` makes this a plain static site.

The intended URL, once publishing is enabled and the deployment succeeds, is:

`https://yellowironmanpat.github.io/tfmark_demo/`

## Audio provenance

- Original and watermarked WAV files are copied byte-for-byte from the supplied demo archive.
- Full utterances are retained; no extra attacks, lossy compression, clipping, or loudness/peak normalization are applied by this website.
- Original, AudioSeal, and WavMark use 16 kHz; TimbreWatermarking and TFMark use 22.05 kHz.
- AudioSeal and WavMark carry 16-bit messages; TimbreWatermarking and TFMark carry 10-bit messages. WavMark also uses a fixed synchronization pattern.
- TFMark uses the epoch-25 checkpoint with embedding scale 0.1.
- The six examples are an informal listening demonstration, not a listening-study score or a robustness evaluation.
- Public `samples.json` contains the six sample IDs, ordering, transcriptions, and relative audio paths. Machine-specific source paths, checkpoint paths, and internal experiment logs are excluded.

The abstract and author list match the manuscript used to prepare this page on 2026-11-17. The architecture PDF is the same vector figure as in that manuscript; the PNG is used for browser display.

## Updating

Edit `index.html` for paper text and the comparison table, `style.css` for layout, and `player.js` for playback behavior. Keep file paths relative so the page works under a GitHub Pages project URL. When changing samples, update both the HTML table and `samples.json`. Preserve correspondence by sample ID, not filesystem order.

Audio filenames are prefixed with the method name so each public file has a unique name at the repository root.
