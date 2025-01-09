import os
import subprocess
import sys
import shutil
import tempfile
import re
from pathlib import Path
from importlib import resources  # Python 3.9+

SOKOWEB_TEMPFILE_NAME = ".sokoweb_temp_dir"
SOKOWEB_HF_TEMPFILE_NAME = ".sokoweb_hf_temp_dir"

def read_existing_env(env_path):
    existing_vars = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    existing_vars[key.strip()] = value.strip()
    return existing_vars

def validate_port(port):
    try:
        p_int = int(port)
        return 1024 <= p_int <= 65535
    except ValueError:
        return False

def validate_hostname(hostname):
    if not hostname:
        return False
    ip_pattern = re.compile(r'^(\d{1,3}.){3}\d{1,3}|[a-zA-Z0-9.-]+$')
    return bool(ip_pattern.match(hostname))

def prompt_for_three_vars(existing_vars):
    """
    Prompt ONLY for NODE_PORT, NODE_TCP_PORT, ADVERTISE_IP.
    If user hits Enter, keep existing .env value or use defaults.
    """
    # 1) NODE_PORT
    default_node_port = existing_vars.get('NODE_PORT', '8000')
    while True:
        node_port = input(
            f"Enter NODE_PORT (press Enter for default {default_node_port}): "
        ).strip()
        if not node_port:
            node_port = default_node_port
        if validate_port(node_port):
            existing_vars["NODE_PORT"] = node_port
            break
        print("Invalid port! Must be between 1024 and 65535.")

    # 2) NODE_TCP_PORT
    default_tcp_port = existing_vars.get('NODE_TCP_PORT', '8500')
    while True:
        node_tcp_port = input(
            f"Enter NODE_TCP_PORT (press Enter for default {default_tcp_port}): "
        ).strip()
        if not node_tcp_port:
            node_tcp_port = default_tcp_port
        if validate_port(node_tcp_port):
            existing_vars["NODE_TCP_PORT"] = node_tcp_port
            break
        print("Invalid port! Must be between 1024 and 65535.")

    # 3) ADVERTISE_IP
    default_ip = existing_vars.get('ADVERTISE_IP', 'localhost')
    while True:
        advertise_ip = input(
            f"Enter ADVERTISE_IP (e.g., example.com) [default {default_ip}]: "
        ).strip()
        if not advertise_ip:
            advertise_ip = default_ip
        if validate_hostname(advertise_ip):
            existing_vars["ADVERTISE_IP"] = advertise_ip
            break
        print("Invalid hostname/IP! Please enter a valid hostname or IP address.")

def set_default_vars(existing_vars):
    """
    Force certain environment variables to have the same defaults
    as your docker-compose.yml. If the user hasn't defined them,
    we hard-code them here.
    """
    hardcoded_defaults = {
        "SECRET_KEY": "root",
        "ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
        "ENCRYPTION_PASSWORD": "s3cr3t_p@ssw0rd",
        "MPESA_CONSUMER_KEY": "qKWanfm4aw1FoduqOGGDBdv0f7UJf8Li",
        "MPESA_CONSUMER_SECRET": "07QvgShVQBVRF0eE",
        "BUSINESS_SHORT_CODE": "6290257",
        "PASSKEY": "390a62dc3a65c889ce9275360b7ee8c875e115c2bb0e3a312446f9a9740fb20d",
        "CALLBACK_URL": "https://example.com",
        "TESTING": "false",
        "POSTGRES_HOST": "postgres",
        "IS_VALIDATOR": "true",
    }
    for k, v in hardcoded_defaults.items():
        if k not in existing_vars or not existing_vars[k]:
            existing_vars[k] = v

def write_env(env_path, vars_dict):
    try:
        with open(env_path, 'w') as f:
            for k, v in vars_dict.items():
                f.write(f"{k}={v}\n")
    except Exception as e:
        print(f"Error writing .env: {e}")
        sys.exit(1)

