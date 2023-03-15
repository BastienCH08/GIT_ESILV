curl -s https://live.euronext.com/fr/markets/paris > /home/ubuntu/Projet/temp.txt
lastPrice=$(cat /home/ubuntu/Projet/temp.txt | grep -A 3 "EUR / USD" | tail -n 1)
lastDate=$(date +"%Y/%m/%d %H:%M")
echo $lastDate";"$lastPrice >> /home/ubuntu/Projet/out.csv
