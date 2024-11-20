
def log_message(message, to_file=True, log_file="log.txt"):
    """Escreve log no terminal e opcionalmente em arquivo."""
    print(message)
    if to_file:
        with open(log_file, "a") as file:
            file.write(f"{message}\n")
