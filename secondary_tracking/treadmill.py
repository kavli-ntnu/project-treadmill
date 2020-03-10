import numpy as np
import datajoint as dj

from secondary_tracking import project_database_prefix
from ephys.utilities import ingestion, time_sync
from ephys import get_schema_name


schema = dj.schema(project_database_prefix + 'secondary_tracking')

reference = dj.create_virtual_module('reference', get_schema_name('reference'))
acquisition = dj.create_virtual_module('acquisition', get_schema_name('acquisition'))
behavior = dj.create_virtual_module('behavior', get_schema_name('behavior'))


@schema
class TreadmillTracking(dj.Imported):
    definition = """  # session-level tracking data from the treadmill(s) employed in the experiment
    -> acquisition.Session
    treadmill_tracking_time:          datetime        # start time of this treadmill speed recording
    ---
    treadmill_tracking_name:  varchar(40)         # user-assign name of this treadmill tracking (e.g. 27032019laserSess1)
    treadmill_timestamps:    blob@ephys_store    # (s) timestamps of the treadmill speed samples
    """

    class TreadmillSync(dj.Part):
        definition = """
        -> master
        ---
        sync_master_clock:                  varchar(128)        # name of the sync-master 
        track_sync_data=null:               blob@ephys_store    # sync data (binary)
        track_time_zero=null:               float               # (s) the first time point of this tracking
        track_sync_timestamps=null:         blob@ephys_store    # (s) timestamps of sync data in tracking clock
        track_sync_master_timestamps=null:  blob@ephys_store    # (s) timestamps of sync data in master clock
        """

    class Speed(dj.Part):
        definition = """
        -> master
        treadmill_name: varchar(32)
        ---
        treadmill_speed: blob@ephys_store    # (s) treadmill speed at each timestamp
        """

    key_source = acquisition.Session & acquisition.Recording  # wait for recording to be ingested first before tracking

    def make(self, key):
        input_dir = ingestion.find_input_directory(key)
        if not input_dir:
            print(f'{input_dir} not found in this machine, skipping...')
            return

        rec_type, recordings = ingestion.get_recordings(input_dir)

        if rec_type in ('neuropixels', 'neurologger'):  # if 'neuropixels' recording, check for OptiTrack's `motive` or `.csv`
            opti_list = ingestion.get_optitrack(input_dir)
            if not opti_list:
                raise FileNotFoundError('No OptiTrack "matmot.mtv" or  ".csv" found')

            for opti in opti_list:
                if 'Format Version' not in opti.meta:
                    raise NotImplementedError('Treadmill data ingest from type other than "optitrack.csv" not implemented')

                secondary_data = opti.secondary_data
                if 'Treadmill' not in secondary_data:
                    raise KeyError('No "Treadmill" found in the secondary data of optitrack.csv')

                treadmill_key = dict(key, treadmill_tracking_time=opti.recording_time)
                self.insert1(dict(treadmill_key,
                                  treadmill_tracking_name=opti.tracking_name,  # name of the session folder
                                  treadmill_timestamps=secondary_data['t']))

                if hasattr(opti, 'sync_data'):
                    self.TreadmillSync.insert1(dict(treadmill_key,
                                                    sync_master_clock=opti.sync_data['master_name'],
                                                    track_time_zero=secondary_data['t'][0],
                                                    track_sync_timestamps=opti.sync_data['slave'],
                                                    track_sync_master_timestamps=opti.sync_data['master']))
                else:  # data presynced with tracking-recording pair,
                       # still need for a linear shift from session start to the recording this tracking is synced to
                    self.TrackingSync.insert1(time_sync.create_tracking_sync_data(
                        treadmill_key, np.array([secondary_data['t'][0], secondary_data['t'][-1]])))

                self.Speed.insert1([dict(treadmill_key, treadmill_name=k, treadmill_speed=v['speed'])
                                    for k, v in secondary_data['Treadmill'].items()])

            print(f'Insert {len(opti_list)} treadmill tracking(s): {input_dir.stem}')

        else:
            raise NotImplementedError(f'Treadmill Tracking ingestion for recording type {rec_type} not implemented')
