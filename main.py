# main.py

def _run():
    try:
        from todo.cli import main as cli_main
    except ModuleNotFoundError:
        from cli import main as cli_main
    cli_main()

if __name__ == "__main__":
    _run()
