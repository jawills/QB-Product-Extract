# QB Product Extract

## Tutorial

To see a full YouTube video on how to operate this script, please watch here: [youtube.com](https://youtu.be/-7kmQMZMQHU)

## Requirements
- Python 3
- Postman
- Pipenv

## Initial Setup

1. To run the script for the first time, you will need to renmame the `config.py.copy` to `config.py`. 
2. Create QBO app to get client id / client secret for authentication.
3. Follow the [Postman Instructions](https://developer.intuit.com/app/developer/qbo/docs/develop/sandboxes/postman) to get the refresh token.
4. Run `pipenv install` to install the required packages.

## Run Script

Use the following to export the data:
    pipenv shell
    python main.py
