while read -r line
do
  newline="[$(date +%s%3N)] $line"
  echo $newline >> log
done