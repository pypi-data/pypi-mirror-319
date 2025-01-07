from allsafe.modules import ConsoleStream, encrypt

import os


__version__ = "1.1.2"

def get_description():
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    desc_file_path = os.path.join(parent_dir, "DESCRIPTION.txt")
    desc = ""
    with open(desc_file_path, 'r') as f:
        desc = f.read()
    
    return desc
    
def handle_inputs(console: ConsoleStream):
    addr_sample = console.styles.gray("(e.g Battle.net)")
    addr = console.ask(f"Enter app address/name {addr_sample}",
                       case_sensitive=False)

    username_sample = console.styles.gray("(e.g user123)")
    username = console.ask(f"Enter username {username_sample}",
                           case_sensitive=False)

    case_note = console.styles.gray("(case-sensitive)")
    note = "(do [bold]NOT[/bold] forget this), " + case_note
    secret_key = console.ask(f"Enter secret key {note}")

    return (addr, username, secret_key)

def print_passwds(console: ConsoleStream, passwds: list):
    md_passwds = [console.styles.passwd(i) for i in passwds]
    console.write(
        "\n"
        f"🔒 8-Length Password:\t{md_passwds[0]}\n"
        f"🔏 16-Length Password:\t{md_passwds[1]}\n"
        f"🔐 24-Length Password:\t{md_passwds[2]}\n"
    )

def main():
    console = ConsoleStream()
    description = get_description()
    
    console.panel("[bold]AllSafe[/bold] Modern Password Generator", description, style=console.styles.GRAY)
    console.write(":link: Github: https://github.com/emargi/allsafe")
    console.write(":gear: Version: " + __version__ + "\n")

    addr, username, secret_key = handle_inputs(console)
    # I don't know if we would ever need statuses
    with console.status("Encrypting..."):
        passwds = encrypt(secret_key, addr, username)
    
    print_passwds(console, passwds)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)

