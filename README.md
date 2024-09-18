# DeNet_testApp

use different poetry environments for client and server apps


In server folder
- activate poetry using: `poetry shell`
- add all dependencies: `poetry install`
- define new `.env` file for project with next vars:
```
FILESTORE_DIR="./outfile" # example
HOST="localhost"
PORT=8000
```
- start server using `fastapi dev dn_serverapp/main.py`

In client folder
- activate poetry using: `poetry shell`
- add all dependencies: `poetry install`
- define new `.env` file for project with next vars:
```
FSTORE_URL="http://localhost:8000" (example)
```
- use client: python dn_clientapp/main.py --help

