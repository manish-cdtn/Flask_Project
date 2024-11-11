from http import HTTPStatus
from typing import Any, Dict
from flask import jsonify
import psycopg2
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)

def build_response(http_status: HTTPStatus, body: Dict[str, Any]) -> Dict[str, Any]:
    response = jsonify(body)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,x-requested-with'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = True
    response.status_code = http_status
    return response


def update_db_objects(session, model, data: dict, filters):
    try:
        if filters:
            updated_rows = session.query(model).filter(*filters).update(data, synchronize_session=False)
            if updated_rows:
                logger.info(f'DB successfully updated for {model.__tablename__} with {data} for filters {filters}')
            else:
                logger.info('DB query was success but no rows were updated')
                return True
            return updated_rows
        else:
            logger.info(f'Filters are required to perform update operation')
    except Exception as error_:
        session.rollback()
        logger.error(f'Something went wrong in updating {model.__tablename__}, {error_=}')
    return


def add_db_object(session, table_name, data):
    try:
        session.add(data)
        logger.info(f'DB successfully inserted for {table_name}')
        return True
    except Exception as error_:
        session.rollback()
        logger.error(f'Something went wrong in inserting {table_name}, {error_=}')
    return


def delete_db_object(session, model, filters):
    try:
        if filters:
            deleted_rows = session.query(model).filter(*filters).delete()
            if deleted_rows:
                logger.info(f'DB successfully deleted for {model.__tablename__} for filters {filters}')
            return (True, deleted_rows)
        else:
            logger.info(f'Filters are required to perform delete operation')
    except IntegrityError as error_:
        logger.error(f'Got IntegrityError updating {model.__tablename__}, {error_=}')
        if isinstance(error_.orig, psycopg2.errors.ForeignKeyViolation):
            return (False, 'ForeignKeyViolation: One or more ids to be deleted are in use.')
    except Exception as error_:
        logger.error(f'Something went wrong in updating {model.__tablename__}, {error_=}')
        return (False, error_)


