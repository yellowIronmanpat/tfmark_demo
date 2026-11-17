# Credits and audio source

## Speech data

The examples are drawn from **LibriSpeech test-clean**. LibriSpeech was prepared by Vassil Panayotov with the assistance of Daniel Povey from LibriVox audiobooks. The official [OpenSLR SLR12 page](https://www.openslr.org/12) lists the corpus under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The six utterance IDs and their transcriptions are recorded in [`samples.json`](samples.json). Original speech was preserved. Watermarked versions were generated using the methods below; the TimbreWatermarking and TFMark inputs were resampled to 22.05 kHz. See the [preparation details](README.md#sample-preparation) for the transformations and message lengths. Corpus attribution does not imply endorsement of TFMark by the corpus creators.

## Compared methods

The baseline implementation links match those cited in the manuscript:

- [AudioSeal](https://github.com/facebookresearch/audioseal)
- [TimbreWatermarking](https://github.com/TimbreWatermarking/TimbreWatermarking)
- [WavMark](https://github.com/wavmark/wavmark)

This demo does not redistribute those implementations or their checkpoints. Refer to each upstream repository for its code and model terms.

## Website and paper materials

The presentation structure was inspired by the [DuraMark demo](https://muzw.github.io/duramark_demo/). HTML, CSS, and playback JavaScript were written for TFMark; DuraMark's paper text and audio are not included.

The TFMark abstract and architecture figure accompany the authors' manuscript. The dataset license above applies to the source corpus; it is not a blanket license for every item in this repository. No additional repository-wide software or manuscript license is declared here.
