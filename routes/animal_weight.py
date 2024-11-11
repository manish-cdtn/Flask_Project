from http import HTTPStatus
from flask import Blueprint, request
from db_connect import get_db_session
from services.animal_weight_service import AnimalWeightService
from util.commom_util import build_response


animal_weight_measurements_bp = Blueprint(
    name='animal_weight_measurements_bp',
    import_name=__name__,
    url_prefix = '/organizations'
)


@animal_weight_measurements_bp.route('/<uuid:organization_id>/studies/<uuid:study_id>/animal_weight/animal_id/<uuid:animal_id>', methods=['GET'])
def get_animal_weight(organization_id, study_id, animal_id):
    session = get_db_session()
    try:               
        service = AnimalWeightService(session)
        animal_weight_data = service.get_animal_weight(animal_id)  
        return build_response(http_status=HTTPStatus.OK, body={'data': animal_weight_data})    
    except Exception as error_:
        return build_response(http_status=HTTPStatus.INTERNAL_SERVER_ERROR, body={'error': f'{error_}'})
    
    
@animal_weight_measurements_bp.route('/<uuid:organization_id>/studies/<uuid:study_id>/animal_weight', methods=['POST'])
def insert_animal_weight(organization_id, study_id):
    session = get_db_session()
    try:               
        request_data = request.json
        
        service = AnimalWeightService(session)
        create_animal_wgt_response = service.create_animal_weight(study_id, request_data)  
        session.commit()
        return build_response(http_status=HTTPStatus.OK, body=create_animal_wgt_response) 
    except Exception as e:
        session.rollback()
        return build_response(http_status=HTTPStatus.INTERNAL_SERVER_ERROR, body={'error': f'{e}'})
    
    
@animal_weight_measurements_bp.route('/<uuid:organization_id>/studies/<uuid:study_id>/animal_weight', methods=['PATCH'])
def update_animal_weight(organization_id, study_id):
    session = get_db_session()
    try:               
        request_data = request.json
        
        service = AnimalWeightService(session)
        create_animal_wgt_response = service.update_animal_weight(request_data)  
        session.commit()
        return build_response(http_status=HTTPStatus.OK, body=create_animal_wgt_response) 
    except Exception as e:
        session.rollback()
        return build_response(http_status=HTTPStatus.INTERNAL_SERVER_ERROR, body={'error': f'{e}'})
    
    
@animal_weight_measurements_bp.route('/<uuid:organization_id>/studies/<uuid:study_id>/animal_weight', methods=['DELETE'])
def delete_animal_weight(organization_id, study_id):
    session = get_db_session()
    try:               
        request_data = request.json
        
        service = AnimalWeightService(session)
        delete_animal_wgt_response = service.delete_animal_weight(request_data)  
        session.commit()
        return build_response(http_status=HTTPStatus.OK, body=delete_animal_wgt_response) 
    except Exception as e:
        session.rollback()
        return build_response(http_status=HTTPStatus.INTERNAL_SERVER_ERROR, body={'error': f'{e}'})
    
    