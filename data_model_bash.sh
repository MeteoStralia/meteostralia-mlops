
source ./env/Scripts/activate
python ./src/data_service/ingest_data/reset_data.py
python ./src/data_service/ingest_data/ingest_new_data.py
python ./src/data_service/complete_nas/complete_nas.py
python ./src/data_service/features/add_features.py
python ./src/data_service/encode_data/encode_data.py
python3 ./src/data_service/split_data/split_data.py
python3 ./src/data_service/scale_data/scale_data.py
python3 ./src/modeling_service/training/train.py
python3 ./src/modeling_service/evaluate/evaluate.py