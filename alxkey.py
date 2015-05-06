_msg_help = """
Key not set

1) Download key file at https://github.com/gomes-/alx/blob/master/alexkey.py
2) Edit the file and put your keys (don't add extra space)
3) Store in a safe place
4) Run the command

$ alx keydir /path/to/file/dir

5) Run alx-server.py
"""

alxkey_version = '0.2.0'

alxkey_azure = {
    'AZURE_STORAGE_ACCOUNT_NAME': 'your account name here',
    'AZURE_ACCESS_KEY': 'your key here',
    'AZURE_CERT_PATH_PUB': '',
    'AZURE_CERT_PATH_PRV': '',
    'AZURE_POLL': '30',
    'AZURE_INVISIBLE': '30',
    }

alxkey_aws = {
    'AWS_ACCESS_KEY_ID': 'your id here',
    'AWS_SECRET_ACCESS_KEY': 'your key here',
    'AWS_REGION': 'us-east-1',
    'AWS_SQS': 'alx-server',
    'AWS_POLL' : '30',
    'AWS_INVISIBLE': '30',
    }

alxkey_primary = 'az'