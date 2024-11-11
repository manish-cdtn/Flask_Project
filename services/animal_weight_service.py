from typing import Dict, List
from uuid import UUID
import uuid
from venv import logger
from models import Animal, AnimalWeightMeasurement
from sqlalchemy.orm import Session
from repositories.animal_weight_repository import AnimalWeightRepository
from util.commom_util import add_db_object


class AnimalWeightService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.animal_weight_repository = AnimalWeightRepository(session)
        
      
    def get_animal_weight(self, animal_id):
        animal_wgts: List[AnimalWeightMeasurement] = self.animal_weight_repository.fetch_animal_wgt_by_animal_id(animal_id)
        
        fetch_animal_wgts_data: List[Dict] = list()

        for animal_wgt in animal_wgts:
            data = {
                'animal_weight_measurement_id' : animal_wgt.animal_weight_measurement_id,
                'weight' : animal_wgt.weight,
                'animal_id' : animal_wgt.animal_id,
                'measurement_date' : animal_wgt.measurement_date,
                'update_time_stamp' : animal_wgt.update_time_stamp,
                'user_id' : animal_wgt.user_id,
                'tumor_id' : animal_wgt.tumor_id,
                'comments' : animal_wgt.comments,
                'is_exclude' : animal_wgt.is_exclude,
                'created_at' : animal_wgt.created_at,
                'updated_at' : animal_wgt.updated_at,
                'state' : animal_wgt.state,
                'day_num' : animal_wgt.day_num 
            }

            fetch_animal_wgts_data.append(data)
        return fetch_animal_wgts_data
    
    
    def create_animal_weight(self, study_id, request_data):
        animal_objs: Animal = self.animal_weight_repository.fetch_animal_by_study_id(study_id)
        
        matching_animal = next((animal for animal in animal_objs if animal.animal_id == request_data['animal_id']), None)
    
        # if not matching_animal:
        #     raise Exception('Animal Id is not present in the study')
        
        wgt_data: AnimalWeightMeasurement = AnimalWeightMeasurement(animal_weight_measurement_id=str(uuid.uuid4()))
        wgt_data.animal_id = str(request_data['animal_id']),
        wgt_data.weight = request_data['weight']
                
        if not add_db_object(session=self.session, table_name=AnimalWeightMeasurement.__tablename__, data=wgt_data):
            raise Exception('Failed to create Animal weight measurement data')
                
        response = {'status': 'success', 'inserted_id': wgt_data.animal_weight_measurement_id}
        return response 
    
    
    def update_animal_weight(self, request_data):
        animal_wgt_ids = {UUID(animal_wgt['animal_weight_measurement_id']): animal_wgt for animal_wgt in request_data}
        
        animal_ids = {UUID(animal_wgt['animal_id']) for animal_wgt in request_data}

        existing_animal_wgt_ids = self.animal_weight_repository.fetch_existing_animal_wgt_ids(list(animal_wgt_ids.keys()), list(animal_ids))
        
        not_found_animal_wgt_ids = list(set(animal_wgt_ids.keys()) - set(existing_animal_wgt_ids))

        animal_weight_update_data = []

        for animal_wgt_id in existing_animal_wgt_ids:
            animal_wgt_data = {
                'animal_weight_measurement_id': str(animal_wgt_id),
                'animal_id': str(animal_wgt_ids[animal_wgt_id].get('animal_id')),
                'weight': animal_wgt_ids[animal_wgt_id].get('weight')
            }
            animal_weight_update_data.append(animal_wgt_data)

        try:
            if animal_weight_update_data:
                self.animal_weight_repository.update_animal_weight_ids(animal_weight_update_data)
        except Exception as error_:
            self.session.rollback()
            logger.error(f'Something went wrong while updating Animal Weight, Error: {error_}')
            raise Exception('Failed to update Animal Weights')

        update_response_body = {'data': {'updated': [str(id) for id in existing_animal_wgt_ids]}}

        if not_found_animal_wgt_ids:
            update_response_body['data'].update({'missing': [str(id) for id in not_found_animal_wgt_ids]})
            
        return update_response_body
        
        
    def delete_animal_weight(self, request_data):
        animal_weight_measurement_id = UUID(request_data['animal_weight_measurement_id'])
        animal_id = UUID(request_data['animal_id'])
        
        if not self.animal_weight_repository.fetch_existing_animal_wgt_id(animal_weight_measurement_id, animal_id):
            raise Exception("Animal weight measurement ID does not exist")
        
        deletion_successful = self.animal_weight_repository.delete_animal_weight(animal_weight_measurement_id)
        
        if not deletion_successful:
            raise Exception("Failed to delete Animal Weight Measurement.")
        
        response = {'status': 'success', 'deleted_id': str(animal_weight_measurement_id)}
        return response
        
        
        