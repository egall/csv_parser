csv_dir="/home/egall/scratch/scritch/scratch/csvs/"
for filename in "$csv_dir"/*
do
    echo "$filename"
    dos2unix $filename
    sed -i.bak '/^.*[,]*,,,,,,,,$/d' $filename 
    sed -i.bak 's/^,//' $filename 
    sed -i.bak 's/^gal\/A,//' $filename 
    rm "$csv_dir"/*bak
done
