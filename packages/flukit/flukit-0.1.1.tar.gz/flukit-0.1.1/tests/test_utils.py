import pytest

from flukit.utils import NumberedResidue, NumberedProtein, ALLOWED_LETTERS


def test_numbered_residue_init():
    # Test default initialization
    nr = NumberedResidue()
    assert nr.residue == "-"
    assert nr.number_dict == {}

    # Test with custom values
    nr = NumberedResidue("A", {"H3": "98"})
    assert nr.residue == "A"
    assert nr.number_dict == {"H3": "98"}


def test_residue_validation():
    # Test valid residues
    for letter in ALLOWED_LETTERS:
        nr = NumberedResidue(letter)
        assert nr.residue == letter

    # Test invalid residue length
    with pytest.raises(ValueError, match="Only one letter accepted"):
        NumberedResidue("AA")

    # Test invalid residue character
    with pytest.raises(ValueError, match="Not an amino acid letter"):
        NumberedResidue("B")  # B is not in ALLOWED_LETTERS


def test_number_dict_conversion():
    # Test with mixed types
    nr = NumberedResidue("A", {1: 2, "H3": 98})
    assert nr.number_dict == {"1": "2", "H3": "98"}

    # Test with empty dict
    nr = NumberedResidue("A")
    assert nr.number_dict == {}


def test_repr_formatting():
    # Test simple case with no numbering
    nr = NumberedResidue("A")
    assert repr(nr) == "|A|"

    # Test with single numbering
    nr = NumberedResidue("Y", {"H3": "98"})
    assert repr(nr) == "  |Y |\nH3|98|"

    # Test with multiple numbering systems
    nr = NumberedResidue("Y", {"H3": "98", "H1": "102"})
    result = repr(nr)
    assert "  | Y |" in result
    assert "H3| 98|" in result
    assert "H1|102|" in result


def test_align_repr():
    # Test alignment with different length inputs
    contents = ["H3|98|", "H1|102|", "|Y|"]
    result = NumberedResidue._align_repr(contents)
    lines = result.split("\n")

    # Check that all lines have the same length
    assert len(set(len(line) for line in lines)) == 1

    # Check that pipes are aligned
    first_pipes = [line.index("|") for line in lines]
    assert len(set(first_pipes)) == 1

    second_pipes = [line.rindex("|") for line in lines]
    assert len(set(second_pipes)) == 1


