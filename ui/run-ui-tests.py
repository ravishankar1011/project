import json
import os
import platform
import shlex
import shutil
import socket
import subprocess
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests  # For downloading Selenium JAR
from hugoutils.telemetry.logger import LogManager

logger = LogManager.get_logger(__name__)

# --- Configuration Variables ---
# These can be modified as needed
THREADS = 2  # Number of emulators launch
AVD_DEVICE_TYPE = "pixel_6"
# EMU_MEMORY_IN_MB = "2048"
TIMEOUT_SECONDS = 120
PARALLEL_EMU_START = 1  # Number of emulators this script will spin up parallelly

# SDK and Tools
AVD_NAME_BASE = "test_api30_avd"
ANDROID_PLATFORM_VERSION = "34"

# Port ranges
EMULATOR_PORT_START = 30000
EMULATOR_PORT_END = 30999
APPIUM_PORT_START = 31000
APPIUM_PORT_END = 31999
SELENIUM_NODE_PORT_START = 32000
SELENIUM_NODE_PORT_END = 32999

# Selenium Grid
HUB_PORT = 4444
SELENIUM_SERVER_VERSION = "4.13.0"  # User specified
SELENIUM_SERVER_JAR_NAME = f"selenium-server-{SELENIUM_SERVER_VERSION}.jar"
SELENIUM_SERVER_DOWNLOAD_URL = (f"https://github.com/SeleniumHQ/selenium/releases/download"
                                f"/selenium-{SELENIUM_SERVER_VERSION}/{SELENIUM_SERVER_JAR_NAME}")

# Working directory
SETUP_DIR = Path.cwd() / "ui_automation"
SELENIUM_JAR_PATH = SETUP_DIR / SELENIUM_SERVER_JAR_NAME

# Log directories
LOG_DIR = SETUP_DIR / "log"
APPIUM_LOG_DIR = LOG_DIR / "appium"
NODE_LOG_DIR = LOG_DIR / "node"
EMULATOR_LOG_DIR = LOG_DIR / "emulator"

# Global lists to store runtime info
RUNNING_EMULATOR_UDIDS = []
RUNNING_APPIUM_PORTS = []

lock = threading.RLock()

# --- Helper Functions ---
def log_step(message):
    """Prints a formatted step message."""
    print("\n" + "-" * 50)
    print(f"STEP: {message}")
    print("-" * 50)


def _is_rosetta_on_arm_mac():
    """Checks if the current Python process is running under Rosetta 2 on an ARM Mac."""
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        try:
            result = subprocess.run(["sysctl", "-n", "sysctl.proc_translated"], capture_output=True,
                                    text=True, check=False)
            return result.stdout.strip() == "1"
        except Exception as e:
            logger.error(f"Warning: Error checking Rosetta status: {e}. Assuming native.")
            return False


def run_command(command, check=True, shell=False, cwd=None, env=None, capture_output=False):
    """Runs a shell command."""
    if isinstance(command, str) and not shell:
        command = shlex.split(command)

    if _is_rosetta_on_arm_mac() and command[0] == "brew":
        logger.info("INFO: Prepending 'arch -arm64' to brew command due to Rosetta on ARM Mac.")
    command = ["arch", "-arm64"] + command
    logger.info(f"Executing: {' '.join(command) if isinstance(command, list) else command}")
    try:
        if capture_output:
            result = subprocess.run(command, check=check, shell=shell, cwd=cwd, env=env, text=True,
                                    capture_output=True)
            logger.info(result.stdout)
            if result.stderr:
                logger.error(f"STDERR:\n{result.stderr}")
            return result
        else:
            result = subprocess.run(command, check=check, shell=shell, cwd=cwd, env=env)
            return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing command: {e}")
        if capture_output:
            logger.info(f"STDOUT:\n{e.stdout}")
            logger.error(f"STDERR:\n{e.stderr}")
        raise e
    except FileNotFoundError as e:
        logger.error(f"Error: Command not found: {command}")
        raise e