def copy_traversable(src_traversable, dst_path: Path):
    """
    Recursively copy all files/subdirectories from src_traversable
    (which is an importlib Traversable) to dst_path.
    """
    dst_path.mkdir(parents=True, exist_ok=True)
    for child in src_traversable.iterdir():
        if child.is_dir():
            copy_traversable(child, dst_path / child.name)
        else:
            with resources.as_file(child) as local_file:
                shutil.copy2(local_file, dst_path / child.name)

def up(detached=False):
    """
    Bring up Docker containers for the DHT node using a persistent temp directory.
    Store the temp directory path so we can reference it in 'down()'.
    """
    print("\nSetting up environment variables...")

    temp_dir_path = tempfile.mkdtemp()

    from importlib import resources
    docker_dir = resources.files("sokoweb.docker")

    # Copy Dockerfile, docker-compose.yml
    with resources.as_file(docker_dir / "Dockerfile") as dockerfile_path:
        shutil.copyfile(dockerfile_path, f"{temp_dir_path}/Dockerfile")

    with resources.as_file(docker_dir / "docker-compose.yml") as compose_path:
        shutil.copyfile(compose_path, f"{temp_dir_path}/docker-compose.yml")

    env_path = Path(temp_dir_path) / ".env"
    user_env = Path.cwd() / ".env"
    if user_env.exists():
        shutil.copyfile(user_env, env_path)

    existing_vars = read_existing_env(env_path)
    prompt_for_three_vars(existing_vars)
    set_default_vars(existing_vars)

    if existing_vars["ADVERTISE_IP"] == "localhost":
        existing_vars["BOOTSTRAP_NODES"] = ""
    else:
        if "BOOTSTRAP_NODES" not in existing_vars or not existing_vars["BOOTSTRAP_NODES"]:
            existing_vars["BOOTSTRAP_NODES"] = "ec2-13-49-77-213.eu-north-1.compute.amazonaws.com:8000"

    write_env(env_path, existing_vars)

    with open(SOKOWEB_TEMPFILE_NAME, "w") as f:
        f.write(temp_dir_path)

    print("\nStarting Docker containers (DHT node)...")
    compose_cmd = ["docker", "compose", "-f", "docker-compose.yml", "up", "--build"]
    if detached:
        compose_cmd.append("-d")

    try:
        process = subprocess.run(compose_cmd, check=True, cwd=temp_dir_path)
        if process.returncode == 0:
            if detached:
                print("Successfully started DHT Docker containers in detached mode.")
            else:
                print("Successfully started DHT Docker containers.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting Docker containers (exit code={e.returncode})")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

def down():
    """
    Stop/remove containers (and volumes) by reading .sokoweb_temp_dir.
    """
    print("Stopping Docker containers (DHT) and removing volumes...")
    temp_file = Path.cwd() / SOKOWEB_TEMPFILE_NAME
    if not temp_file.exists():
        print(f"No {SOKOWEB_TEMPFILE_NAME} file found in the current directory.")
        print("Cannot determine where docker-compose.yml is located.")
        return

    with open(temp_file, "r") as f:
        temp_dir_path = f.read().strip()

    docker_compose_file = Path(temp_dir_path) / "docker-compose.yml"
    if not docker_compose_file.exists():
        print("No docker-compose.yml found in the stored temp directory path!")
        return

    try:
        subprocess.run(
            ["docker", "compose", "-f", str(docker_compose_file), "down", "-v"],
            check=True,
            cwd=temp_dir_path
        )
        print("Successfully stopped and removed containers/volumes (DHT).")
    except subprocess.CalledProcessError as e:
        print(f"Error stopping Docker containers (exit code={e.returncode})")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

    shutil.rmtree(temp_dir_path, ignore_errors=True)
    temp_file.unlink(missing_ok=True)

