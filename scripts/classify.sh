#!/bin/sh

echo '$ venv/bin/python select_feature.py'
venv/bin/python select_feature.py
echo '--'

echo '$ venv/bin/python classify.py'
venv/bin/python classify.py
echo '--'

echo 'All done!'