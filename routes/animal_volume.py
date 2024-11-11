from http import HTTPStatus
from flask import Blueprint, request
from db_connect import get_db_session
from services.animal_volume_service import AnimalVolumeService
from util.commom_util import build_response


animal_volume_measurements_bp = Blueprint(
    name='animal_volume_measurements_bp',
    import_name=__name__,
    url_prefix = '/organizations'
)


@animal_volume_measurements_bp.route('/<uuid:organization_id>/studies/<uuid:study_id>/animal_volume/animal_id/<uuid:animal_id>', methods=['GET'])
def get_animal_volume(organization_id, study_id, animal_id):
    session = get_db_session()
    try:               
        service = AnimalVolumeService(session)
        animal_volume_data = service.get_animal_volume(animal_id)  
        return build_response(http_status=HTTPStatus.OK, body={'data': animal_volume_data})    
    except Exception as error_:
        return build_response(http_status=HTTPStatus.INTERNAL_SERVER_ERROR, body={'error': f'{error_}'})
    
    
@animal_volume_measurements_bp.route('/<uuid:organization_id>/studies/<uuid:study_id>/animal_volume', methods=['POST'])
def insert_animal_volume(organization_id, study_id):
    session = get_db_session()
    try:               
        request_data = request.json
        
        service = AnimalVolumeService(session)
        create_animal_vol_response = service.create_animal_volume(study_id, request_data)  
        session.commit()
        return build_response(http_status=HTTPStatus.OK, body=create_animal_vol_response) 
    except Exception as e:
        session.rollback()
        return build_response(http_status=HTTPStatus.INTERNAL_SERVER_ERROR, body={'error': f'{e}'})
    
    
@animal_volume_measurements_bp.route('/<uuid:organization_id>/studies/<uuid:study_id>/animal_volume', methods=['PATCH'])
def update_animal_volume(organization_id, study_id):
    session = get_db_session()
    try:               
        request_data = request.json
        
        service = AnimalVolumeService(session)
        create_animal_vol_response = service.update_animal_volume(request_data)  
        session.commit()
        return build_response(http_status=HTTPStatus.OK, body=create_animal_vol_response) 
    except Exception as e:
        session.rollback()
        return build_response(http_status=HTTPStatus.INTERNAL_SERVER_ERROR, body={'error': f'{e}'})
    
    
@animal_volume_measurements_bp.route('/<uuid:organization_id>/studies/<uuid:study_id>/animal_volume', methods=['DELETE'])
def delete_animal_volume(organization_id, study_id):
    session = get_db_session()
    try:               
        request_data = request.json
        
        service = AnimalVolumeService(session)
        delete_animal_vol_response = service.delete_animal_volume(request_data)  
        session.commit()
        return build_response(http_status=HTTPStatus.OK, body=delete_animal_vol_response) 
    except Exception as e:
        session.rollback()
        return build_response(http_status=HTTPStatus.INTERNAL_SERVER_ERROR, body={'error': f'{e}'})
    
    