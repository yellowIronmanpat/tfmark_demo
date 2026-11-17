# TFMark audio demo

**[Listen to the demo](https://yellowironmanpat.github.io/tfmark_demo/)** · [维护说明（中文）](docs/MAINTENANCE.md) · [Credits and audio source](ATTRIBUTION.md)

**TFMark: Robust Speech Watermarking via Time–Frequency Embedding**  
Shaoqi Tang, Liping Chen, Kong Aik Lee, and Zhenhua Ling.

This repository hosts the static listening demo accompanying the manuscript. It contains six LibriSpeech test-clean utterances, with matched Original, AudioSeal, TimbreWatermarking, WavMark, and TFMark versions: **6 rows × 5 methods = 30 WAV files**. The first three examples are female speakers and the last three are male speakers.

The repository contains the website and listening samples. Training code, checkpoints, and full experiment results are not included. The examples illustrate audio quality before attacks; they are not a subjective listening study or a robustness evaluation.

## Repository layout

| Path | Contents |
| --- | --- |
| `index.html` | Paper information, abstract, architecture, and audio comparison table |
| `assets/css/style.css` | Desktop and mobile layout |
| `assets/js/player.js` | Exclusive playback, accessible status, and load-error messages |
| `assets/images/architecture.png` | Browser image of the architecture |
| `assets/pdf/architecture.pdf` | Original vector architecture figure |
| `audio/{method}/{sample_id}.wav` | Original WAV files, grouped by method |
| `samples.json` | Sample order, IDs, transcriptions, durations, and audio paths |
| `asset-manifest.json` | SHA-256 checksums for the 30 WAV files and both figures |
| `scripts/validate.py` | File, sample, WAV, checksum, and optional published-site checks |
| `scripts/check-player.cjs` | Playback behavior checks without a browser |
| `.github/workflows/validate.yml` | Checks on commits and after Pages deployments |
| `.nojekyll` | Serve the site as plain static files |

## Preview and validate

From the repository root, with Python 3.9 or newer:

```sh
python3 scripts/validate.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://localhost:8000/>. No package installation or build is needed; `index.html` can also be opened directly. JavaScript enhances playback but is not required to display the table or use the native audio controls.

With Node.js installed, check the playback behavior:

```sh
node scripts/check-player.cjs
```

Check the deployed page and every referenced local asset, including all 30 complete audio files:

```sh
python3 scripts/validate.py --url https://yellowironmanpat.github.io/tfmark_demo/
```

This compares the downloaded bytes with the local checkout. Run it after the Pages deployment for that commit succeeds. It tests HTTP delivery and integrity, not subjective audio quality or browser rendering.

## Sample preparation

| Method | Sampling rate | Message payload | WAV encoding |
| --- | --- | --- | --- |
| Original | 16 kHz | — | 16-bit PCM |
| AudioSeal | 16 kHz | 16 bits | 24-bit PCM |
| TimbreWatermarking | 22.05 kHz | 10 bits | 24-bit PCM |
| WavMark | 16 kHz | 16 bits, plus a fixed synchronization pattern | 24-bit PCM |
| TFMark | 22.05 kHz | 10 bits | 24-bit PCM |

- Full matched utterances were used. No extra attacks, lossy compression, clipping, or independent loudness/peak normalization were applied by this website.
- The 22.05 kHz inputs were resampled from the same 16 kHz original utterances during sample preparation. The website retains each method's supplied sampling rate.
- TFMark samples were exported from the epoch-25 checkpoint with embedding scale `s = 0.1` and the mask disabled.
- These files were re-exported for the listening demonstration; they are not claimed to be the WAV files saved during the original metric evaluation.
- All WAV files are byte-for-byte copies of the supplied demo export. The manifest records their checksums. Internal paths, checkpoint locations, embedded messages, and private export logs are excluded.

## Deployment and updates

GitHub Pages publishes **`main` → `/(root)`** at <https://yellowironmanpat.github.io/tfmark_demo/>. Commits to `main` trigger the existing Pages deployment. The validation workflow checks repository contents and runs a separate online check after a successful Pages build.

Edit `index.html` for paper content, CSS for appearance, and JavaScript for playback. For sample changes, update `samples.json`, the matching HTML rows, and the checksums together. Keep paths relative; the website is hosted under `/tfmark_demo/`.

The paper title, author list, abstract, and vector architecture figure were checked against the manuscript on **2026-11-17**. Update these together when the manuscript changes. Details and troubleshooting are in [the maintenance guide](docs/MAINTENANCE.md).
