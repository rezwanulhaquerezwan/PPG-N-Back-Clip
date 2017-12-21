# -*- coding: utf-8 -*-

import os
import fnmatch
from functools import reduce
from ppg import BASE_DIR
from ppg.params import TRAINING_DATA_RATIO
from ppg.utils import exist, load_json, dump_json, get_change_ratio


def merge(feature_data_1, feature_data_2):
    return {
        '0': feature_data_1['0'] + feature_data_2['0'],
        '1': feature_data_1['1'] + feature_data_2['1'],
        '2': feature_data_1['2'] + feature_data_2['2'],
    }


def subject_independent():
    extracted_data_dir = os.path.join(BASE_DIR, 'data', 'extracted')
    subject_independent_data_dir = os.path.join(BASE_DIR, 'data', 'subject_independent')

    if exist(pathname=extracted_data_dir):
        all_subject_data = {}
        for filename_with_ext in fnmatch.filter(os.listdir(extracted_data_dir), '*.json'):
            subject = os.path.splitext(filename_with_ext)[0]
            feature_data = {
                '0': [],
                '1': [],
                '2': [],
            }
            pathname = os.path.join(extracted_data_dir, filename_with_ext)
            json_data = load_json(pathname=pathname)
            if json_data is not None:
                for session_id in json_data:
                    for block in json_data[session_id]['blocks']:
                        feature_data[str(block['level'])].append({
                            'ppg45': block['ppg']['ppg45'],
                            'ppg45_cr': get_change_ratio(data=block['ppg']['ppg45'], baseline=json_data[session_id]['rest']['ppg']['ppg45']),
                            'svri': block['ppg']['svri'],
                            'svri_cr': get_change_ratio(data=block['ppg']['svri'], baseline=json_data[session_id]['rest']['ppg']['svri']),
                            'average_skin_conductance_level': block['skin_conductance']['average_level'],
                            'average_skin_conductance_level_cr': get_change_ratio(data=block['skin_conductance']['average_level'], baseline=json_data[session_id]['rest']['skin_conductance']['average_level']),
                            'minimum_skin_conductance_level': block['skin_conductance']['minimum_level'],
                            'minimum_skin_conductance_level_cr': get_change_ratio(data=block['skin_conductance']['minimum_level'], baseline=json_data[session_id]['rest']['skin_conductance']['minimum_level']),
                            'average_rri': block['ecg']['average_rri'],
                            'average_rri_cr': get_change_ratio(data=block['ecg']['average_rri'], baseline=json_data[session_id]['rest']['ecg']['average_rri']),
                            'rmssd': block['ecg']['rmssd'],
                            'rmssd_cr': get_change_ratio(data=block['ecg']['rmssd'], baseline=json_data[session_id]['rest']['ecg']['rmssd']),
                            'lf_hrv_power': block['ecg']['lf_hrv_power'],
                            'lf_hrv_power_cr': get_change_ratio(data=block['ecg']['lf_hrv_power'], baseline=json_data[session_id]['rest']['ecg']['lf_hrv_power']),
                            'hf_hrv_power': block['ecg']['hf_hrv_power'],
                            'hf_hrv_power_cr': get_change_ratio(data=block['ecg']['hf_hrv_power'], baseline=json_data[session_id]['rest']['ecg']['hf_hrv_power']),
                        })
                all_subject_data[subject] = feature_data
        for subject in all_subject_data:
            output_data = {
                'train': reduce(lambda feature_data_1, feature_data_2: merge(feature_data_1, feature_data_2), [all_subject_data[participant] for participant in all_subject_data if participant != subject]),
                'test': {
                    '0': all_subject_data[subject]['0'][int(len(all_subject_data[subject]['0']) * TRAINING_DATA_RATIO):],
                    '1': all_subject_data[subject]['1'][int(len(all_subject_data[subject]['1']) * TRAINING_DATA_RATIO):],
                    '2': all_subject_data[subject]['2'][int(len(all_subject_data[subject]['2']) * TRAINING_DATA_RATIO):],
                },
            }
            dump_json(data=output_data, pathname=os.path.join(subject_independent_data_dir, '%s.json' % subject), overwrite=True)


if __name__ == '__main__':
    subject_independent()