class TestNumberedProtein:
    """Test suite for NumberedProtein class."""

    @pytest.fixture
    def alt_schema_protein(self):
        """Protein with alternating schema positions."""
        return NumberedProtein(
            "MTKPC",
            {"H3": ["1", "3", "5", "7", "9"], "H5": ["2", "4", "6", "8", "10"]},
            default_schema="H3",
        )

    @pytest.fixture
    def nonseq_schema_protein(self):
        """Protein with non-sequential numbering schemas."""
        return NumberedProtein(
            "MXC-Y*DPS*",
            {
                "H3": ["31", "32", "33", "-", "34", "35", "36", "37", "38", "39"],
                "H5": ["11", "12", "13", "14", "15", "16", "17", "18", "19", "20"],
            },
            default_schema="H5",
        )

    def test_initialization(self, alt_schema_protein, nonseq_schema_protein):
        """Test protein initialization with different schemas."""
        # Test alternating schema protein
        assert str(alt_schema_protein) == "MTKPC"
        assert alt_schema_protein.raw_seq == "MTKPC"
        assert alt_schema_protein.seq == "MTKPC"
        assert len(alt_schema_protein) == 5

        # Test non-sequential schema protein
        assert str(nonseq_schema_protein) == "MXC-Y*DPS*"
        assert nonseq_schema_protein.raw_seq == "MXC-Y*DPS*"
        assert nonseq_schema_protein.seq == "MXC-Y*DPS*"
        assert len(nonseq_schema_protein) == 10

        # Test invalid schema length
        with pytest.raises(
            ValueError, match="Schema H3 length doesn't match sequence length"
        ):
            NumberedProtein("MTKPC", {"H3": ["1", "2", "3"]})

    def test_get_residue_alt_schema(self, alt_schema_protein):
        """Test residue retrieval with alternating schema positions."""
        # Test H3 schema positions
        residue = alt_schema_protein.get_residue("H3", "1")
        assert residue.residue == "M"
        assert residue.number_dict == {"orig": "1", "H3": "1", "H5": "2"}

        residue = alt_schema_protein.get_residue("H3", "3")
        assert residue.residue == "T"
        assert residue.number_dict == {"orig": "2", "H3": "3", "H5": "4"}

        # Test H5 schema positions
        residue = alt_schema_protein.get_residue("H5", "4")
        assert residue.residue == "T"
        assert residue.number_dict == {"orig": "2", "H3": "3", "H5": "4"}

        residue = alt_schema_protein.get_residue("H5", "8")
        assert residue.residue == "P"
        assert residue.number_dict == {"orig": "4", "H3": "7", "H5": "8"}

    def test_get_residue_nonseq_schema(self, nonseq_schema_protein):
        """Test residue retrieval with non-sequential numbering schemas."""
        # Test H3 schema positions
        residue = nonseq_schema_protein.get_residue("H3", "31")
        assert residue.residue == "M"
        assert residue.number_dict == {"orig": "1", "H3": "31", "H5": "11"}

        # Test special characters
        residue = nonseq_schema_protein.get_residue("H3", "-")
        assert residue.residue == "-"
        assert residue.number_dict == {"orig": "4", "H3": "-", "H5": "14"}

        # Test H5 schema positions
        residue = nonseq_schema_protein.get_residue("H5", "15")
        assert residue.residue == "Y"
        assert residue.number_dict == {"orig": "5", "H3": "34", "H5": "15"}

    def test_replace_residue_alt_schema(self, alt_schema_protein):
        """Test residue replacement with alternating schema positions."""
        # Test mutations using H3 schema
        alt_schema_protein.replace_residue("H3", "7", "A")  # P→A
        assert str(alt_schema_protein) == "MTKAC"
        assert alt_schema_protein.mutations == ["P7A"]

        # Test mutations using H5 schema
        alt_schema_protein.replace_residue("H5", "6", "R")  # K→R
        assert str(alt_schema_protein) == "MTRAC"
        assert alt_schema_protein.mutations == ["K5R", "P7A"]  # Ordered by position

        # Test reversion
        alt_schema_protein.replace_residue("H3", "7", "P")  # A→P
        assert str(alt_schema_protein) == "MTRPC"
        assert alt_schema_protein.mutations == ["K5R"]

    def test_replace_residue_nonseq_schema(self, nonseq_schema_protein):
        """Test residue replacement with non-sequential numbering schemas."""
        # Test mutations using H3 schema
        nonseq_schema_protein.replace_residue("H3", "32", "A")  # X→A
        assert str(nonseq_schema_protein) == "MAC-Y*DPS*"
        assert nonseq_schema_protein.mutations == ["X12A"]

        # Test mutations using H5 schema
        nonseq_schema_protein.replace_residue("H5", "17", "Q")  # D→Q
        assert str(nonseq_schema_protein) == "MAC-Y*QPS*"
        assert nonseq_schema_protein.mutations == ["X12A", "D17Q"]

        # Test special character mutations
        nonseq_schema_protein.replace_residue("H5", "14", "X")  # -→X
        assert str(nonseq_schema_protein) == "MACXY*QPS*"
        assert nonseq_schema_protein.mutations == ["X12A", "-14X", "D17Q"]

    def test_invalid_positions(self, alt_schema_protein, nonseq_schema_protein):
        """Test error handling for invalid positions."""
        # Test alternating schema protein
        with pytest.raises(ValueError, match="Position 2 not found in schema H3"):
            alt_schema_protein.get_residue("H3", "2")
        with pytest.raises(ValueError, match="Position 3 not found in schema H5"):
            alt_schema_protein.get_residue("H5", "3")

        # Test non-sequential schema protein
        with pytest.raises(ValueError, match="Position 1 not found in schema H3"):
            nonseq_schema_protein.get_residue("H3", "1")
        with pytest.raises(ValueError, match="Position 10 not found in schema H5"):
            nonseq_schema_protein.get_residue("H5", "10")

    def test_mutation_ordering(self, alt_schema_protein, nonseq_schema_protein):
        """Test mutation ordering by position."""
        # Test alternating schema protein
        alt_schema_protein.replace_residue("H3", "9", "S")  # C→S
        alt_schema_protein.replace_residue("H3", "1", "V")  # M→V
        alt_schema_protein.replace_residue("H5", "4", "R")  # T→R
        assert alt_schema_protein.mutations == ["M1V", "T3R", "C9S"]

        # Test non-sequential schema protein
        nonseq_schema_protein.replace_residue("H3", "39", "A")  # *→A
        nonseq_schema_protein.replace_residue("H5", "11", "V")  # M→V
        nonseq_schema_protein.replace_residue("H3", "33", "D")  # C→D
        assert nonseq_schema_protein.mutations == ["M11V", "C13D", "*20A"]

    def test_slice_basic(self, alt_schema_protein):
        """Test basic slicing functionality with different schemas."""
        # Test slicing with H3 schema
        sliced = alt_schema_protein.slice("1", "5", schema="H3")
        assert str(sliced) == "MTK"
        assert sliced._numbering_schemas["H3"] == ["1", "3", "5"]
        assert sliced._numbering_schemas["H5"] == ["2", "4", "6"]

        # Test slicing with H5 schema
        sliced = alt_schema_protein.slice("2", "6", schema="H5")
        assert str(sliced) == "MTK"
        assert sliced._numbering_schemas["H3"] == ["1", "3", "5"]
        assert sliced._numbering_schemas["H5"] == ["2", "4", "6"]

    def test_slice_with_gaps(self, nonseq_schema_protein):
        """Test slicing with sequences containing gaps."""
        # Test slicing around gap
        sliced = nonseq_schema_protein.slice("32", "34", schema="H3")
        assert str(sliced) == "XC-Y"
        assert sliced._numbering_schemas["H3"] == ["32", "33", "-", "34"]
        assert sliced._numbering_schemas["H5"] == ["12", "13", "14", "15"]

    def test_slice_errors(self, alt_schema_protein, nonseq_schema_protein):
        """Test error cases for slicing."""
        # Test invalid schema
        with pytest.raises(ValueError, match="Unknown schema: H1"):
            alt_schema_protein.slice("1", "5", schema="H1")

        # Test invalid positions
        with pytest.raises(ValueError, match="Position not found in schema H3"):
            alt_schema_protein.slice("2", "5", schema="H3")

        # Test end before start
        with pytest.raises(ValueError, match="Start position must be before end position"):
            alt_schema_protein.slice("5", "1", schema="H3")

        # Test positions with gaps
        with pytest.raises(ValueError, match="Unsupported position"):
            nonseq_schema_protein.slice("-", "34", schema="H3")

    def test_slice_boundaries(self, alt_schema_protein):
        """Test slicing at sequence boundaries."""
        # Test slice at start
        sliced = alt_schema_protein.slice("1", "3", schema="H3")
        assert str(sliced) == "MT"
        assert sliced._numbering_schemas["H3"] == ["1", "3"]
        assert sliced._numbering_schemas["H5"] == ["2", "4"]

        # Test slice at end
        sliced = alt_schema_protein.slice("7", "9", schema="H3")
        assert str(sliced) == "PC"
        assert sliced._numbering_schemas["H3"] == ["7", "9"]
        assert sliced._numbering_schemas["H5"] == ["8", "10"]
