import tempfile
from pathlib import Path

import numpy as np
import pytest

from soundpython import Audio, AudioMetadata

# Test constants
MONO_SAMPLE_RATE = 44100
STEREO_SAMPLE_RATE = 44100

TEST_ROOT_DIR: Path = Path(__file__).parent
TEST_DATA_DIR: Path = TEST_ROOT_DIR / "test_data"


def test_mono_mp3_metadata():
    """Test loading a mono MP3 file and verify its metadata"""
    # Load the test file
    audio = Audio.from_file(TEST_DATA_DIR / "test_mono.mp3")

    # Check metadata values
    assert audio.metadata.sample_rate == MONO_SAMPLE_RATE, "Sample rate should be 22.05kHz"
    assert audio.metadata.channels == 1, "Audio should be mono"
    assert audio.metadata.bits_per_sample == 16, "Bit depth should be 16 bits"

    # Verify data array properties
    assert isinstance(audio.data, np.ndarray), "Data should be a numpy array"
    assert audio.data.dtype == np.float32, "Data should be float32"
    assert audio.data.ndim == 1, "Mono audio should be 1-dimensional"

    # Check data normalization
    assert np.all(audio.data >= -1.0), "Data should be normalized >= -1.0"
    assert np.all(audio.data <= 1.0), "Data should be normalized <= 1.0"

    # Verify frame count matches data length
    assert len(audio.data) == audio.metadata.frame_count, "Frame count should match data length"


def test_file_not_found():
    """Test that appropriate error is raised for missing files"""
    with pytest.raises(FileNotFoundError):
        Audio.from_file("nonexistent.mp3")


def test_get_channel_mono():
    """Test that get_channel on mono audio returns the same audio"""
    audio = Audio.from_file(TEST_DATA_DIR / "test_mono.mp3")
    channel = audio.get_channel(0)

    # Should be the same data
    np.testing.assert_array_equal(audio.data, channel.data)
    assert audio.metadata.channels == channel.metadata.channels


def test_to_mono_on_mono():
    """Test that to_mono on mono audio returns the same audio"""
    audio = Audio.from_file(TEST_DATA_DIR / "test_mono.mp3")
    mono = audio.to_mono()

    # Should be the same data
    np.testing.assert_array_equal(audio.data, mono.data)
    assert audio.metadata.channels == mono.metadata.channels


def test_audio_representation():
    """Test the string representation of the Audio object"""
    audio = Audio.from_file(TEST_DATA_DIR / "test_mono.mp3")
    repr_str = repr(audio)

    assert "44100Hz" in repr_str, "Sample rate should be in string representation"
    assert "channels=1" in repr_str, "Channel count should be in string representation"
    assert isinstance(repr_str, str), "Representation should be a string"


def test_length():
    """Test the __len__ method returns correct frame count"""
    audio = Audio.from_file(TEST_DATA_DIR / "test_mono.mp3")
    assert len(audio) == audio.metadata.frame_count


def test_stereo_mp3_metadata():
    """Test loading a stereo MP3 file and verify its metadata"""
    # Load the test file
    audio = Audio.from_file(TEST_DATA_DIR / "test_stereo.mp3")

    # Check metadata values
    assert audio.metadata.sample_rate == STEREO_SAMPLE_RATE, "Sample rate should be 44.1kHz"
    assert audio.metadata.channels == 2, "Audio should be stereo"
    assert audio.metadata.bits_per_sample == 16, "Bit depth should be 16 bits"

    # Verify data array properties
    assert isinstance(audio.data, np.ndarray), "Data should be a numpy array"
    assert audio.data.dtype == np.float32, "Data should be float32"
    assert audio.data.ndim == 2, "Stereo audio should be 2-dimensional"
    assert audio.data.shape[1] == 2, "Stereo audio should have 2 channels"

    # Check data normalization
    assert np.all(audio.data >= -1.0), "Data should be normalized >= -1.0"
    assert np.all(audio.data <= 1.0), "Data should be normalized <= 1.0"

    # Verify frame count matches data length
    assert len(audio.data) == audio.metadata.frame_count, "Frame count should match data length"


