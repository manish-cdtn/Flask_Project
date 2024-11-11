from models import Animal, AnimalWeightMeasurement
from sqlalchemy.orm import Session


class AnimalWeightRepository:
    def __init__(self, session: Session) -> None:
        self.session = session
        
    
    def fetch_animal_wgt_by_animal_id(self, animal_id):
        return self.session.query(AnimalWeightMeasurement).filter(AnimalWeightMeasurement.animal_id == animal_id)
    
    
    def fetch_animal_by_study_id(self, study_id):
        return self.session.query(Animal).filter(Animal.study_id == study_id).all()
        
    
    def fetch_existing_animal_wgt_ids(self, animal_wgt_ids, animal_ids):
        existing_animal_wgts = self.session.query(AnimalWeightMeasurement.animal_weight_measurement_id).filter(
            AnimalWeightMeasurement.animal_id.in_(animal_ids),
            AnimalWeightMeasurement.animal_weight_measurement_id.in_(animal_wgt_ids)
        ).all()
        return [wgt[0] for wgt in existing_animal_wgts]
    
    def update_animal_weight_ids(self, animal_weight_update_data):
        self.session.bulk_update_mappings(AnimalWeightMeasurement, animal_weight_update_data)
        
        
    def fetch_existing_animal_wgt_id(self, animal_weight_measurement_id, animal_id):
        return self.session.query(AnimalWeightMeasurement).filter(
            AnimalWeightMeasurement.animal_weight_measurement_id == animal_weight_measurement_id,
            AnimalWeightMeasurement.animal_id == animal_id
        ).first() is not None
    
    def delete_animal_weight(self, animal_weight_measurement_id):
        result = self.session.query(AnimalWeightMeasurement).filter(
            AnimalWeightMeasurement.animal_weight_measurement_id == animal_weight_measurement_id
        ).delete()
        
        return result > 0 
        
        
    