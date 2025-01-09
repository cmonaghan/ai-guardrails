# AI Guardrail

## Setup

Install dependencies

    pyenv local env
    pip install -r requirements.txt

Create IAM machine user with permissions only to apply guardrails

    TBD

Set credentials

    # create .env file
    touch .env

    # Save the following in your .env file
    AWS_ACCESS_KEY_ID="<key_id>"
    AWS_SECRET_ACCESS_KEY="<key_value>"
    GUARDRAIL_IDENTIFIER="5mkwbr0dnqvg"
    GUARDRAIL_VERSION="1"
