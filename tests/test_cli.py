"""
Tests for the Nickname Forge CLI.
Initial comments in Russian, translated to English via AI tools for global accessibility.
"""

import pytest
from typer.testing import CliRunner
from nickname_forge.main import app

runner = CliRunner()


class TestBasicInvocation:
    """Tests for basic CLI calls."""

    def test_help(self):
        """--help should print usage and return 0."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Forge unique nicknames" in result.stdout

    def test_default_generation(self):
        """Default invocation (no args) should generate nicknames."""
        result = runner.invoke(app, [])
        assert result.exit_code == 0
        assert "Forged Nicknames" in result.stdout

    def test_no_score_flag(self):
        """--no-score should hide the Score column."""
        result = runner.invoke(app, ["--no-score"])
        assert result.exit_code == 0
        assert "Score" not in result.stdout
        assert "Forged Nicknames" in result.stdout


class TestStyleOption:
    """Tests for --style / -s."""

    def test_cyberpunk_style(self):
        result = runner.invoke(app, ["--style", "cyberpunk", "--count", "3"])
        assert result.exit_code == 0
        assert "Forged Nicknames" in result.stdout

    def test_fantasy_style(self):
        result = runner.invoke(app, ["--style", "fantasy", "--count", "3"])
        assert result.exit_code == 0

    def test_space_style(self):
        result = runner.invoke(app, ["--style", "space", "--count", "3"])
        assert result.exit_code == 0

    def test_steampunk_style(self):
        result = runner.invoke(app, ["--style", "steampunk", "--count", "3"])
        assert result.exit_code == 0

    def test_short_style_flag(self):
        result = runner.invoke(app, ["-s", "space", "--count", "2"])
        assert result.exit_code == 0

    def test_invalid_style(self):
        result = runner.invoke(app, ["--style", "foobar"])
        assert result.exit_code == 1
        assert "Error" in result.stdout or "not found" in result.stdout


class TestCountOption:
    """Tests for --count / -c."""

    def test_count_1(self):
        result = runner.invoke(app, ["--count", "1"])
        assert result.exit_code == 0

    def test_count_respects_max(self):
        result = runner.invoke(app, ["--count", "100"])
        assert result.exit_code != 0

    def test_count_respects_min(self):
        result = runner.invoke(app, ["--count", "0"])
        assert result.exit_code != 0

    def test_short_count_flag(self):
        result = runner.invoke(app, ["-c", "5"])
        assert result.exit_code == 0


class TestSeparatorOption:
    """Tests for --sep."""

    def test_dash_separator(self):
        result = runner.invoke(app, ["--sep", "-", "--count", "5", "--no-score"])
        assert result.exit_code == 0
        assert "-" in result.stdout

    def test_underscore_separator(self):
        result = runner.invoke(app, ["--sep", "_", "--count", "5", "--no-score"])
        assert result.exit_code == 0
        assert "_" in result.stdout

    def test_empty_separator(self):
        result = runner.invoke(app, ["--count", "10", "--no-score"])
        assert result.exit_code == 0
        names_part = result.stdout.split("Forged Nicknames")[1]
        core_part = names_part.split("Forge complete")[0]
        assert "-" not in core_part
        assert "_" not in core_part


class TestListStyles:
    """Tests for --list-styles / -l."""

    def test_list_styles(self):
        result = runner.invoke(app, ["--list-styles"])
        assert result.exit_code == 0
        assert "cyberpunk" in result.stdout
        assert "fantasy" in result.stdout
        assert "space" in result.stdout
        assert "steampunk" in result.stdout

    def test_short_list_styles(self):
        result = runner.invoke(app, ["-l"])
        assert result.exit_code == 0
        assert "Available Styles" in result.stdout

    def test_list_styles_shows_examples(self):
        result = runner.invoke(app, ["--list-styles"])
        assert result.exit_code == 0
        assert "Example" in result.stdout


class TestScoreOption:
    """Tests for --score / --no-score."""

    def test_score_shown_by_default(self):
        result = runner.invoke(app, ["--count", "3"])
        assert result.exit_code == 0
        assert "Score" in result.stdout

    def test_no_score_hides_score(self):
        result = runner.invoke(app, ["--no-score", "--count", "3"])
        assert result.exit_code == 0
        assert "Score" not in result.stdout

    def test_explicit_score(self):
        result = runner.invoke(app, ["--score", "--count", "3"])
        assert result.exit_code == 0
        assert "Score" in result.stdout


class TestEdgeCases:
    """Boundary and combination tests."""

    def test_count_max_boundary(self):
        result = runner.invoke(app, ["--count", "50"])
        assert result.exit_code == 0

    def test_count_min_boundary(self):
        result = runner.invoke(app, ["--count", "1"])
        assert result.exit_code == 0

    def test_multiple_flags_combined(self):
        result = runner.invoke(
            app,
            ["--style", "space", "--count", "5", "--sep", "-", "--no-score"],
        )
        assert result.exit_code == 0
        assert "-" in result.stdout
        assert "Score" not in result.stdout


class TestSaveOption:
    """Tests for --save."""

    def test_save_creates_file(self, tmp_path):
        filepath = tmp_path / "output.txt"
        result = runner.invoke(app, ["--save", str(filepath), "--count", "5"])
        assert result.exit_code == 0
        assert filepath.exists()

    def test_save_shows_confirmation(self, tmp_path):
        filepath = tmp_path / "output.txt"
        result = runner.invoke(app, ["--save", str(filepath), "--count", "3"])
        assert "Saved" in result.stdout
        assert "output.txt" in result.stdout

    def test_saved_file_has_correct_line_count(self, tmp_path):
        filepath = tmp_path / "output.txt"
        runner.invoke(app, ["--save", str(filepath), "--count", "10"])

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) == 10