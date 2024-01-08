# Takes all parquet files in the current directory and copies them
# with new names.
for file in *.parquet; do
    # Extract the part before the number
    prefix=$(echo $file | awk -F'[0-9]' '{print $1}')

    # Generate a new random number
    new_number=$((RANDOM + 1))

    # Form the new filename
    new_file="${prefix}${new_number}.parquet"
    echo "-------"
    echo "$file"
    echo "$new_file"

    # Copy the file
    cp "$file" "$new_file"
done
