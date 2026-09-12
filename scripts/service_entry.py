"""Frozen executable entry point; all application logic remains in the service."""
from remixfun.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
