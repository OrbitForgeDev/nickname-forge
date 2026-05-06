"""
Core generation engine for Nickname Forge.
Combines style templates into unique nicknames.
Initial comments in Russian, translated to English via AI tools for global accessibility.
"""

import json
import random
from pathlib import Path
from typing import Optional

# Path to the data directory relative to this file
DATA_DIR = Path(__file__).resolve().parent / "data"


class StyleNotFoundError(Exception):
    """Raised when a requested style does not exist."""
    pass


class Nickname:
    """Represents a generated nickname with metadata."""

    def __init__(self, name: str, style: str, score: int):
        self.name = name
        self.style = style
        self.score = score

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Nickname(name='{self.name}', style='{self.style}', score={self.score})"


class NicknameForge:
    """
    Main engine that loads templates and forges nicknames.
    """

    def __init__(self):
        self._templates: dict[str, dict] = {}
        self._load_all_styles()

    def _load_all_styles(self) -> None:
        """Load all JSON style files from the data directory."""
        if not DATA_DIR.exists():
            raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")

        for json_file in DATA_DIR.glob("*.json"):
            style_name = json_file.stem  # filename without extension
            with open(json_file, "r", encoding="utf-8") as f:
                self._templates[style_name] = json.load(f)

    @property
    def available_styles(self) -> list[str]:
        """Return a sorted list of loaded style names."""
        return sorted(self._templates.keys())

    def _calculate_score(self, name: str) -> int:
        """
        Calculate a readability score for the nickname (0-100).
        Higher is better.
        """
        score = 50  # baseline

        # Longer names (>10 chars) get a bonus for uniqueness
        if len(name) > 10:
            score += 15
        elif len(name) < 6:
            score -= 10

        # Bonus for mixed case
        has_upper = any(c.isupper() for c in name)
        has_lower = any(c.islower() for c in name)
        if has_upper and has_lower:
            score += 10

        # Penalty for three consecutive identical letters
        for i in range(len(name) - 2):
            if name[i].lower() == name[i+1].lower() == name[i+2].lower():
                score -= 20
                break

        return max(0, min(100, score))

    def generate(self, style: str, separator: str = "") -> Nickname:
        """
        Generate a single nickname in the given style.

        Args:
            style: Style name (e.g., 'cyberpunk', 'fantasy', 'space', 'steampunk').
            separator: String to join parts (e.g., '-', '_', '').

        Returns:
            A Nickname object.

        Raises:
            StyleNotFoundError: If the requested style does not exist.
        """
        if style not in self._templates:
            available = ", ".join(self.available_styles)
            raise StyleNotFoundError(
                f"Style '{style}' not found. Available styles: {available}"
            )

        template = self._templates[style]
        prefix = random.choice(template["prefixes"])
        root = random.choice(template["roots"])
        suffix = random.choice(template["suffixes"])

        parts = [prefix, root, suffix]
        name = separator.join(parts)
        score = self._calculate_score(name)

        return Nickname(name=name, style=style, score=score)

    def generate_batch(
        self,
        style: str,
        count: int = 10,
        separator: str = "",
        unique: bool = True,
    ) -> list[Nickname]:
        """
        Generate multiple nicknames at once.

        Args:
            style: Style name.
            count: Number of nicknames to generate.
            separator: String to join parts.
            unique: If True, avoid duplicate names in the batch.

        Returns:
            A list of Nickname objects.

        Raises:
            StyleNotFoundError: If the requested style does not exist.
        """
        if style not in self._templates:
            available = ", ".join(self.available_styles)
            raise StyleNotFoundError(
                f"Style '{style}' not found. Available styles: {available}"
            )

        results: list[Nickname] = []
        seen_names: set[str] = set()

        # Safety limit to prevent infinite loops when unique=True and pool is small
        max_attempts = count * 20
        attempts = 0

        while len(results) < count and attempts < max_attempts:
            nickname = self.generate(style=style, separator=separator)
            attempts += 1

            if unique and nickname.name in seen_names:
                continue

            seen_names.add(nickname.name)
            results.append(nickname)

        return results

    def export_to_file(
        self,
        style: str,
        filepath: str,
        count: int = 10,
        separator: str = "",
    ) -> int:
        """
        Generate nicknames and save them to a text file.

        Args:
            style: Style name.
            filepath: Path to the output file.
            count: Number of nicknames to generate.
            separator: String to join parts.

        Returns:
            Number of nicknames written to the file.

        Raises:
            StyleNotFoundError: If the requested style does not exist.
            IOError: If the file cannot be written.
        """
        nicknames = self.generate_batch(
            style=style,
            count=count,
            separator=separator,
            unique=True,
        )

        with open(filepath, "w", encoding="utf-8") as f:
            for nick in nicknames:
                f.write(f"{nick.name}\n")

        return len(nicknames)


# Quick demo when run directly
if __name__ == "__main__":
    forge = NicknameForge()
    print("Available styles:", forge.available_styles)
    print()

    for style_name in forge.available_styles:
        name = forge.generate(style_name, separator="")
        print(f"[{style_name}] {name}")
    print()

    print("Batch of 5 cyberpunk nicknames:")
    for n in forge.generate_batch("cyberpunk", count=5):
        print(f"  {n.name} (score: {n.score})")