def test_stereo_channel_separation():
    """Test that stereo channels can be correctly separated"""
    audio = Audio.from_file(TEST_DATA_DIR / "test_stereo.mp3")

    # Get individual channels
    left = audio.get_channel(0)
    right = audio.get_channel(1)

    # Check that channels are mono
    assert left.metadata.channels == 1
    assert right.metadata.channels == 1

    # Check that the data matches the original
    np.testing.assert_array_equal(audio.data[:, 0], left.data)
    np.testing.assert_array_equal(audio.data[:, 1], right.data)

    # Check sample rates are preserved
    assert left.metadata.sample_rate == STEREO_SAMPLE_RATE
    assert right.metadata.sample_rate == STEREO_SAMPLE_RATE


def test_stereo_to_mono_conversion():
    """Test converting stereo to mono"""
    audio = Audio.from_file(TEST_DATA_DIR / "test_stereo.mp3")
    mono = audio.to_mono()

    # Check that output is mono
    assert mono.metadata.channels == 1
    assert mono.data.ndim == 1

    # Check that mono data is average of stereo channels
    expected_mono = audio.data.mean(axis=1)
    np.testing.assert_array_equal(mono.data, expected_mono)

    # Check metadata is preserved
    assert mono.metadata.sample_rate == STEREO_SAMPLE_RATE
    assert mono.metadata.sample_width == audio.metadata.sample_width

    # Check normalization is preserved
    assert np.all(mono.data >= -1.0)
    assert np.all(mono.data <= 1.0)


def assert_audios_equal(audio1, audio2, check_data=True, is_lossy=False):
    """Helper function to compare two Audio objects

    Args:
        audio1: First audio object
        audio2: Second audio object
        check_data: If True, compare audio data
        is_lossy: If True, use more lenient tolerances for lossy formats
    """
    # Compare metadata
    assert audio1.metadata.sample_rate == audio2.metadata.sample_rate, "Sample rates should match"
    assert audio1.metadata.channels == audio2.metadata.channels, "Channel counts should match"
    assert audio1.metadata.sample_width == audio2.metadata.sample_width, "Sample widths should match"
    assert (
        abs(audio1.metadata.duration_seconds - audio2.metadata.duration_seconds) < 0.1
    ), "Durations should match within 0.1s"

    # For lossy formats, frame count might differ slightly
    if not is_lossy:
        assert audio1.metadata.frame_count == audio2.metadata.frame_count, "Frame counts should match"

    # Compare actual audio data if requested
    if check_data:
        if is_lossy:
            # Very lenient comparison for MP3
            # We're mainly checking that the overall structure is preserved
            assert audio1.data.shape == audio2.data.shape, "Audio shapes should match"

            # Check that RMS difference is not too large
            rms_diff = np.sqrt(np.mean((audio1.data - audio2.data) ** 2))
            assert rms_diff < 0.1, f"RMS difference too large: {rms_diff}"

            # Check correlation to ensure signal structure is preserved
            correlation = np.corrcoef(audio1.data.ravel(), audio2.data.ravel())[0, 1]
            assert correlation > 0.9, f"Correlation too low: {correlation}"
        else:
            # Strict comparison for lossless formats
            np.testing.assert_allclose(audio1.data, audio2.data, rtol=1e-4, atol=1e-4)


# Fix 1: Update test_save_and_load_mono
def test_save_and_load_mono():
    """Test saving and loading mono audio preserves the data"""
    original = Audio.from_file(TEST_DATA_DIR / "test_mono.mp3")

    with (
        tempfile.NamedTemporaryFile(suffix=".wav") as temp_wav,
        tempfile.NamedTemporaryFile(suffix=".mp3") as temp_mp3,
    ):
        # Test WAV format
        original.save(temp_wav.name)
        loaded_wav = Audio.from_file(temp_wav.name)
        assert_audios_equal(original, loaded_wav)

        # Test MP3 format - note is_lossy=True here
        original.save(temp_mp3.name)
        loaded_mp3 = Audio.from_file(temp_mp3.name)
        assert_audios_equal(original, loaded_mp3, is_lossy=True)


