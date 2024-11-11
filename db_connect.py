import json
import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values


_DB_SESSION = None
_DB_ENGINE_SESSION = None

env_vars = dotenv_values()
def get_db_engine_session():
    """
    Returns DB connection engine.
    """

    global _DB_ENGINE_SESSION

    if _DB_ENGINE_SESSION is None:

        secret_name = env_vars.get("SECRET_MANAGER_NAME")
        region_name = env_vars.get("REGION")
        db_cluster_name = env_vars.get("CLUSTER_ARN")
        db_port = env_vars.get("DB_PORT")
        db_name = env_vars.get("DB_NAME")
        # Create a Secrets Manager client
        client = boto3.client('secretsmanager', region_name=region_name)

        # Retrieve the secret value
        response = client.get_secret_value(SecretId=secret_name)

        # Extract the secret value from the response
        if 'SecretString' in response:
            secret_value = json.loads(response['SecretString'])
            # print("Secret value:", secret_value['dev_github_oauth_token'])
        else:
            print('Secret value not found.')

        password = secret_value['password']
        # print("*****************************", password)
        url_str = f'postgresql://biopticon:{password}@{db_cluster_name}:{db_port}/{db_name}'
        # print("************************ ", url_str)
        _DB_ENGINE_SESSION = create_engine(url_str, connect_args={'options': '-csearch_path={}'.format('dbo')})

        return _DB_ENGINE_SESSION


def get_db_session():
    """
    Returns DB session.
    """
    global _DB_SESSION
    if _DB_SESSION is None:
        session = sessionmaker(bind=get_db_engine_session())
        _DB_SESSION = session()
    return _DB_SESSION
