import sys

def main():
    required_args = ['directory', 'image_repo']
    if len(sys.argv[1:]) < len(required_args):
        raise Exception(f'ERROR The following arguments are required: {required_args}')
    directory = sys.argv[1]
    image_repo = sys.argv[2]
    version_file_path = f'{directory}/version.txt'
    current_version = get_current_version(version_file_path)
    new_version = int(current_version) + 1
    update_version_file(version_file_path, new_version)
    new_tag = build_new_tag(image_repo, new_version)
    print(new_tag)

def get_current_version(version_file_path):
    with open(version_file_path, 'r') as f:
        current_version = f.read().strip()
    if current_version == '':
        raise Exception('version_file_path was empty.')
    return current_version

def update_version_file(version_file_path, new_version):
    with open(version_file_path, 'w') as f:
        f.write(str(new_version))

def build_new_tag(image_repo, new_version):
    new_tag = f'{image_repo}:{new_version}'
    return new_tag

if __name__ == "__main__":
    main()