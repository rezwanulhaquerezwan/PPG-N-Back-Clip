# -*- coding: utf-8 -*-

import os
import fnmatch
from ppg import BASE_DIR
from ppg.utils import exist, load_json, dump_json, load_model, dump_model, export_csv
from ppg.learn import get_merged_feature_set
from ppg.learn import feature_selection_classifier


def select_feature():
    merged_data_dir = os.path.join(BASE_DIR, 'data', 'merged')
    model_dir = os.path.join(BASE_DIR, 'models', 'feature_selection')
    result_dir = os.path.join(BASE_DIR, 'results', 'feature_selection')


    level_sets = [
        ['0', '2'],
        ['0', '1'],
        ['1', '2'],
    ]
    feature_type_sets = [
        ['ppg45_cr'],
    ]


    if exist(pathname=merged_data_dir):
        result_data = {}
        for filename_with_ext in fnmatch.filter(os.listdir(merged_data_dir), '*.json'):
            participant = os.path.splitext(filename_with_ext)[0]
            pathname = os.path.join(merged_data_dir, filename_with_ext)
            json_data = load_json(pathname=pathname)
            if json_data is not None:
                for level_set in level_sets:
                    level_set_name = '-'.join(level_set)
                    if level_set_name not in result_data:
                        result_data[level_set_name] = {}
                    for feature_type_set in feature_type_sets:
                        feature_type_set_name = '-'.join(feature_type_set)
                        if feature_type_set_name not in result_data[level_set_name]:
                            result_data[level_set_name][feature_type_set_name] = {
                                'grid_scores': {},
                            }
                        features, labels = get_merged_feature_set(data=json_data, level_set=level_set, feature_type_set=feature_type_set)
                        model_pathname = os.path.join(model_dir, level_set_name, feature_type_set_name, '%s.model' % participant)
                        classifier = load_model(pathname=model_pathname)
                        if classifier is None:
                            classifier = feature_selection_classifier(features=features, labels=labels)
                            dump_model(model=classifier, pathname=model_pathname)
                        print(participant, level_set_name, feature_type_set_name)
                        result_data[level_set_name][feature_type_set_name]['grid_scores'][participant] = classifier.grid_scores_.tolist()

        for level_set_name in result_data:
            dump_json(data=result_data[level_set_name], pathname=os.path.join(result_dir, '%s.json' % level_set_name), overwrite=True)
            for feature_type_set in feature_type_sets:
                feature_type_set_name = '-'.join(feature_type_set)
                csv_data = []
                all_grid_scores = []
                for participant in result_data[level_set_name][feature_type_set_name]['grid_scores']:
                    csv_row = {
                        'participant': participant,
                    }
                    grid_scores = result_data[level_set_name][feature_type_set_name]['grid_scores'][participant]
                    all_grid_scores.append(grid_scores)
                    for score_index, score in list(enumerate(grid_scores)):
                        csv_row[str(score_index + 1)] = score
                    csv_data.append(csv_row)
                csv_row = {
                    'participant': 'average',
                }
                for scores_index, scores in list(enumerate([list(x) for x in zip(*[grid_scores for grid_scores in all_grid_scores])])):
                    csv_row[str(scores_index + 1)] = sum(scores) / len(scores)
                csv_data.append(csv_row)
                fieldnames = ['participant'] + [str(x) for x in list(range(1, len(result_data[level_set_name][feature_type_set_name]['grid_scores'][participant]) + 1))]
                export_csv(data=csv_data, fieldnames=fieldnames, pathname=os.path.join(result_dir, feature_type_set_name, '%s-grid_scores.csv' % level_set_name), overwrite=True)


if __name__ == '__main__':
    select_feature()
