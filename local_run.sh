set -e

function main {
    if [[ $directory == "frontend" ]]; then
        image_repo="621544995223.dkr.ecr.us-west-2.amazonaws.com/budget-tracker-ecr"
        ports="8080:80"
    elif [[ $directory == "backend" ]]; then
        image_repo="621544995223.dkr.ecr.us-west-2.amazonaws.com/budget-tracker-ecr-backend"
        ports="5000:5000"
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
    printf "stopping all running containers with ancestor image $image_repo:$old_image_version \n"
    docker stop $(docker ps -q --filter ancestor=$image_repo:$old_image_version ) > /dev/null || true
    printf "Spinning up a new container from image: $new_image_tag \n"
    container_id=$(docker run -it --rm -d -p $ports $new_image_tag)
    printf "The new container's ID is: $container_id \n"
}

directory="$1"
main $directory