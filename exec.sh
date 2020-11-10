#!/bin/bash
source /home/admin/.bashrc
cd /home/admin/menchin_trainer
rm answer.txt
rm latest.txt

python3 ./menchin_trainer.py

sleep 10
/home/admin/.local/bin/toot post -m question.jpg -v unlisted "7枚メンチン(2面子1雀頭)クイズ! : 何待ち?ノーテン?" > latest.txt

sleep 10
/home/admin/.local/bin/toot post -v unlisted -r `cat latest.txt | grep https | cut -d'/' -f 5` -p "正解は..." -m ripi.jpg `cat answer.txt`
