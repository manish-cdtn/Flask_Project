from sqlalchemy import (JSON, Boolean, Column, Date, DateTime, Enum, Float,
                        ForeignKey, Integer, SmallInteger, String, Text,
                        UniqueConstraint, text)
from sqlalchemy.dialects.postgresql import INET, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class Organization(Base):
    __tablename__ = 'organizations'
    __table_args__ = (UniqueConstraint('id', 'name', 'cognito_group_name'),)

    id = Column(Integer, nullable=False, server_default=text("nextval('organizations_id_seq'::regclass)"))
    organization_id = Column(UUID, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    cognito_group_name = Column(String(50), nullable=False, unique=True)
    description = Column(String(100))
    primary_mobile_number = Column(String(15), nullable=False, server_default=text("'N\A'::character varying"))
    secondry_mobile_number = Column(String(15), server_default=text('NULL::character varying'))
    address = Column(String(255), nullable=False, server_default=text("'N\A'::character varying"))
    website = Column(Text, nullable=False, server_default=text("'N\A'::text"))
    poc_email_address = Column(String(50), nullable=False, server_default=text("'N\A'::character varying"))
    is_enabled = Column(Boolean, server_default=text('false'))
    is_deleted = Column(Boolean, server_default=text('false'))
    logo_url = Column(Text)
    created_at = Column(DateTime, server_default=text("timezone('UTC'::text, CURRENT_TIMESTAMP)"))
    updated_at = Column(DateTime, server_default=text("timezone('UTC'::text, CURRENT_TIMESTAMP)"))
    is_key_created = Column(Boolean, nullable=False, server_default=text('false'))
    org_domain = Column(String)
    is_mfa_required = Column(Boolean, nullable=False, server_default=text('false'))


class Study(Base):
    __tablename__ = 'study'

    id = Column(Integer, nullable=False, server_default=text("nextval('study_id_seq'::regclass)"))
    study_id = Column(UUID, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    sponsor_id = Column(Text)
    protocol_id = Column(Text)
    experiment_no = Column(Text)
    passage_number = Column(Integer)
    group_comment = Column(Text)
    tumor_initial_size = Column(Float(53))
    tumor_target_size = Column(Float(53))
    story_duration = Column(Integer)
    number_of_groups = Column(Integer)
    default_gender = Column(Enum('female', 'male', name='gender_enum'))
    tl_species_id = Column(ForeignKey('term_list_species.tl_species_id'))
    tl_animal_supplier_id = Column(ForeignKey('term_list_animal_supplier.tl_animal_supplier_id'))
    date_of_arrival = Column(DateTime)
    average_weight = Column(Float(53))
    average_age = Column(Float(53))
    tl_atm_atp_id = Column(ForeignKey('term_list_animal_test_method.tl_animal_test_method_id'))
    log_book_number = Column(Text)
    order_number = Column(Text)
    log_book_page = Column(Text)
    grouping_date = Column(DateTime)
    tl_tumor_histology_id = Column(ForeignKey('term_list_tumor_histology.tl_tumor_histology_id'))
    protocol_step = Column(Integer)
    start_date_is = Column(
        Enum('Group_Assignment_Date', 'Inoculation_Date', 'Dosing_Start_Date', name='study_start_date_is_enum'),
        server_default=text("'Inoculation_Date'::study_start_date_is_enum"))
    study_start_date = Column(DateTime)
    study_end_date = Column(DateTime)
    is_signed_off = Column(Boolean)
    signed_off_date = Column(DateTime)
    inoculation_date = Column(DateTime)
    is_active = Column(Boolean)
    number_of_animals = Column(Integer)
    max_number_of_animals = Column(Integer)
    settings_id = Column(ForeignKey('settings.settings_id'))
    randomization_anova_id = Column(ForeignKey('randomization_anovas.randomization_anova_id'))
    tl_study_type_id = Column(ForeignKey('term_list_study_type.tl_study_type_id'))
    using_group_labels = Column(Boolean)
    pre_study_suffix = Column(Text)
    pre_study_preffix = Column(Text)
    cage_prefix = Column(String)
    cage_suffix = Column(String)
    cage_start_number = Column(Integer)
    custom_data_label = Column(Text)
    is_q_method = Column(Boolean)
    is_deleted = Column(Boolean, server_default=text('false'))
    organization_id = Column(ForeignKey('organizations.organization_id'), nullable=False)
    created_at = Column(DateTime, server_default=text("timezone('UTC'::text, CURRENT_TIMESTAMP)"))
    updated_at = Column(DateTime, server_default=text("timezone('UTC'::text, CURRENT_TIMESTAMP)"))
    status = Column(
        Enum('PRE_STUDY', 'IN_PROGRESS', 'COMPLETED', 'SIGNED_OFF', 'PRE_STUDY_MEASUREMENTS', 'PRE_STUDY_PLANNING', name='study_status_enum'),
        nullable=False, server_default=text("'PRE_STUDY'::study_status_enum"))
    toxicity_day = Column(Integer)
    start_num = Column(Integer)
    end_num = Column(Integer)
    animal_pre_study_id_as_study_id = Column(Boolean, server_default=text('false'))
    is_sequential_animal_id = Column(Boolean, server_default=text('false'))
    grouping_type = Column(String)
    runs_test_type = Column(String)
    tl_study_category_id = Column(ForeignKey('term_list_study_category.tl_study_category_id'))
    study_director_id = Column(ForeignKey('users.user_id'))
    study_measurement_type = Column(Enum('TumorImager', 'Caliper', name='study_measurement_type_enum'))
    selected_m_dt = Column(DateTime)
    grouping_m_dt = Column(DateTime)
    dosing_date = Column(DateTime)
    is_migrated = Column(Boolean, server_default=text('false'))

    organization = relationship('Organization')
    # randomization_anova = relationship('RandomizationAnova')
    # settings = relationship('Setting')
    # study_director_r = relationship('User')
    # tl_animal_supplier = relationship('TermListAnimalSupplier')
    # tl_atm_atp = relationship('TermListAnimalTestMethod')
    # tl_species = relationship('TermListSpecies')
    # tl_study_category = relationship('TermListStudyCategory')
    # tl_study_type = relationship('TermListStudyType')
    # tl_tumor_histology = relationship('TermListTumorHistology')


class Animal(Base):
    __tablename__ = 'animals'
    __table_args__ = (UniqueConstraint('study_id', 'pre_study_animal_id'), UniqueConstraint('study_id', 'study_animal_id'))

    id = Column(Integer, nullable=False, server_default=text("nextval('animals_id_seq'::regclass)"))
    animal_id = Column(UUID, primary_key=True)
    study_id = Column(ForeignKey('study.study_id'), nullable=False)
    group_id = Column(ForeignKey('groups.group_id'))
    study_status = Column(Integer)
    gender = Column(Enum('female', 'male', name='gender_enum'))
    update_time_stamp = Column(DateTime)
    study_animal_id = Column(Text)
    pre_study_animal_id = Column(Text)
    chip_id = Column(Text)
    custom_data_value = Column(Text)
    is_terminated = Column(Boolean)
    cage_id = Column(Text)
    pre_study_cage_id = Column(Text)
    animal_status = Column(Integer)
    animal_start_date = Column(DateTime)
    is_dead = Column(Boolean)
    comments = Column(Text)
    grouping_volume = Column(Float(53))
    grouping_weight = Column(Float(53))
    grouping_is_include = Column(Boolean)
    is_custom_data_selected = Column(Boolean, server_default=text('false'))
    created_at = Column(DateTime, server_default=text("timezone('UTC'::text, CURRENT_TIMESTAMP)"))
    updated_at = Column(DateTime, server_default=text("timezone('UTC'::text, CURRENT_TIMESTAMP)"))

    # group = relationship('Group')
    study = relationship('Study')
    
    
class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, nullable=False, server_default=text("nextval('devices_id_seq'::regclass)"))
    device_id = Column(UUID, primary_key=True)
    device_type = Column(Text)
    device_name = Column(Text)
    com_port = Column(Integer)
    baud_rate = Column(Integer)
    parity = Column(Text)
    hand_shake = Column(Boolean)
    data_bits = Column(Integer)
    stop_bits = Column(Integer)
    read_string = Column(Text)
    write_string = Column(Text)
    start_string = Column(Text)
    auto_string = Column(Text)
    calibration_date = Column(DateTime)
    reread_string = Column(Text)
    input_length = Column(Integer)
    r_threshold = Column(Integer)
    input_mode = Column(Integer)
    created_at = Column(DateTime, server_default=text("timezone('UTC'::text, CURRENT_TIMESTAMP)"))
    updated_at = Column(DateTime, server_default=text("timezone('UTC'::text, CURRENT_TIMESTAMP)"))
    device_type_id = Column(Text, nullable=False)
    
    
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, server_default=text("nextval('users_id_seq'::regclass)"))
    user_id = Column(UUID, primary_key=True)
    user_cognito_id = Column(UUID, nullable=False, unique=True)
    organization_id = Column(ForeignKey('organizations.organization_id'), nullable=False)
    email = Column(Text, nullable=False, unique=True)
    is_enabled = Column(Boolean, server_default=text('false'))
    status = Column(
        Enum('active', 'pending', 'deleted', name='users_status_enum'), nullable=False, server_default=text("'pending'::users_status_enum"))
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30))
    profile_img_url = Column(Text)
    role = Column(Enum('admin', 'user', name='users_role_enum'), nullable=False, server_default=text("'user'::users_role_enum"))
    created_at = Column(DateTime, server_default=text("timezone('UTC'::text, CURRENT_TIMESTAMP)"))
    updated_at = Column(DateTime, server_default=text("timezone('UTC'::text, CURRENT_TIMESTAMP)"))
    organization_role = Column(Enum('super_admin', 'admin', 'user', 'reviewer', name='users_organization_role_enum'))
    is_org_admin = Column(Boolean, nullable=False, server_default=text('false'))
    is_mfa_enabled = Column(Boolean, nullable=False, server_default=text('false'))
    first_login_at = Column(DateTime)

    organization = relationship('Organization')



