"""Utility classes for handling numbered protein sequences."""

from typing import Dict, List, Union

import Bio.Seq as bs
from Bio.Data import IUPACData

ALLOWED_LETTERS = set(IUPACData.protein_letters + "X-*")
ALLOWED_LETTERS_LITE = set(IUPACData.protein_letters + "X")


class NumberedResidue:
    """A class representing a single amino acid residue with position numbers in different schemas.

    This class holds a single amino acid residue and its position numbers in different
    numbering schemas (e.g., H1, H3). It provides validation for amino acid letters
    and formatting for string representation.

    Attributes:
        residue: The amino acid letter.
        number_dict: Dictionary mapping schema names to position numbers.
    """

    def __init__(
        self,
        residue: str = "-",
        number_dict: Dict[Union[str, int], Union[str, int]] = {},
    ) -> None:
        """Initialize a NumberedResidue instance.

        Args:
            residue: The amino acid letter. Defaults to "-" (gap).
            number_dict: Dictionary mapping schema names to position numbers.
                Keys and values are converted to strings. Defaults to empty dict.

        Raises:
            ValueError: If residue is not a single letter or not a valid amino acid.
        """
        self.residue = residue
        self.number_dict = number_dict

    @property
    def residue(self) -> str:
        return self._residue

    @residue.setter
    def residue(self, value: str) -> None:
        value = str(value)
        if len(value) != 1:
            raise ValueError("Only one letter accepted")
        if value not in ALLOWED_LETTERS:
            raise ValueError("Not an amino acid letter")
        self._residue = value

    @property
    def number_dict(self) -> Dict[str, str]:
        return self._number_dict

    @number_dict.setter
    def number_dict(self, value: Dict[Union[str, int], Union[str, int]]) -> None:
        value = {str(k): str(v) for k, v in value.items()}
        self._number_dict = value

    def __repr__(self) -> str:
        contents = [f"|{self.residue}|"] + [
            f"{k}|{v}|" for k, v in self.number_dict.items()
        ]
        return NumberedResidue._align_repr(contents)

    @classmethod
    def _align_repr(cls, contents: List[str]) -> str:
        """Align the string representation of residue and its numbering.

        Args:
            contents: List of strings to align, each containing pipe-separated values.

        Returns:
            str: Aligned string representation with consistent spacing.
        """
        first_pipe_positions = [item.index("|") for item in contents]
        max_first_pipe = max(first_pipe_positions)

        processed_list = []
        for item in contents:
            first_pipe = item.index("|")
            first_blank = " " * (max_first_pipe - first_pipe)
            aligned_item = item[:first_pipe] + first_blank + item[first_pipe:]
            processed_list.append(aligned_item)

        second_pipe_positions = [
            item.index("|", item.index("|") + 1) for item in processed_list
        ]
        max_second_pipe = max(second_pipe_positions)

        res_list = []
        for item in processed_list:
            first_pipe = item.index("|")
            second_pipe = item.index("|", first_pipe + 1)
            second_blank_len = max_second_pipe - second_pipe
            aligned_item = (
                item[:first_pipe]
                + "|"
                + item[(first_pipe + 1) : second_pipe].center(
                    second_blank_len + second_pipe - first_pipe - 1
                )
                + "|"
            )

            res_list.append(aligned_item)

        res = "\n".join(res_list)

        return res


