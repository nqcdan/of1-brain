def hello(name: str = "World") -> str:
    name = name.strip() or "World"
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(hello())
