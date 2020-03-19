import datajoint as dj

# The remainder is not version dependent and should remain intact

_default_database_prefix = 'group_shared_'

if 'custom' not in dj.config:
    dj.config['custom'] = {}

if 'project.db.prefix' not in dj.config['custom']:
    raise KeyError('Please specify "project.db.prefix" under dj.config["custom"]')

project_database_prefix = dj.config['custom']['project.db.prefix']
