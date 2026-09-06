@echo off
git clone https://github.com/ultralytics/yolov5.git yolov5
cd yolov5
py -m pip install -r requirements.txt
py train.py --img 768 --batch 4 --epochs 300 --data %DATASET_YAML% --weights yolov5m.pt --optimizer SGD --cos-lr --lr0 0.001 --hyp ../training/hyp-kiwi.yaml --device 0 --project ../runs --name kiwifruit_yolov5m