def test_save_and_load_stereo():
    """Test saving and loading stereo audio preserves the data"""
    original = Audio.from_file(TEST_DATA_DIR / "test_stereo.mp3")

    with (
        tempfile.NamedTemporaryFile(suffix=".wav") as temp_wav,
        tempfile.NamedTemporaryFile(suffix=".mp3") as temp_mp3,
    ):
        # Test WAV format (lossless)
        original.save(temp_wav.name)
        loaded_wav = Audio.from_file(temp_wav.name)
        assert_audios_equal(original, loaded_wav, is_lossy=False)

        # Test MP3 format (lossy)
        original.save(temp_mp3.name)
        loaded_mp3 = Audio.from_file(temp_mp3.name)
        assert_audios_equal(original, loaded_mp3, is_lossy=True)


def test_save_invalid_format():
    """Test that saving with invalid format raises error"""
    audio = Audio.from_file(TEST_DATA_DIR / "test_mono.mp3")

    with tempfile.NamedTemporaryFile(suffix=".xyz") as temp_file:
        with pytest.raises(ValueError):
            audio.save(temp_file.name)


def test_concat_mono():
    """Test concatenating two mono audio files"""
    # Load same file twice for testing
    audio1 = Audio.from_file(TEST_DATA_DIR / "test_mono.mp3")
    audio2 = Audio.from_file(TEST_DATA_DIR / "test_mono.mp3")

    # Concatenate
    result = audio1.concat(audio2)

    # Check metadata
    assert result.metadata.sample_rate == audio1.metadata.sample_rate
    assert result.metadata.channels == 1
    assert result.metadata.sample_width == audio1.metadata.sample_width
    assert (
        abs(result.metadata.duration_seconds - (audio1.metadata.duration_seconds + audio2.metadata.duration_seconds))
        < 0.1
    )

    # Check data
    assert len(result.data) == len(audio1.data) + len(audio2.data)
    np.testing.assert_array_equal(result.data[: len(audio1.data)], audio1.data)
    np.testing.assert_array_equal(result.data[len(audio1.data) :], audio2.data)


def test_concat_stereo():
    """Test concatenating two stereo audio files"""
    # Load same file twice for testing
    audio1 = Audio.from_file(TEST_DATA_DIR / "test_stereo.mp3")
    audio2 = Audio.from_file(TEST_DATA_DIR / "test_stereo.mp3")

    # Concatenate
    result = audio1.concat(audio2)

    # Check metadata
    assert result.metadata.sample_rate == audio1.metadata.sample_rate
    assert result.metadata.channels == 2
    assert result.metadata.sample_width == audio1.metadata.sample_width
    assert (
        abs(result.metadata.duration_seconds - (audio1.metadata.duration_seconds + audio2.metadata.duration_seconds))
        < 0.1
    )

    # Check data shape and content
    assert result.data.shape == (audio1.data.shape[0] + audio2.data.shape[0], 2)
    np.testing.assert_array_equal(result.data[: audio1.data.shape[0]], audio1.data)
    np.testing.assert_array_equal(result.data[audio1.data.shape[0] :], audio2.data)


def test_concat_invalid():
    """Test concatenating incompatible audio files"""
    mono = Audio.from_file(TEST_DATA_DIR / "test_mono.mp3")
    stereo = Audio.from_file(TEST_DATA_DIR / "test_stereo.mp3")

    # Test mismatched channels
    with pytest.raises(ValueError, match="Channel counts must match"):
        mono.concat(stereo)

    with pytest.raises(ValueError, match="Channel counts must match"):
        stereo.concat(mono)

    # Create audio with different sample rate for testing
    different_rate = Audio(
        mono.data,
        AudioMetadata(
            sample_rate=22050,  # Different from mono file
            channels=mono.metadata.channels,
            sample_width=mono.metadata.sample_width,
            duration_seconds=mono.metadata.duration_seconds,
            frame_count=len(mono.data),
        ),
    )

    # Test mismatched sample rates
    with pytest.raises(ValueError, match="Sample rates must match"):
        mono.concat(different_rate)


