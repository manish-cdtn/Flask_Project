from models import Animal, AnimalVolumeMeasurement
from sqlalchemy.orm import Session


class AnimalVolumeRepository:
    def __init__(self, session: Session) -> None:
        self.session = session
        
    
    def fetch_animal_vol_by_animal_id(self, animal_id):
        return self.session.query(AnimalVolumeMeasurement).filter(AnimalVolumeMeasurement.animal_id == animal_id)
    
    
    def fetch_animal_by_study_id(self, study_id):
        return self.session.query(Animal).filter(Animal.study_id == study_id).all()
        
    
    def fetch_existing_animal_vol_ids(self, animal_vol_ids, animal_ids):
        existing_animal_vols = self.session.query(AnimalVolumeMeasurement.animal_volume_measurement_id).filter(
            AnimalVolumeMeasurement.animal_id.in_(animal_ids),
            AnimalVolumeMeasurement.animal_volume_measurement_id.in_(animal_vol_ids)
        ).all()
        return [vol[0] for vol in existing_animal_vols]
    
    def update_animal_volume_ids(self, animal_volume_update_data):
        self.session.bulk_update_mappings(AnimalVolumeMeasurement, animal_volume_update_data)
        
        
    def fetch_existing_animal_vol_id(self, animal_volume_measurement_id, animal_id):
        return self.session.query(AnimalVolumeMeasurement).filter(
            AnimalVolumeMeasurement.animal_volume_measurement_id == animal_volume_measurement_id,
            AnimalVolumeMeasurement.animal_id == animal_id
        ).first() is not None
    
    def delete_animal_volume(self, animal_volume_measurement_id):
        result = self.session.query(AnimalVolumeMeasurement).filter(
            AnimalVolumeMeasurement.animal_volume_measurement_id == animal_volume_measurement_id
        ).delete()
        
        return result > 0 
        
        
    