def get_free_port(start_port, end_port):
    """Finds a free TCP port in the given range."""
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
            return port
        except OSError:
            continue
    raise IOError(f"No free port found in range {start_port}-{end_port}")


def start_emulator(index, system_image_package_name):
    avd_name = f"{AVD_NAME_BASE}-{index}"
    log_step(f"Starting Emulator Instance {index + 1} (AVD: {avd_name})")
    logger.info(f"Creating AVD: {avd_name} with device type {AVD_DEVICE_TYPE}...")
    avd_create_command = [
        "avdmanager", "create", "avd",
        "-n", avd_name,
        "-k", system_image_package_name,
        "--device", AVD_DEVICE_TYPE,
        "--force"
    ]
    subprocess.run(avd_create_command, input="no\n", text=True, check=True, capture_output=True)
    logger.info(f"AVD {avd_name} created/updated successfully.")

    emulator_log_file = EMULATOR_LOG_DIR / f"{avd_name}_{index}.log"

    emulator_console_port = get_free_port(EMULATOR_PORT_START, EMULATOR_PORT_END)
    logger.info(f"Starting Emulator {avd_name} on console port {emulator_console_port}...")

    emulator_command = [
        "emulator",
        "-avd", avd_name,
        "-port", str(emulator_console_port),
        "-no-snapshot-load",
        "-no-boot-anim",
        "-no-audio",
        "-gpu",
        "auto",
        # "-memory", EMU_MEMORY_IN_MB
        "-no-window"
    ]
    with open(emulator_log_file, "wb") as log_fp:
        process = subprocess.Popen(emulator_command, stdout=log_fp, stderr=log_fp)

    emulator_pid = process.pid
    logger.info(f"Emulator {avd_name} launch initiated with PID {emulator_pid}. Log: "
                f"{emulator_log_file}")

    emulator_udid = f"emulator-{emulator_console_port}"
    logger.info(f"Waiting for emulator {emulator_udid} to boot (max {TIMEOUT_SECONDS} seconds)...")
    seconds_elapsed = 0
    while seconds_elapsed < TIMEOUT_SECONDS:
        check_boot_command = ["adb", "-s", emulator_udid, "shell", "getprop", "sys.boot_completed"]
        result_boot = subprocess.run(check_boot_command, capture_output=True, text=True,
                                     timeout=5)
        check_dev_command = ["adb", "-s", emulator_udid, "shell", "getprop", "dev.bootcomplete"]
        result_dev = subprocess.run(check_dev_command, capture_output=True, text=True,
                                    timeout=5)

        if result_boot.stdout.strip() == "1" and result_dev.stdout.strip() == "1":
            print()
            logger.info(f"\nEmulator ({emulator_udid}) booted successfully.")
            return emulator_udid
        print(".", end="", flush=True)
        time.sleep(5)  # Increased sleep from 2 to 5 for less spammy output
        seconds_elapsed += 5

    logger.error(
        f"\nError: Emulator ({emulator_udid}) did not boot within {TIMEOUT_SECONDS} seconds.")
    exit(1)


def setup_environment_paths_macos():
    """Sets up ANDROID_SDK_ROOT and PATH for macOS."""
    android_home_brew = Path("/opt/homebrew/bin")
    android_sdk_root_brew_share = Path("/opt/homebrew/share/android-commandlinetools")
    standard_sdk_root = Path.home() / "Library" / "Android" / "sdk"

    # Prioritize standard SDK root if it exists and contains cmdline-tools
    if (standard_sdk_root / "cmdline-tools" / "latest" / "bin" / "sdkmanager").exists():
        os.environ["ANDROID_SDK_ROOT"] = str(standard_sdk_root)
        logger.info(f"Using standard ANDROID_SDK_ROOT: {standard_sdk_root}")
    elif android_sdk_root_brew_share.exists():
        os.environ["ANDROID_SDK_ROOT"] = str(android_sdk_root_brew_share)
        logger.info(f"Using brew share path for ANDROID_SDK_ROOT: {android_sdk_root_brew_share}")
    else:
        logger.error(
            "Warning: Could not determine a robust ANDROID_SDK_ROOT. Using Homebrew bin for "
            "ANDROID_HOME as per bash script.")
        os.environ["ANDROID_SDK_ROOT"] = str(android_home_brew)

    os.environ["ANDROID_HOME"] = os.environ["ANDROID_SDK_ROOT"]

    sdk_root = os.environ["ANDROID_SDK_ROOT"]
    new_paths = [
        str(Path(sdk_root) / "emulator"),
        str(Path(sdk_root) / "tools"),
        str(Path(sdk_root) / "tools" / "bin"),
        str(Path(sdk_root) / "platform-tools"),
        str(Path(sdk_root) / "cmdline-tools" / "latest" / "bin"),
        "/opt/homebrew/bin",
        "/usr/local/bin"
    ]
    os.environ["PATH"] = os.pathsep.join(new_paths) + os.pathsep + os.environ.get("PATH", "")
    logger.info(f"Updated PATH for macOS.")


