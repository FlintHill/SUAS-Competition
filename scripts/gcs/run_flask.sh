cd ../../
bash ./install.sh
cd scripts/gcs
export FLASK_APP=flask_gcs.py
python -m flask run
