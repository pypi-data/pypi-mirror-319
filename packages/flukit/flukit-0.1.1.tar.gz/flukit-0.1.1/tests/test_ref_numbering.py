import pytest
from flukit.align import ref_numbering
import subprocess


def test_identical_sequences():
    """Test numbering when query and reference are identical."""
    query = "MKDC"
    ref = "MKDC"
    expected = ["1", "2", "3", "4"]
    assert ref_numbering(query, ref) == expected


def test_completely_different_sequences():
    """Test numbering with completely different sequences."""
    query = "AAAA"
    ref = "CCCC"
    expected = ["1", "2", "3", "4"]
    assert ref_numbering(query, ref) == expected


def test_single_character():
    """Test numbering with single character sequences."""
    query = "M"
    ref = "M"
    expected = ["1"]
    assert ref_numbering(query, ref) == expected


def test_long_sequences():
    """Test numbering with longer sequences."""
    query = "M" * 20
    ref = "M" * 20
    expected = [str(i) for i in range(1, 21)]
    assert ref_numbering(query, ref) == expected


def test_alternating_gaps():
    """Test with alternating gaps in both sequences."""
    query = "MKC"
    ref = "MK"
    expected = ["1", "2", "-"]
    assert ref_numbering(query, ref) == expected


def test_ref_numbering_basic():
    """Test basic reference numbering functionality."""
    query = "MKCPQSFAAHG"
    ref = "MKDCPTSFAA"
    expected = ["1", "2", "4", "5", "6", "7", "8", "9", "10", "-", "-"]
    assert ref_numbering(query, ref) == expected


def test_gaps_at_sequence_ends():
    """Test gaps at the beginning and end of sequences."""
    query = "MKD"
    ref = "AAMKDAA"
    expected = ["3", "4", "5"]
    assert ref_numbering(query, ref) == expected


def test_large_deletion():
    """Test handling of large deletions in query."""
    query = "MC"
    ref = "MKDCPQSFAAHC"
    expected = ["11", "12"]
    assert ref_numbering(query, ref) == expected


def test_large_insertion():
    """Test handling of large insertions in reference."""
    query = "MKDCPQSFAAHC"
    ref = "MC"
    expected = ["-"] * 10 + ["1", "2"]
    assert ref_numbering(query, ref) == expected
