<h1> Before setting up the server do the following:<h1>

instatiate the .env file with variables

    FILESTORE_DIR="../outfile/"
    HOST="localhost"
    PORT_NUMBER="8000"


- need to instatiate the filestore directory before setting up the server and

- to test the upload/download function you can create a custom object with in unix systems(mac was used):
 `head -c 4294967296 /dev/urandom > bigfile.dat`
  download function sends the big file, but browser won't handle it
`