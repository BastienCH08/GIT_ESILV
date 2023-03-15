curl -s https://live.euronext.com/fr/markets/paris > /home/ubuntu/GIT_ESILV/Projet/temp.txt
lastPrice=$(cat /home/ubuntu/GIT_ESILV/Projet/temp.txt | grep -A 3 "EUR / USD" | tail -n 1)
lastDate=$(date +"%Y/%m/%d %H:%M")
echo $lastDate";"$lastPrice >> /home/ubuntu/GIT_ESILV/Projet/out.csv