def setup_environment_paths_linux():
    """Sets up ANDROID_SDK_ROOT and PATH for Linux."""
    sdk_root_dir = Path.home() / "Android"  # Matches bash script's sdkmanager install location
    os.environ["ANDROID_SDK_ROOT"] = str(sdk_root_dir)
    os.environ["ANDROID_HOME"] = str(sdk_root_dir)

    new_paths = [
        str(sdk_root_dir / "emulator"),
        str(sdk_root_dir / "cmdline-tools" / "latest" / "bin"),
        str(sdk_root_dir / "platform-tools")
    ]
    os.environ["PATH"] = os.pathsep.join(new_paths) + os.pathsep + os.environ.get("PATH", "")
    logger.info(f"Updated PATH for Linux.")


def main():
    global RUNNING_EMULATOR_UDIDS, RUNNING_APPIUM_PORTS

    # --- Initial Setup ---
    log_step("Initial Setup")

    # Create directories
    shutil.rmtree(LOG_DIR, ignore_errors=True)  # Clear old logs if they exist
    SETUP_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    APPIUM_LOG_DIR.mkdir(parents=True, exist_ok=True)
    NODE_LOG_DIR.mkdir(parents=True, exist_ok=True)
    EMULATOR_LOG_DIR.mkdir(parents=True, exist_ok=True)
    (SETUP_DIR / "config").mkdir(parents=True, exist_ok=True)  # For TOML files

    logger.info(f"Setup directory: {SETUP_DIR}")
    logger.info(f"Log directory: {LOG_DIR}")

    # OS Detection
    system = platform.system()
    is_macos = (system == "Darwin")
    is_linux = (system == "Linux")

    if not is_macos and not is_linux:
        logger.error(f"Error: Unsupported OS '{system}'. This script supports macOS and Linux.")
        sys.exit(1)

    # 1. Install Java
    log_step("Checking/Installing Java (OpenJDK 17)")
    try:
        java_version_result = run_command("java -version", capture_output=True, check=False)
        if java_version_result and java_version_result.returncode == 0:
            logger.info(f"Java is already installed: {java_version_result.stderr.splitlines()[0]}")
        else:
            raise FileNotFoundError  # Trigger installation
    except (FileNotFoundError, AttributeError):  # AttributeError if result is None
        logger.info("Java not found or version check failed. Installing OpenJDK 17...")
        if is_macos:
            run_command("brew install openjdk@17")
            # Symlink for system Java wrappers if needed (often handled by brew)
            logger.info("Ensure /opt/homebrew/opt/openjdk@17/bin is in your PATH or set JAVA_HOME.")
            exit(1)
        elif is_linux:
            run_command("sudo apt-get update -y")
            run_command("sudo apt-get install -y openjdk-17-jdk")
        logger.info("Java installation complete.")

    # 2. Install Android Command Line Tools & Appium
    log_step("Installing Android Command Line Tools and Appium")
    if is_macos:
        if not shutil.which("brew"):
            logger.info("Homebrew not found. Installing Homebrew...")
            run_command(
                '/bin/bash -c "$(curl -fsSL '
                'https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                shell=True)
            # Update PATH for current script - brew might instruct to do this manually in .zprofile
            os.environ["PATH"] = "/opt/homebrew/bin:" + os.environ.get("PATH", "")

        run_command("brew install --cask android-commandlinetools")
        setup_environment_paths_macos()  # Set ANDROID_SDK_ROOT and PATH

        if not shutil.which("appium"):
            if not shutil.which("npm"):
                logger.info("npm not found. Installing npm via Homebrew...")
                run_command("brew install node")
            logger.info("Installing Appium via npm...")
            run_command("npm install -g appium")
        else:
            logger.info(
                f"Appium is already installed: "
                f"{run_command('appium -v', capture_output=True).stdout.strip()}")

        if not shutil.which("jq"):
            run_command("brew install jq")

    elif is_linux:
        cmdline_tools_zip = SETUP_DIR / "cmdline-tools.zip"
        android_sdk_cmdline_tools_dir = Path(
            os.environ.get("ANDROID_SDK_ROOT", Path.home() / "Android")) / "cmdline-tools"
        latest_tools_dir = android_sdk_cmdline_tools_dir / "latest"

        if not cmdline_tools_zip.exists() and not latest_tools_dir.exists():
            logger.info("Downloading Android command line tools for Linux...")
            cmdline_tools_url = ("https://dl.google.com/android/repository/commandlinetools-linux"
                                 "-11076708_latest.zip")
            try:
                response = requests.get(cmdline_tools_url, stream=True)
                response.raise_for_status()
                with open(cmdline_tools_zip, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                logger.info("Command line tools downloaded.")
            except requests.RequestException as e:
                logger.error(f"Failed to download command line tools: {e}")
                sys.exit(1)

        if cmdline_tools_zip.exists() and not latest_tools_dir.exists():
            logger.info("Unzipping command line tools...")
            android_sdk_cmdline_tools_dir.mkdir(parents=True, exist_ok=True)
            temp_unzip_dir = SETUP_DIR / "temp_cmdline_unzip"
            shutil.unpack_archive(cmdline_tools_zip, temp_unzip_dir)

            unzipped_inner_dir = temp_unzip_dir / "cmdline-tools"  # Default structure from
            if unzipped_inner_dir.exists():
                latest_tools_dir.mkdir(parents=True, exist_ok=True)
                for item in unzipped_inner_dir.iterdir():
                    shutil.move(str(item), str(latest_tools_dir / item.name))
                shutil.rmtree(temp_unzip_dir)
                logger.info(f"Command line tools moved to {latest_tools_dir}")
            else:
                logger.error(
                    f"Error: Expected 'cmdline-tools' directory not found after unzipping to "
                    f"{temp_unzip_dir}")
                sys.exit(1)

        setup_environment_paths_linux()  # Set ANDROID_SDK_ROOT and PATH

        if not shutil.which("appium"):
            if not shutil.which("npm"):
                logger.info("npm not found. Installing npm...")
                run_command("sudo apt-get install -y npm")  # Might need nodejs too
            logger.info("Installing Appium globally via npm (sudo might be required)...")
            run_command("sudo npm install -g appium")  # Sudo common for global npm on Linux
        else:
            logger.info(
                f"Appium is already installed: "
                f"{run_command('appium -v', capture_output=True).stdout.strip()}")

    # Check and install Appium uiautomator2 driver
    try:
        driver_list_result = run_command("appium driver list --installed --json",
                                         capture_output=True, check=True)
        installed_drivers = json.loads(driver_list_result.stdout)
        if not installed_drivers.get("uiautomator2", {}).get("installed", False):
            raise ValueError("uiautomator2 driver not found in JSON output")  # Trigger install
        logger.info("Appium driver 'uiautomator2' is already installed. Skipping.")
    except (subprocess.CalledProcessError, ValueError, json.JSONDecodeError) as e:
        logger.info(
            f"Failed to check installed drivers or uiautomator2 not found ({e}). Installing "
            f"Appium driver 'uiautomator2'...")
        run_command("appium driver install uiautomator2")
    logger.info("Android Command Line Tools and Appium setup check complete.")

    # 3. Install Android SDK Packages
    log_step(f"Installing Android SDK Packages (API {ANDROID_PLATFORM_VERSION})")
    sdk_root_path = os.environ.get("ANDROID_SDK_ROOT")
    if not sdk_root_path:
        logger.error("Error: ANDROID_SDK_ROOT is not set. Cannot run sdkmanager.")
        sys.exit(1)

    logger.info("Attempting to accept SDK licenses...")
    try:
        run_command(f"yes | sdkmanager --licenses", shell=True, check=False)
        logger.info("SDK license acceptance command executed.")
    except Exception as e:
        logger.warning(
            f"Warning: SDK license command had an issue: {e}, might have already been accepted")

    logger.info("Installing core SDK packages...")
    packages_to_install = [
        "platform-tools",
        f"platforms;android-{ANDROID_PLATFORM_VERSION}",
        "emulator"
    ]
    for pkg in packages_to_install:
        logger.info(f"Installing {pkg}...")
        run_command(f"sdkmanager {pkg}")

    # System image
    cpu_arch_host = run_command("uname -m", capture_output=True).stdout
    if cpu_arch_host in ["x86_64", "x86_64\n"]:
        system_image_arch_suffix = "x86_64"
    elif cpu_arch_host in ["aarch64", "aarch64\n", "arm64", "arm64\n"]:
        system_image_arch_suffix = "arm64-v8a"
    else:
        logger.error(
            f"Warning: Unsupported host CPU architecture '{cpu_arch_host}'. Defaulting to x86_64 "
            f"for system image.")
        system_image_arch_suffix = "x86_64"

    system_image_package_name = (f"system-images;android-{ANDROID_PLATFORM_VERSION};google_apis;"
                                 f"{system_image_arch_suffix}")
    logger.info(
        f"Installing system image for {system_image_arch_suffix}: {system_image_package_name}")
    run_command(f"sdkmanager {system_image_package_name}")
    logger.info("SDK package installation complete.")

    # 4. Create and Start Android Emulators (Sequentially as per bash script logic)
    log_step(f"Creating and starting {THREADS} Android Emulators")

    with ThreadPoolExecutor(PARALLEL_EMU_START) as executor:
        futures = [
            executor.submit(start_emulator, i, system_image_package_name)
            for i in range(THREADS)
        ]
        RUNNING_EMULATOR_UDIDS = [f.result() for f in futures]

    # 5. Downloading APK from S3 (Placeholder)
    log_step("Downloading APK (Placeholder)")
    logger.info("TODO: Implement APK download from S3 or artifact repository")

    # 6. Start Appium Servers
    log_step(f"Starting {len(RUNNING_EMULATOR_UDIDS)} Appium Servers")
    for i, emulator_udid in enumerate(RUNNING_EMULATOR_UDIDS):
        appium_port = get_free_port(APPIUM_PORT_START, APPIUM_PORT_END)

        logger.info(
            f"Starting Appium on port {appium_port} for emulator: {emulator_udid}")
        appium_log_path = APPIUM_LOG_DIR / f"appium_{i}.log"

        default_caps = json.dumps({
            "appium:udid": emulator_udid,
        })

        appium_command = [
            "appium", "server",
            "-p", str(appium_port),
            "--default-capabilities", default_caps,
            "--log-timestamp",
            "--log-no-colors"
        ]

        with open(appium_log_path, "wb") as log_fp:
            process = subprocess.Popen(appium_command, stdout=log_fp, stderr=log_fp)
        RUNNING_APPIUM_PORTS.append(appium_port)
        logger.info(
            f"Appium server for {emulator_udid} starting with PID {process.pid}. Log: "
            f"{appium_log_path}")
        time.sleep(5)

    if not RUNNING_APPIUM_PORTS:
        logger.error("Error: No Appium servers were started.")
        sys.exit(1)

    # 7. Download Selenium Server JAR
    log_step("Downloading Selenium Server JAR")
    if SELENIUM_JAR_PATH.exists():
        logger.info(f"Selenium Server JAR already exists: {SELENIUM_JAR_PATH}")
    else:
        logger.info(
            f"Downloading {SELENIUM_SERVER_JAR_NAME} from {SELENIUM_SERVER_DOWNLOAD_URL}...")
        try:
            response = requests.get(SELENIUM_SERVER_DOWNLOAD_URL, stream=True)
            response.raise_for_status()
            with open(SELENIUM_JAR_PATH, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.info(f"Selenium Server JAR downloaded to {SELENIUM_JAR_PATH}")
        except requests.RequestException as e:
            logger.error(f"Failed to download Selenium JAR: {e}")
            sys.exit(1)

    # 8. Create Selenium Node TOML Configuration Files
    log_step("Creating Selenium Node TOML configuration files")
    node_config_files = []
    for i, appium_port_for_node in enumerate(RUNNING_APPIUM_PORTS):
        node_config_file_path = SETUP_DIR / "config" / f"device_capabilities_{i}.toml"

        toml_content = (f"\n"
                        f"[node]\n"
                        f"detect-drivers = false\n"
                        f"max-sessions = 1 # Each node handles one Appium server/device\n"
                        f"\n"
                        f"[relay]\n"
                        f"url = \"http://localhost:{appium_port_for_node}\"\n"
                        f"status-endpoint = \"/status\"\n"
                        f"# Capabilities advertised by this Selenium Node for the Appium instance "
                        f"it relays to\n"
                        f"configs = [\n"
                        f"  \"1\", \"{{\\\"appium:deviceName\\\": \\\"PIXEL_API"
                        f"{ANDROID_PLATFORM_VERSION}\\\", \\\"platformName\\\": \\\"Android\\\", "
                        f"\\\"appium:platformVersion\\\": \\\"{ANDROID_PLATFORM_VERSION}.0\\\", "
                        f"\\\"appium:automationName\\\": \\\"UiAutomator2\\\", "
                        f"\\\"appium:udid\\\": \\\"{RUNNING_EMULATOR_UDIDS[i]}\\\"}}\"]\n")

        with open(node_config_file_path, "w") as f:
            f.write(toml_content)
        node_config_files.append(node_config_file_path)
        logger.info(f"Node configuration file created: {node_config_file_path}")

    if not node_config_files:
        logger.error(
            "Error: No node configuration files were created. Cannot start Selenium nodes.")
        sys.exit(1)

    # 9. Start Selenium Grid Hub
    log_step("Starting Selenium Grid Hub")
    logger.info(f"Starting Selenium Grid Hub on port {HUB_PORT}...")
    hub_log_path = LOG_DIR / "hub.log"
    hub_command = [
        "java", "-jar", str(SELENIUM_JAR_PATH),
        "hub", "--port", str(HUB_PORT)
    ]
    with open(hub_log_path, "wb") as log_fp:
        process = subprocess.Popen(hub_command, stdout=log_fp, stderr=log_fp)
    logger.info(f"Selenium Hub starting with PID {process.pid}. Log: {hub_log_path}")
    time.sleep(10)

    # 10. Start Selenium Grid Nodes
    log_step(f"Starting {len(node_config_files)} Selenium Grid nodes")
    for i, node_config_file in enumerate(node_config_files):
        node_port = get_free_port(SELENIUM_NODE_PORT_START, SELENIUM_NODE_PORT_END)
        logger.info(
            f"Starting Selenium Grid node on port {node_port}, using config {node_config_file}...")
        node_log_path = NODE_LOG_DIR / f"node_{i}.log"

        node_command = [
            "java", "-jar", str(SELENIUM_JAR_PATH),
            "node", "--port", str(node_port),
            "--config", str(node_config_file),
        ]
        with open(node_log_path, "wb") as log_fp:
            process = subprocess.Popen(node_command, stdout=log_fp, stderr=log_fp)
        logger.info(f"Selenium Node starting with PID {process.pid}. Log: {node_log_path}")
        time.sleep(5)  # Give node time to register

    log_step("Setup Complete!")
    logger.info("To stop services: bash shutdown-process.sh")


if __name__ == "__main__":
    main()
