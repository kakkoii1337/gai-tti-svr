import toml,os,subprocess

base_name="gai-tti"
   
def __get_version(pyproject_path):
    with open(pyproject_path, "r+") as f:
        data = toml.load(f)
    return data["tool"]["poetry"]["version"]

def _docker_run_tti(pyproject_path):
    version=__get_version(pyproject_path)
    cmd=f"""docker container stop gai-tti && docker container rm -f gai-tti"""
    os.system(cmd)

    cmd=f"""docker run -d \
        -e CLI_ARGS="--listen --api --xformers --medvram --ckpt /stable-diffusion-webui/models/Stable-diffusion/runwayml/v1-5-pruned-emaonly.safetensors --no-download-sd-model" \
        --gpus all \
        -v ~/.gai/models/Stable-diffusion:/stable-diffusion-webui/models/Stable-diffusion \
        -v ~/.gai/models/VAE:/stable-diffusion-webui/models/VAE \
        -p 12035:12035 \
        --name gai-tti \
        --network gai-sandbox \
        gai-tti:{version}"""
    os.system(cmd)

def main():
    here=os.path.dirname(__file__)
    pyproject_dir=os.path.join(here,'..')
    dockerfile_dir=pyproject_dir
    pyproject_path=os.path.join(pyproject_dir,'pyproject.toml')

    # Get the version from the pyproject.toml file
    _docker_run_tti(pyproject_path)

if __name__ == "__main__":
    main()