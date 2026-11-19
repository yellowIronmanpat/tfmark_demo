# TFMark Audio Demo

**[Listen to the demo](https://yellowironmanpat.github.io/tfmark_demo/)**

Audio examples for *TFMark: A Robust Speech Watermarking Method via Time–Frequency Mechanism*.
Six matched utterances compare Original, AudioSeal, TimbreWatermarking, WavMark, and TFMark (30 WAV files). These samples demonstrate audio quality before attacks.

## Files and updates

- `index.html` — page content and audio table.
- `assets/` — styles, playback script, and architecture figures.
- `audio/` — WAV files grouped by method.

Edit these files and push to `main`; GitHub Pages publishes from the repository root. Use relative links. To preview locally, run `python3 -m http.server 8000` and open <http://localhost:8000/>.

## Credits

Speech: [LibriSpeech test-clean](https://www.openslr.org/12), prepared by Vassil Panayotov with Daniel Povey from LibriVox recordings, under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Watermarked versions were generated for this demo; TimbreWatermarking and TFMark inputs were resampled to 22.05 kHz. No attacks or separate loudness normalization were applied.

Baselines: [AudioSeal](https://github.com/facebookresearch/audioseal), [TimbreWatermarking](https://github.com/TimbreWatermarking/TimbreWatermarking), and [WavMark](https://github.com/wavmark/wavmark).
