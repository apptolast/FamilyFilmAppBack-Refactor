from sqlalchemy.dialects.postgresql import ENUM

role_enum = ENUM('USER', 'ADMIN', name='role', create_enum=True)