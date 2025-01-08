__version__ = "3.1.1b3"
# We also have the semver version since __version__ is not semver compliant
__semver_version__ = "3.1.1-beta3"

from .plugin import BenchmarkFixture

__all__ = ["BenchmarkFixture", "__version__", "__semver_version__"]
