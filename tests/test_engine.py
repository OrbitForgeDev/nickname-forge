"""
Tests for the Nickname Forge engine.
Initial comments in Russian, translated to English via AI tools for global accessibility.
"""

import pytest
from nickname_forge.engine import NicknameForge, Nickname, StyleNotFoundError


@pytest.fixture
def forge():
    """Create a fresh NicknameForge instance for each test."""
    return NicknameForge()


class TestNicknameForgeInit:
    """Tests for engine initialization."""

    def test_available_styles_loaded(self, forge):
        """JSON styles should be automatically loaded on init."""
        styles = forge.available_styles
        assert "cyberpunk" in styles
        assert "fantasy" in styles
        assert "space" in styles
        assert "steampunk" in styles
        assert len(styles) == 4

    def test_available_styles_returns_sorted_list(self, forge):
        """Style list should be alphabetically sorted."""
        styles = forge.available_styles
        assert styles == sorted(styles)


class TestGenerate:
    """Tests for single nickname generation."""

    def test_generate_returns_nickname_object(self, forge):
        """Result should be a Nickname instance."""
        result = forge.generate("cyberpunk")
        assert isinstance(result, Nickname)

    def test_generate_has_name(self, forge):
        """Generated nickname should have a non-empty name."""
        result = forge.generate("fantasy")
        assert result.name
        assert len(result.name) > 0

    def test_generate_has_style(self, forge):
        """Nickname should store its source style."""
        result = forge.generate("space")
        assert result.style == "space"

    def test_generate_has_score_in_range(self, forge):
        """Score should always be between 0 and 100."""
        result = forge.generate("cyberpunk")
        assert 0 <= result.score <= 100

    def test_generate_different_styles_produce_different_results(self, forge):
        """Different styles should use different word pools."""
        cyber_names = set()
        space_names = set()

        for _ in range(20):
            cyber_names.add(forge.generate("cyberpunk").name)
            space_names.add(forge.generate("space").name)

        assert cyber_names != space_names

    def test_generate_with_separator(self, forge):
        """Separator should appear between name parts."""
        result = forge.generate("cyberpunk", separator="-")
        parts = result.name.split("-")
        assert len(parts) == 3

    def test_generate_with_empty_separator(self, forge):
        """Default empty separator produces a solid string."""
        result = forge.generate("cyberpunk", separator="")
        assert " " not in result.name

    def test_generate_unknown_style_raises_error(self, forge):
        """Unknown style should raise StyleNotFoundError with a helpful message."""
        with pytest.raises(StyleNotFoundError) as exc_info:
            forge.generate("foobar")
        assert "foobar" in str(exc_info.value)
        assert "Available styles" in str(exc_info.value)

    def test_generate_str_representation(self, forge):
        """str(nickname) should return just the name."""
        nick = forge.generate("cyberpunk")
        assert str(nick) == nick.name

    def test_generate_repr_representation(self, forge):
        """repr(nickname) should include all metadata."""
        nick = forge.generate("cyberpunk")
        r = repr(nick)
        assert nick.name in r
        assert str(nick.style) in r
        assert str(nick.score) in r


class TestGenerateBatch:
    """Tests for batch generation."""

    def test_batch_returns_correct_count(self, forge):
        """Batch should return exactly the requested count."""
        batch = forge.generate_batch("cyberpunk", count=7)
        assert len(batch) == 7

    def test_batch_default_count_is_10(self, forge):
        """Default batch size should be 10."""
        batch = forge.generate_batch("cyberpunk")
        assert len(batch) == 10

    def test_batch_all_elements_are_nickname_objects(self, forge):
        """Every element in the batch should be a Nickname."""
        batch = forge.generate_batch("fantasy", count=5)
        for item in batch:
            assert isinstance(item, Nickname)

    def test_batch_respects_unique_flag(self, forge):
        """When unique=True, no duplicate names should appear."""
        batch = forge.generate_batch("space", count=10, unique=True)
        names = [n.name for n in batch]
        assert len(names) == len(set(names))

    def test_batch_unknown_style_raises_error(self, forge):
        """Batch with unknown style should raise StyleNotFoundError."""
        with pytest.raises(StyleNotFoundError):
            forge.generate_batch("invalid", count=5)

    def test_batch_with_separator(self, forge):
        """Names in batch should contain the given separator."""
        batch = forge.generate_batch("fantasy", count=5, separator="_")
        for nick in batch:
            assert "_" in nick.name


class TestExportToFile:
    """Tests for file export functionality."""

    def test_export_creates_file(self, forge, tmp_path):
        """Export should create the target file."""
        filepath = tmp_path / "test_nicknames.txt"
        count = forge.export_to_file("cyberpunk", str(filepath), count=5)

        assert count == 5
        assert filepath.exists()

    def test_export_file_content(self, forge, tmp_path):
        """Exported file should contain the correct number of non-empty lines."""
        filepath = tmp_path / "test_nicknames.txt"
        count = forge.export_to_file("fantasy", str(filepath), count=7)

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) == 7
        for line in lines:
            assert line.strip()

    def test_export_unknown_style_raises_error(self, forge, tmp_path):
        """Export with unknown style should raise StyleNotFoundError."""
        filepath = tmp_path / "test_nicknames.txt"
        with pytest.raises(StyleNotFoundError):
            forge.export_to_file("invalid_style", str(filepath))

    def test_export_with_separator(self, forge, tmp_path):
        """Exported names should include the chosen separator."""
        filepath = tmp_path / "test_sep.txt"
        forge.export_to_file("space", str(filepath), count=3, separator="-")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        assert "-" in content


class TestNickname:
    """Tests for the Nickname data class."""

    def test_nickname_creation(self):
        """Should store all supplied fields."""
        nick = Nickname(name="TestName", style="test", score=85)
        assert nick.name == "TestName"
        assert nick.style == "test"
        assert nick.score == 85

    def test_nickname_str(self):
        """String representation should be the name."""
        nick = Nickname(name="OrbitForgeDev", style="space", score=100)
        assert str(nick) == "OrbitForgeDev"

    def test_nickname_repr(self):
        """Repr should contain all fields for debugging."""
        nick = Nickname(name="OrbitForgeDev", style="space", score=100)
        r = repr(nick)
        assert "OrbitForgeDev" in r
        assert "space" in r
        assert "100" in r