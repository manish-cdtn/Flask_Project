from typing import Dict, List
from uuid import UUID
import uuid
from venv import logger
from models import Animal, AnimalVolumeMeasurement
from sqlalchemy.orm import Session
from repositories.animal_volume_repository import AnimalVolumeRepository
from util.commom_util import add_db_object


class AnimalVolumeService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.animal_volume_repository = AnimalVolumeRepository(session)
        
      
    def get_animal_volume(self, animal_id):
        animal_vols: List[AnimalVolumeMeasurement] = self.animal_volume_repository.fetch_animal_vol_by_animal_id(animal_id)
        
        fetch_animal_vols_data: List[Dict] = list()

        for animal_vol in animal_vols:
            data = {
                'animal_volume_measurement_id' : animal_vol.animal_volume_measurement_id,
                'volume' : animal_vol.volume,
                'length' : animal_vol.l,
                'width' : animal_vol.w,
                'height' : animal_vol.h,
                'animal_id' : animal_vol.animal_id,
                'measurement_date' : animal_vol.measurement_date,
                'update_time_stamp' : animal_vol.update_time_stamp,
                'user_id' : animal_vol.user_id,
                'tumor_id' : animal_vol.tumor_id,
                'comments' : animal_vol.comments,
                'is_exclude' : animal_vol.is_exclude,
                'created_at' : animal_vol.created_at,
                'updated_at' : animal_vol.updated_at,
                'state' : animal_vol.state,
                'day_num' : animal_vol.day_num,
                'device_id' : animal_vol.device_id   
            }

            fetch_animal_vols_data.append(data)
        return fetch_animal_vols_data
    
    
    def create_animal_volume(self, study_id, request_data):
        animal_objs: Animal = self.animal_volume_repository.fetch_animal_by_study_id(study_id)
        
        matching_animal = next((animal for animal in animal_objs if animal.animal_id == request_data['animal_id']), None)
    
        # if not matching_animal:
        #     raise Exception('Animal Id is not present in the study')
        
        vol_data: AnimalVolumeMeasurement = AnimalVolumeMeasurement(animal_volume_measurement_id=str(uuid.uuid4()))
        vol_data.animal_id = str(request_data['animal_id']),
        vol_data.volume = request_data['volume'],
        vol_data.h = request_data['height'],
        vol_data.l = request_data['length'],
        vol_data.w = request_data['width']
                
        if not add_db_object(session=self.session, table_name=AnimalVolumeMeasurement.__tablename__, data=vol_data):
            raise Exception('Failed to create Animal volume measurement data')
                
        response = {'status': 'success', 'inserted_id': vol_data.animal_volume_measurement_id}
        return response 
    
    
    def update_animal_volume(self, request_data):
        animal_vol_ids = {UUID(animal_vol['animal_volume_measurement_id']): animal_vol for animal_vol in request_data}
        
        animal_ids = {UUID(animal_vol['animal_id']) for animal_vol in request_data}

        existing_animal_vol_ids = self.animal_volume_repository.fetch_existing_animal_vol_ids(list(animal_vol_ids.keys()), list(animal_ids))
        
        not_found_animal_vol_ids = list(set(animal_vol_ids.keys()) - set(existing_animal_vol_ids))

        animal_volume_update_data = []

        for animal_vol_id in existing_animal_vol_ids:
            animal_vol_data = {
                'animal_volume_measurement_id': str(animal_vol_id),
                'animal_id': str(animal_vol_ids[animal_vol_id].get('animal_id')),
                'volume': animal_vol_ids[animal_vol_id].get('volume'),
                'w': animal_vol_ids[animal_vol_id].get('width'),
                'h': animal_vol_ids[animal_vol_id].get('height'),
                'l': animal_vol_ids[animal_vol_id].get('length')
            }
            animal_volume_update_data.append(animal_vol_data)

        try:
            if animal_volume_update_data:
                self.animal_volume_repository.update_animal_volume_ids(animal_volume_update_data)
        except Exception as error_:
            self.session.rollback()
            logger.error(f'Something went wrong while updating Animal Volume, Error: {error_}')
            raise Exception('Failed to update Animal Volumes')

        update_response_body = {'data': {'updated': [str(id) for id in existing_animal_vol_ids]}}

        if not_found_animal_vol_ids:
            update_response_body['data'].update({'missing': [str(id) for id in not_found_animal_vol_ids]})
            
        return update_response_body
        
        
    def delete_animal_volume(self, request_data):
        animal_volume_measurement_id = UUID(request_data['animal_volume_measurement_id'])
        animal_id = UUID(request_data['animal_id'])
        
        if not self.animal_volume_repository.fetch_existing_animal_vol_id(animal_volume_measurement_id, animal_id):
            raise Exception("Animal volume measurement ID does not exist")
        
        deletion_successful = self.animal_volume_repository.delete_animal_volume(animal_volume_measurement_id)
        
        if not deletion_successful:
            raise Exception("Failed to delete Animal Volume Measurement.")
        
        response = {'status': 'success', 'deleted_id': str(animal_volume_measurement_id)}
        return response
        
        
        