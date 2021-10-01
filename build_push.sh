set -e

directory="$1"
if [[ $directory == "frontend" ]]; then
    image_repo="621544995223.dkr.ecr.us-west-2.amazonaws.com/budget-tracker-ecr"
elif [[ $directory == "backend" ]]; then
    image_repo="621544995223.dkr.ecr.us-west-2.amazonaws.com/budget-tracker-ecr-backend"
else
    printf "The directory argument must be provided. E.g. frontend or backend \n"
    exit 1
fi
old_image_version=$(cat $directory/version.txt)
new_image_tag=$(python build_new_image_tag.py $directory $image_repo)
printf "new_image_tag: $new_image_tag \n"
cd $directory
docker build -f Dockerfile -t $new_image_tag .
cd ..
printf "Pushing $new_image_tag... \n"
docker push $new_image_tag