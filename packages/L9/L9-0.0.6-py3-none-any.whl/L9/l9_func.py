def l9_print() -> None:
    """Display the L9 in the console."""
    print("L9")

def l9_advertising() -> None:
    """Display the L9 advertising in the console."""
    print("L9! Low cost services. Boosting LPs. 5/5 stars rating. Fast answers. 24/7 support. 100% satisfaction guaranteed.")

def l9_lnineazer(message: str) -> str:
    """Transform the message into an L9 message."""
    return f"/!\\ L9 {"".join([char.upper() if index % 2 else char.lower() for index, char in enumerate(message)])} L9 /!\\"

if __name__ == "__main__":
    l9()
    l9_advertising()
    print(l9_lnineazer("Hello, World!"))