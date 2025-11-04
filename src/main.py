"""Core module to run the Universe Simulator application."""
from src.core.engine import Engine

def main():
    """Entry point for the Universe Simulator application."""
    engine = Engine()
    engine.run()

if __name__ == "__main__":
    main()