def test_slice():
    """Test slicing audio by time"""
    # Load test file
    audio = Audio.from_file(TEST_DATA_DIR / "test_mono.mp3")

    # Test slicing the middle portion
    start_time = 0.5
    end_time = 1.0
    sliced = audio.slice(start_time, end_time)

    # Check metadata
    assert sliced.metadata.sample_rate == audio.metadata.sample_rate
    assert sliced.metadata.channels == audio.metadata.channels
    assert sliced.metadata.sample_width == audio.metadata.sample_width
    assert abs(sliced.metadata.duration_seconds - (end_time - start_time)) < 0.1

    # Check expected length in samples
    expected_samples = int((end_time - start_time) * audio.metadata.sample_rate)
    assert abs(len(sliced) - expected_samples) <= 1  # Allow for rounding

    # Test slicing from start
    start_slice = audio.slice(end_seconds=1.0)
    assert abs(start_slice.metadata.duration_seconds - 1.0) < 0.1

    # Test slicing to end
    end_slice = audio.slice(start_seconds=1.0)
    assert abs(end_slice.metadata.duration_seconds - (audio.metadata.duration_seconds - 1.0)) < 0.1

    # Test invalid inputs
    with pytest.raises(ValueError):
        audio.slice(-1.0)  # Negative start time

    with pytest.raises(ValueError):
        audio.slice(2.0, 1.0)  # End before start

    with pytest.raises(ValueError):
        audio.slice(0.0, audio.metadata.duration_seconds + 1)  # End after audio duration


def test_slice_stereo():
    """Test slicing stereo audio"""
    audio = Audio.from_file(TEST_DATA_DIR / "test_stereo.mp3")

    # Slice a portion
    sliced = audio.slice(0.5, 1.5)

    # Check that stereo structure is preserved
    assert sliced.metadata.channels == 2
    assert sliced.data.ndim == 2
    assert sliced.data.shape[1] == 2

    # Check duration
    assert abs(sliced.metadata.duration_seconds - 1.0) < 0.1

    # Check that the data is a proper subset
    start_idx = int(0.5 * audio.metadata.sample_rate)
    end_idx = int(1.5 * audio.metadata.sample_rate)
    np.testing.assert_array_equal(sliced.data, audio.data[start_idx:end_idx])


def test_overlay_mono():
    """Test overlaying two mono audio files with crossfade"""
    # Load same file twice for testing
    audio1 = Audio.from_file(TEST_DATA_DIR / "test_mono.mp3")
    audio2 = Audio.from_file(TEST_DATA_DIR / "test_mono.mp3")

    # Test with 0.5 second fade
    fade_duration = 0.5
    result = audio1.overlay(audio2, fade_duration)

    # Check metadata
    assert result.metadata.sample_rate == audio1.metadata.sample_rate
    assert result.metadata.channels == 1
    assert result.metadata.sample_width == audio1.metadata.sample_width

    # Check data shape
    fade_samples = int(fade_duration * audio1.metadata.sample_rate)
    expected_length = len(audio1.data) + len(audio2.data) - fade_samples
    assert len(result.data) == expected_length

    # Check normalization
    assert np.all(result.data >= -1.0)
    assert np.all(result.data <= 1.0)

    # Test fade region
    fade_start_idx = len(audio1.data) - fade_samples
    fade_region = result.data[fade_start_idx : fade_start_idx + fade_samples]

    # Verify fade is actually happening
    assert np.all(np.diff(fade_region) != 0), "Fade region should not be constant"


def test_overlay_stereo():
    """Test overlaying two stereo audio files with crossfade"""
    # Load same file twice for testing
    audio1 = Audio.from_file(TEST_DATA_DIR / "test_stereo.mp3")
    audio2 = Audio.from_file(TEST_DATA_DIR / "test_stereo.mp3")

    # Test with 0.5 second fade
    fade_duration = 0.5
    result = audio1.overlay(audio2, fade_duration)

    # Check metadata
    assert result.metadata.sample_rate == audio1.metadata.sample_rate
    assert result.metadata.channels == 2
    assert result.metadata.sample_width == audio1.metadata.sample_width

    # Check data shape
    fade_samples = int(fade_duration * audio1.metadata.sample_rate)
    expected_length = len(audio1.data) + len(audio2.data) - fade_samples
    assert len(result.data) == expected_length
    assert result.data.shape[1] == 2

    # Check normalization
    assert np.all(result.data >= -1.0)
    assert np.all(result.data <= 1.0)

    # Test fade region
    fade_start_idx = len(audio1.data) - fade_samples
    fade_region = result.data[fade_start_idx : fade_start_idx + fade_samples]

    # Verify fade is happening in both channels
    assert np.all(np.diff(fade_region[:, 0]) != 0), "Left channel fade should not be constant"
    assert np.all(np.diff(fade_region[:, 1]) != 0), "Right channel fade should not be constant"


