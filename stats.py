# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
import numpy as np
from ppg import BASE_DIR
from ppg.utils import exist, load_json, dump_json, export_csv


def stats():
    extracted_data_dir = os.path.join(BASE_DIR, 'data', 'extracted')
    stats_data_dir = os.path.join(BASE_DIR, 'data', 'stats')
    result_dir = os.path.join(BASE_DIR, 'results')
    fieldnames = [
        'name',
        's1_l0_rsme',
        's1_l0_correct_rate',
        's1_l0_svri',
        's1_l0_minimum_skin_conductance_level',
        's1_l0_average_skin_conductance_level',
        's1_l0_average_rri',
        's1_l0_rmssd',
        's1_l0_mf_hrv_power',
        's1_l0_hf_hrv_power',
        's1_l1_rsme',
        's1_l1_correct_rate',
        's1_l1_svri',
        's1_l1_minimum_skin_conductance_level',
        's1_l1_average_skin_conductance_level',
        's1_l1_average_rri',
        's1_l1_rmssd',
        's1_l1_mf_hrv_power',
        's1_l1_hf_hrv_power',
        's1_l2_rsme',
        's1_l2_correct_rate',
        's1_l2_svri',
        's1_l2_minimum_skin_conductance_level',
        's1_l2_average_skin_conductance_level',
        's1_l2_average_rri',
        's1_l2_rmssd',
        's1_l2_mf_hrv_power',
        's1_l2_hf_hrv_power',
        's2_l0_rsme',
        's2_l0_correct_rate',
        's2_l0_svri',
        's2_l0_minimum_skin_conductance_level',
        's2_l0_average_skin_conductance_level',
        's2_l0_average_rri',
        's2_l0_rmssd',
        's2_l0_mf_hrv_power',
        's2_l0_hf_hrv_power',
        's2_l1_rsme',
        's2_l1_correct_rate',
        's2_l1_svri',
        's2_l1_minimum_skin_conductance_level',
        's2_l1_average_skin_conductance_level',
        's2_l1_average_rri',
        's2_l1_rmssd',
        's2_l1_mf_hrv_power',
        's2_l1_hf_hrv_power',
        's2_l2_rsme',
        's2_l2_correct_rate',
        's2_l2_svri',
        's2_l2_minimum_skin_conductance_level',
        's2_l2_average_skin_conductance_level',
        's2_l2_average_rri',
        's2_l2_rmssd',
        's2_l2_mf_hrv_power',
        's2_l2_hf_hrv_power',
    ]

    if exist(pathname=extracted_data_dir):
        csv_data = []
        for filename_with_ext in fnmatch.filter(os.listdir(extracted_data_dir), '*.json'):
            filename, file_ext = os.path.splitext(filename_with_ext)
            output_data = {}
            csv_row = {
                'name': filename,
            }
            pathname = os.path.join(extracted_data_dir, filename_with_ext)
            json_data = load_json(pathname=pathname)
            if json_data is not None:
                for session_id in json_data:
                    if session_id not in output_data:
                        output_data[session_id] = {}
                    for block in json_data[session_id]['blocks']:
                        correct_count = sum([item['correct'] for item in block['stimuli'] if item['correct'] is not None])
                        stimuli_count = len(block['stimuli'])
                        correct_rate = float(correct_count) / float(stimuli_count)
                        svri = np.mean(block['ppg']['svri'])
                        output_data[session_id][block['level']] = {
                            'rsme': block['rsme'],
                            'correct_count': correct_count,
                            'stimuli_count': stimuli_count,
                            'correct_rate': correct_rate,
                            'svri': svri,
                            'minimum_skin_conductance_level': block['skin_conductance']['minimum_level'],
                            'average_skin_conductance_level': block['skin_conductance']['average_level'],
                            'average_rri': block['ecg']['average_rri'],
                            'rmssd': block['ecg']['rmssd'],
                            'mf_hrv_power': block['ecg']['mf_hrv_power'],
                            'hf_hrv_power': block['ecg']['hf_hrv_power'],
                        }
                        csv_row['s%s_l%s_rsme' % (session_id, block['level'])] = block['rsme']
                        csv_row['s%s_l%s_correct_rate' % (session_id, block['level'])] = correct_rate
                        csv_row['s%s_l%s_svri' % (session_id, block['level'])] = svri
                        csv_row['s%s_l%s_minimum_skin_conductance_level' % (session_id, block['level'])] = block['skin_conductance']['minimum_level']
                        csv_row['s%s_l%s_average_skin_conductance_level' % (session_id, block['level'])] = block['skin_conductance']['average_level']
                        csv_row['s%s_l%s_average_rri' % (session_id, block['level'])] = block['ecg']['average_rri']
                        csv_row['s%s_l%s_rmssd' % (session_id, block['level'])] = block['ecg']['rmssd']
                        csv_row['s%s_l%s_mf_hrv_power' % (session_id, block['level'])] = block['ecg']['mf_hrv_power']
                        csv_row['s%s_l%s_hf_hrv_power' % (session_id, block['level'])] = block['ecg']['hf_hrv_power']
                dump_json(data=output_data, pathname=os.path.join(stats_data_dir, filename_with_ext), overwrite=True)
                csv_data.append(csv_row)
        export_csv(data=csv_data, fieldnames=fieldnames, pathname=os.path.join(result_dir, 'stats.csv'), overwrite=True)

if __name__ == '__main__':
    stats()