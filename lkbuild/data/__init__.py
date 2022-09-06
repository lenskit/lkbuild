"""
Built-in data for testing.
"""

from pathlib import Path
from lenskit.datasets import MovieLens

ml_small = MovieLens(Path(__file__).parent / 'ml-latest-small')
