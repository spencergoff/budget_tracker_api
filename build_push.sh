set -e

image_repo="621544995223.dkr.ecr.us-west-2.amazonaws.com/budget-tracker-ecr-backend"
old_image_version=$(cat version.txt)
new_image_tag=$(python build_new_image_tag.py $image_repo)
printf "new_image_tag: $new_image_tag \n"
docker build -f Dockerfile -t $new_image_tag .
printf "Pushing $new_image_tag... \n"
docker push $new_image_tag