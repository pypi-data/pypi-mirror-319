from pathlib import Path

import audiometer


def test_measure_loudness(audio_path: Path):
    expected = dict(
        integrated=-23.5,
        momentary=[
            -120.7,
            -120.7,
            -120.7,
            -44.6,
            -40.1,
            -36.2,
            -33.4,
            -31.1,
            -28.9,
            -26.6,
            -24.2,
            -21.4,
            -18.1,
        ],
    )

    assert audiometer.measure_loudness(audio_path) == expected
