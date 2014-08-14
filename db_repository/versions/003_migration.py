from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
cupping = Table('cupping', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('datetime', DateTime),
    Column('aroma_notes', Text),
    Column('acidity_notes', Text),
    Column('flavour_notes', Text),
    Column('mouthfeel_notes', Text),
    Column('aftertaste_notes', Text),
    Column('overall_notes', Text),
    Column('extra_notes', Text),
    Column('roast_id', Integer),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['cupping'].columns['user_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['cupping'].columns['user_id'].drop()
