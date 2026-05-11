"""CLI helper that constructs the API app."""
from src.api.main import create_app
def main() -> object:
    return create_app()
if __name__ == "__main__":
    print(main())