class AnimalVolumeMeasurement(Base):
    __tablename__ = 'animal_volume_measurements'

    id = Column(Integer, nullable=False, server_default=text("nextval('animal_volume_measurements_id_seq'::regclass)"))
    animal_volume_measurement_id = Column(UUID, primary_key=True)
    volume = Column(Float(53))
    l = Column(Float(53))
    w = Column(Float(53))
    h = Column(Float(53))
    animal_id = Column(ForeignKey('animals.animal_id'), index=True)
    measurement_date = Column(DateTime)
    update_time_stamp = Column(DateTime)
    user_id = Column(ForeignKey('users.user_id'))
    tumor_id = Column(Integer)
    comments = Column(Text)
    is_exclude = Column(Integer)
    created_at = Column(DateTime, server_default=text("timezone('UTC'::text, CURRENT_TIMESTAMP)"))
    updated_at = Column(DateTime, server_default=text("timezone('UTC'::text, CURRENT_TIMESTAMP)"))
    state = Column(Enum('PRE_STUDY', 'STUDY', name='measurements_state_enum'), server_default=text("'PRE_STUDY'::measurements_state_enum"))
    day_num = Column(Integer)
    device_id = Column(ForeignKey('devices.device_id'))

    animal = relationship('Animal')
    device = relationship('Device')
    user = relationship('User')


class AnimalWeightMeasurement(Base):
    __tablename__ = 'animal_weight_measurements'

    id = Column(Integer, nullable=False, server_default=text("nextval('animal_weight_measurements_id_seq'::regclass)"))
    animal_weight_measurement_id = Column(UUID, primary_key=True)
    weight = Column(Float(53))
    animal_id = Column(ForeignKey('animals.animal_id'))
    measurement_date = Column(DateTime)
    update_time_stamp = Column(DateTime)
    user_id = Column(ForeignKey('users.user_id'))
    device_id = Column(Integer)
    tumor_id = Column(Integer)
    comments = Column(Text)
    is_exclude = Column(Integer)
    created_at = Column(DateTime, server_default=text("timezone('UTC'::text, CURRENT_TIMESTAMP)"))
    updated_at = Column(DateTime, server_default=text("timezone('UTC'::text, CURRENT_TIMESTAMP)"))
    state = Column(Enum('PRE_STUDY', 'STUDY', name='measurements_state_enum'), server_default=text("'PRE_STUDY'::measurements_state_enum"))
    day_num = Column(Integer)

    animal = relationship('Animal')
    user = relationship('User')
    
    
    