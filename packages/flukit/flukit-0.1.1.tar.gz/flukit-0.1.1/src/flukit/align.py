"""Alignment and numbering utilities for influenza sequences."""

import os
import io
import tempfile
import subprocess
from typing import Dict, List, Union
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from .utils import ALLOWED_LETTERS_LITE


import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())


def ref_numbering(query: str, ref: str, probcons_path: str = "probcons") -> List[str]:
    """Generate position numbering for a query sequence based on a reference sequence.

    This function aligns the query amino acid sequence to a reference sequence using probcons
    and generates position numbers for the query sequence based on the alignment. Numbering is
    based on the alignment result. To keep the numbering length consistent with raw query sequence
    length, the gaps in aligned query sequence are skipped, the gaps in aligned reference sequence
    are denoted as '-'.

    Probcons should be installed and accessible from the command line.

    Args:
        query: The query sequence to be numbered.
        ref: The reference sequence to align against.
        probcons_path: Path to the probcons executable. Defaults to "probcons".

    Returns:
        List[str]: A list of position numbers corresponding to each residue in the query sequence.
    """
    if not query or not ref:
        raise ValueError("Query and reference sequences cannot be empty")

    assert set(query).issubset(ALLOWED_LETTERS_LITE), "Not amino acid letter detected"
    assert set(ref).issubset(ALLOWED_LETTERS_LITE), "Not amino acid letter detected"

    # Create temporary fasta file for alignment using Biopython
    with tempfile.NamedTemporaryFile(mode="w", suffix=".fasta", delete=False) as f:
        records = [
            SeqRecord(Seq(query), id="query", description=""),
            SeqRecord(Seq(ref), id="ref", description=""),
        ]
        SeqIO.write(records, f, "fasta")
        temp_path = f.name

    try:
        # Run probcons alignment
        result = subprocess.run(
            [probcons_path, temp_path], capture_output=True, text=True, check=True
        )
        aligned = result.stdout.strip()
        logger.info(result.stderr)
    finally:
        # Clean up temp file
        os.unlink(temp_path)

    # Parse alignment output
    records = SeqIO.parse(io.StringIO(aligned), "fasta")
    aligned_query, aligned_ref = [r.seq for r in records]

    if len(aligned_query) != len(aligned_ref):
        raise ValueError("Alignment lengths do not match")

    # Generate numbering
    ref_pos = 0
    numbering = []

    for q, r in zip(aligned_query, aligned_ref):
        if q == "-":
            ref_pos += 1
            continue  # Skip gaps in query
        if r == "-":
            numbering.append("-")  # Gap in reference
        else:
            ref_pos += 1
            numbering.append(str(ref_pos))

    # duplication not allow except for '-'
    numbering_check = [n for n in numbering if n != "-"]
    if len(numbering_check) != len(set(numbering_check)):
        raise ValueError("Duplicate numbering detected")

    return numbering
