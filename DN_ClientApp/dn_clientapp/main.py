import os

import typer
from dotenv import load_dotenv

from routes import files


load_dotenv()
app = typer.Typer()

app.add_typer(files.app, name="files")

@app.command(name="init")
def init(path_to_config: str) -> str:
    """
    use this command to instantiate the config file with user data and possible auth data
    """
    if not os.path.exists(f'{path_to_config}/config.ini'):
        with open(f'{path_to_config}/config.ini', 'a+') as file:
            file.write('[AUTH_DATA]\n')
            file.write('username =\n')
            file.write('password =\n')
    else:
        print('config file exists')


def main():
    app()

if __name__ == "__main__":
    main()