def hyperledger_up(detached=False):
    """
    Bring up Hyperledger Fabric containers, generate MSP+channel artifacts,
    create channel, install chaincode, etc.
    """
    print("\nSetting up Hyperledger Fabric network...")

    temp_dir_path = tempfile.mkdtemp()

    from importlib import resources
    hf_dir = resources.files("sokoweb.hyperledger_docker")

    # Recursively copy the entire hyperledger_docker folder to temp_dir
    copy_traversable(hf_dir, Path(temp_dir_path))

    # store path so we can do hyperledger_down
    with open(SOKOWEB_HF_TEMPFILE_NAME, "w") as f:
        f.write(temp_dir_path)

    # 1) Generate MSP + channel artifacts before containers come up
    generate_script = Path(temp_dir_path) / "scripts" / "generate-certs.sh"
    if generate_script.exists():
        print("Generating MSP & channel artifacts (crypto-config, configtxgen)...")
        try:
            subprocess.run(["bash", "scripts/generate-certs.sh"], check=True, cwd=temp_dir_path)
        except subprocess.CalledProcessError as e:
            print(f"Error generating certs (exit code={e.returncode})")
            sys.exit(e.returncode)
    else:
        print("No generate-certs.sh script found, skipping MSP+channel artifacts generation.")

    # 2) Now start the containers
    compose_cmd = ["docker", "compose", "-f", "docker-compose-hf.yml", "up", "--build"]
    if detached:
        compose_cmd.append("-d")

    try:
        subprocess.run(compose_cmd, check=True, cwd=temp_dir_path)
        print("Hyperledger Fabric containers are up.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting Fabric containers (exit code={e.returncode})")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

    # 3) Create channel, install chaincode
    setup_script = Path(temp_dir_path) / "scripts" / "setup_channels.sh"
    if setup_script.exists():
        print("Creating channel, installing chaincode...")
        try:
            subprocess.run(["bash", str(setup_script)], check=True, cwd=temp_dir_path)
            print("Fabric network and channel setup complete.")
        except subprocess.CalledProcessError as e:
            print(f"Error setting up channel (exit code={e.returncode})")
            sys.exit(e.returncode)
    else:
        print("No setup_channels.sh script found, skipping channel/chaincode setup.")

def hyperledger_down():
    """
    Stop/remove Fabric containers, volumes.
    """
    print("Stopping Hyperledger Fabric containers and removing volumes...")
    temp_file = Path.cwd() / SOKOWEB_HF_TEMPFILE_NAME
    if not temp_file.exists():
        print(f"No {SOKOWEB_HF_TEMPFILE_NAME} file found in the current directory.")
        return

    with open(temp_file, "r") as f:
        temp_dir_path = f.read().strip()

    docker_compose_file = Path(temp_dir_path) / "docker-compose-hf.yml"
    if not docker_compose_file.exists():
        print("No docker-compose-hf.yml found in the stored temp directory path!")
        return

    try:
        subprocess.run(
            ["docker", "compose", "-f", str(docker_compose_file), "down", "-v"],
            check=True,
            cwd=temp_dir_path
        )
        print("Fabric containers and volumes removed.")
    except subprocess.CalledProcessError as e:
        print(f"Error stopping Fabric containers (exit code={e.returncode})")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

    shutil.rmtree(temp_dir_path, ignore_errors=True)
    temp_file.unlink(missing_ok=True)

if __name__ == "__main__":
    """
    Usage (while in the same directory):
    python cli.py => up() in foreground (DHT)
    python cli.py -d => up() in detached mode (DHT)
    python cli.py down => down() (stop DHT)
    python cli.py hf-up => hyperledger_up() (Fabric)
    python cli.py hf-up -d => hyperledger_up() detached (Fabric)
    python cli.py hf-down => hyperledger_down() (Fabric)
    """
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "down":
            down()
        elif arg in ["-d", "--detached"]:
            up(detached=True)
        elif arg == "hf-up":
            # check if next arg is -d
            if len(sys.argv) > 2 and sys.argv[2].lower() in ["-d", "--detached"]:
                hyperledger_up(detached=True)
            else:
                hyperledger_up(detached=False)
        elif arg == "hf-down":
            hyperledger_down()
        else:
            up(detached=False)
    else:
        up(detached=False)