class NumberedProtein:
    """A class representing a protein sequence with multiple numbering schemas.

    This class manages a protein sequence and its numbering in different schemas
    (e.g., H1, H3). It supports sequence mutations and maintains a history of
    mutations in the default schema.

    Attributes:
        raw_seq: The original sequence.
        seq: The current sequence after any mutations.
        default_schema: The default numbering schema for mutation reporting.
    """

    def __init__(
        self,
        seq: str,
        numberings: Dict[str, List[str]] = None,
        default_schema: str = "orig",
    ) -> None:
        """Initialize a NumberedProtein instance.

        Args:
            seq: The protein sequence.
            numberings: Dictionary mapping schema names to lists of position numbers.
                Each list must match the sequence length. Defaults to None.
            default_schema: The default schema for mutation reporting. Defaults to "orig".

        Raises:
            ValueError: If sequence contains invalid amino acids.
            ValueError: If numbering schema length doesn't match sequence length.
            ValueError: If duplicate numbers are detected in a schema (except gaps).
        """
        assert set(seq).issubset(ALLOWED_LETTERS), "Not amino acid letter"

        self._raw_seq = bs.Seq(seq)
        self._seq = bs.MutableSeq(seq)
        self._numbering_schemas = {}
        self._mutations = {}  # Dict to store current mutations by position

        # Add original numbering schema (1-based indexing)
        orig_schema = [str(i + 1) for i in range(len(seq))]
        self._numbering_schemas["orig"] = orig_schema

        # Add user-provided schemas
        if numberings:
            for schema_name, numbers in numberings.items():
                if len(numbers) != len(seq):
                    raise ValueError(
                        f"Schema {schema_name} length doesn't match sequence length"
                    )
                # duplication not allow except for '-'
                numbers_check = [n for n in numbers if n != "-"]
                if len(numbers_check) != len(set(numbers_check)):
                    raise ValueError(
                        f"Duplicate numbers detected in schema {schema_name}"
                    )
                self._numbering_schemas[schema_name] = numbers

        self.default_schema = default_schema

    @property
    def raw_seq(self) -> str:
        """Get the original sequence.

        Returns:
            str: The original sequence before any mutations.
        """
        return str(self._raw_seq)

    @property
    def seq(self) -> str:
        """Get the current sequence after any mutations.

        Returns:
            str: The current sequence including any mutations.
        """
        return str(self._seq)

    @property
    def mutations(self) -> List[str]:
        """Get the list of mutations in the format 'X#Y'.

        X is the original residue, # is the position in default_schema,
        Y is the new residue. Reversion mutations are automatically removed.

        Returns:
            List[str]: List of mutations ordered by position number.
        """

        def get_pos(mutation_str):
            pos = ""
            for char in mutation_str[1:-1]:  # Skip first and last chars (residues)
                pos += char
            try:
                return int(pos)
            except ValueError:
                # For special positions that can't be converted to int,
                # use a large number to put them at the end
                return float("inf")

        return sorted(self._mutations.values(), key=get_pos)

    def get_residue(
        self, schema: str = "orig", position: Union[str, int] = None
    ) -> NumberedResidue:
        """Get a residue by its position in a specific schema.

        Args:
            schema: The numbering schema to use. Defaults to "orig".
            position: The position in the specified schema.

        Returns:
            NumberedResidue: The residue at the specified position.

        Raises:
            ValueError: If schema is unknown or position is not found.
        """
        if schema not in self._numbering_schemas:
            raise ValueError(f"Unknown schema: {schema}")

        if schema == "orig" and isinstance(position, int):
            if position < 1 or position > len(self._seq):
                raise ValueError(f"Position {position} out of range")
            idx = position - 1
        else:
            # Convert position to string for comparison
            position = str(position)
            try:
                idx = self._numbering_schemas[schema].index(position)
            except ValueError:
                raise ValueError(f"Position {position} not found in schema {schema}")

        # Create number_dict for the residue
        number_dict = {
            schema_name: numbers[idx]
            for schema_name, numbers in self._numbering_schemas.items()
        }

        return NumberedResidue(residue=self._seq[idx], number_dict=number_dict)

    def replace_residue(
        self,
        schema: str = "orig",
        position: Union[str, int] = None,
        new_residue: str = None,
    ) -> None:
        """Replace a residue at a specific position.

        Args:
            schema: The numbering schema to use. Defaults to "orig".
            position: The position in the specified schema.
            new_residue: The new amino acid to insert.

        Raises:
            ValueError: If schema is unknown, position is not found, or residue is invalid.
        """
        if schema not in self._numbering_schemas:
            raise ValueError(f"Unknown schema: {schema}")

        if schema == "orig" and isinstance(position, int):
            if position < 1 or position > len(self._seq):
                raise ValueError(f"Position {position} out of range")
            idx = position - 1
        else:
            # Convert position to string for comparison
            position = str(position)
            try:
                idx = self._numbering_schemas[schema].index(position)
            except ValueError:
                raise ValueError(f"Position {position} not found in schema {schema}")

        # Validate new_residue
        if (
            not new_residue
            or len(new_residue) != 1
            or new_residue not in ALLOWED_LETTERS
        ):
            raise ValueError("Invalid residue")

        # Record mutation in default schema format
        old_residue = self._seq[idx]
        default_pos = self._numbering_schemas[self.default_schema][idx]
        mutation = f"{old_residue}{default_pos}{new_residue}"

        # Check if this mutation reverts to the original sequence
        orig_residue = self._raw_seq[idx]
        if new_residue == orig_residue:
            # If reverting to original, remove the mutation record
            self._mutations.pop(default_pos, None)
        else:
            # Otherwise, record the current mutation
            self._mutations[default_pos] = mutation

        # Apply the mutation
        self._seq[idx] = new_residue

    def slice(
        self, start: Union[str, int], end: Union[str, int], schema: str = "orig"
    ) -> "NumberedProtein":
        """Slice the protein sequence based on a specific numbering schema.

        Args:
            start: Start position in the specified schema.
            end: End position in the specified schema.
            schema: The numbering schema to use. Defaults to "orig".

        Returns:
            NumberedProtein: A new instance containing the sliced sequence
                and corresponding numberings.

        Raises:
            ValueError: If schema is unknown, positions are invalid or contain gaps,
                or end position is before start position.
        """

        start, end = str(start), str(end)
        if schema not in self._numbering_schemas:
            raise ValueError(f"Unknown schema: {schema}")
        if start == "-" or end == "-":
            raise ValueError("Unsupported position")

        # Find indices in the sequence
        try:
            start_idx = self._numbering_schemas[schema].index(start)
            end_idx = self._numbering_schemas[schema].index(end) + 1
        except ValueError:
            raise ValueError(f"Position not found in schema {schema}")

        if end_idx < start_idx:
            raise ValueError("Start position must be before end position")

        # Create new numbering schemas for the slice
        new_numberings = {}
        for schema_name, numbers in self._numbering_schemas.items():
            new_numberings[schema_name] = numbers[start_idx:end_idx]

        # Create new NumberedProtein with sliced sequence and numberings
        return NumberedProtein(
            seq=str(self._seq[start_idx:end_idx]),
            numberings=new_numberings,
            default_schema=self.default_schema,
        )

    def __len__(self) -> int:
        """Return the length of the sequence.

        Returns:
            int: The length of the current sequence.
        """
        return len(self.seq)

    def __str__(self) -> str:
        """Return the current sequence as a string.

        Returns:
            str: The current sequence.
        """
        return self.seq

    def __repr__(self) -> str:
        """Return a detailed representation including schemas.

        Returns:
            str: String representation showing sequence and available schemas.
        """
        return f"NumberedProtein(sequence='{self.seq}', schemas={list(self._numbering_schemas.keys())})"
