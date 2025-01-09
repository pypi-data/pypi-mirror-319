import sys

if sys.version_info.major < 3:
    raise ValueError("Incompatible with Python2")


version = "1.0.3"
compatible_versions = ("0.4", "0.5", "1", "1.0.1", "1.0.2", "1.0.3")
