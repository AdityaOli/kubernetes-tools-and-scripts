EMAIL_LIST=RECEIVEREMAILID
limit=80
HOST=`hostname`
DISK_SPACE=`df -HP | awk '{print $5, $6}' | sed 's/%//' | awk '{if ($1 > 80) print $1, $2}' | grep "/"`
if [[ "$DISK_SPACE" ]]; then
 
 
echo "Disk space is more than 80% for below mount on host $HOST." >> diskspace.txt
echo " " >> diskspace.txt
df -HP | awk '{print $5, $6}' |sed 's/%//' | awk '{if ($1 > 80) print $1=$1"%", $2}' >> diskspace.txt
echo "Please clear ASAP to avoid P2 INC" >> diskspace.txt
 
mail -s "Disk space alert on $HOST" -r "SENDEREMAILID"  $EMAIL_LIST < diskspace.txt
rm diskspace.txt
fi
