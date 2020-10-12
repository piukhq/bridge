from os import getenv

CLIENT_SECRET = "2Ai8l8~Utj0_Jo3umKA.7-cRgrb57fgBlG"
CLIENT_ID = "762b5e54-6eac-4ffb-a298-3b75ec79b402"
AUTHORITY = "https://login.microsoftonline.com/a6e2367a-92ea-4e5a-b565-723830bcc095"
REDIRECT_PATH = "/oidc_callback"  # It will be used to form an absolute URL
SESSION_TYPE = "filesystem"
SESSION_FILE_DIR = "/tmp"
CONNECTION_STRING = getenv("CONNECTION_STRING")
TEMPLATES_AUTO_RELOAD = True
