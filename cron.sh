#!/bin/bash

# リクエストして、抽出して、ファイル書き換えて、プッシュ
# curl *** | grep *** > file
# git ***



### git系1
cd ~/Desktop/cinosion/oneStop/publish
ssh -T git@github.com -i ~/.ssh/id_ed25519_cino
git pull origin master

### リクエスト送ってそのまま書き込む
# https://www.chuo-u.ac.jp/news/2020/04/48178/
# https://www.chuo-u.ac.jp/news/feed/
# https://www.chuo-u.ac.jp/campuslife/news/feed/
# https://www.chuo-u.ac.jp/academics/faculties/letters/news/feed/
# http://sil.tamacc.chuo-u.ac.jp/wp/
# https://www.chuo-u.ac.jp/news/2020/04/48178/

curl -s https://www.chuo-u.ac.jp/news/feed/ -o top.xml
curl -s https://www.chuo-u.ac.jp/campuslife/news/feed/ -o clife.xml
curl -s https://www.chuo-u.ac.jp/academics/faculties/letters/news/feed/ -o bun.xml
curl -s https://www.chuo-u.ac.jp/academics/faculties/letters/major/socio_info/news/feed/ -o socinfo.xml

curl -s http://sil.tamacc.chuo-u.ac.jp/wp/ -o infocial.html
curl -s https://www.chuo-u.ac.jp/news/2020/04/48178/ -o corona.html


python3 sub.py
python3 main.py



### git系2
git add bridge.js
git commit -m "update: from cron" --no-edit
ssh -T git@github.com -i ~/.ssh/id_ed25519_cino
git push origin master























