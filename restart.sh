./stop.sh
#/start.sh
nohup python3 capturediff.py > log.txt &
ps -ef | grep python