def test_overlay_invalid():
    """Test overlaying incompatible audio files"""
    mono = Audio.from_file(TEST_DATA_DIR / "test_mono.mp3")
    stereo = Audio.from_file(TEST_DATA_DIR / "test_stereo.mp3")

    # Test mismatched channels
    with pytest.raises(ValueError, match="Channel counts must match"):
        mono.overlay(stereo, 0.5)

    # Test invalid fade duration
    with pytest.raises(ValueError, match="Fade duration must be positive"):
        mono.overlay(mono, 0)

    with pytest.raises(ValueError, match="Fade duration cannot exceed"):
        mono.overlay(mono, 500.0)  # Longer than audio duration

    # Create audio with different sample rate
    different_rate = Audio(
        mono.data,
        AudioMetadata(
            sample_rate=22050,
            channels=mono.metadata.channels,
            sample_width=mono.metadata.sample_width,
            duration_seconds=mono.metadata.duration_seconds,
            frame_count=len(mono.data),
        ),
    )

    # Test mismatched sample rates
    with pytest.raises(ValueError, match="Sample rates must match"):
        mono.overlay(different_rate, 0.5)


def test_create_silent_stereo():
    """Test creating a stereo silent track"""
    duration = 2.0
    audio = Audio.create_silent(duration)

    # Check metadata
    assert audio.metadata.channels == 2
    assert audio.metadata.sample_rate == 44100
    assert audio.metadata.sample_width == 2
    assert abs(audio.metadata.duration_seconds - duration) < 0.0001
    assert audio.metadata.frame_count == int(duration * 44100)

    # Check data shape and content
    assert audio.data.shape == (int(duration * 44100), 2)
    assert np.all(audio.data == 0)
    assert audio.data.dtype == np.float32


def test_create_silent_mono():
    """Test creating a mono silent track"""
    duration = 1.5
    audio = Audio.create_silent(duration, stereo=False)

    # Check metadata
    assert audio.metadata.channels == 1
    assert audio.metadata.sample_rate == 44100
    assert audio.metadata.sample_width == 2
    assert abs(audio.metadata.duration_seconds - duration) < 0.0001
    assert audio.metadata.frame_count == int(duration * 44100)

    # Check data shape and content
    assert audio.data.shape == (int(duration * 44100),)
    assert np.all(audio.data == 0)
    assert audio.data.dtype == np.float32


def test_create_silent_custom_params():
    """Test creating silent track with custom parameters"""
    duration = 1.0
    sample_rate = 22050
    sample_width = 4

    audio = Audio.create_silent(duration, stereo=True, sample_rate=sample_rate, sample_width=sample_width)

    # Check metadata
    assert audio.metadata.channels == 2
    assert audio.metadata.sample_rate == sample_rate
    assert audio.metadata.sample_width == sample_width
    assert abs(audio.metadata.duration_seconds - duration) < 0.0001
    assert audio.metadata.frame_count == int(duration * sample_rate)


def test_create_silent_invalid_params():
    """Test error handling for invalid parameters"""
    # Test negative duration
    with pytest.raises(ValueError, match="Duration must be positive"):
        Audio.create_silent(-1.0)

    # Test zero duration
    with pytest.raises(ValueError, match="Duration must be positive"):
        Audio.create_silent(0.0)

    # Test invalid sample rate
    with pytest.raises(ValueError, match="Sample rate must be positive"):
        Audio.create_silent(1.0, sample_rate=0)

    # Test invalid sample width
    with pytest.raises(ValueError, match="Sample width must be 1, 2, or 4 bytes"):
        Audio.create_silent(1.0, sample_width=3)
