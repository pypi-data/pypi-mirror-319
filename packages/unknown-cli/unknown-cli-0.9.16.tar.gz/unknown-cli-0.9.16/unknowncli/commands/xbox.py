import sys
import shutil
import time
import os
import socket
import getpass
from datetime import datetime, timedelta
from tabulate import tabulate
import click
from click import echo, secho
from pathlib import Path
from subprocess import call, Popen, PIPE
from pprint import pprint
import json
from collections import defaultdict
from dateutil.parser import parse

my_path = Path(__file__).parent
builds_file = my_path / "builds.json"
cached_builds = {}
xbapps_ensured = False
console_ip = None
temp_path = Path("c:/temp/xboxbuilds/")
temp_path.mkdir(parents=True, exist_ok=True)

def abort(msg):
    secho(msg, fg="red")
    sys.exit(1)

def get_timestamp_from_logline(l):
    timestamp_string = l.split("]")[0][1:].split(":")[0]
    try:
        timestamp = datetime.strptime(timestamp_string, "%Y.%m.%d-%H.%M.%S")
    except Exception as e:
        return datetime.now()
    return timestamp

def parse_changelists(changelists_string, config):
    all_builds = collect_builds()
    changelists = []
    if "," in changelists_string:
        changelists = changelists_string.split(",")
    elif "-" in changelists_string:
        lst = changelists_string.split("-")
        lst.sort()

        if len(lst) != 2:
            abort("Changelist range must be in the form [from]-[to]")
        first_changelist = int(lst[0])
        last_changelist = int(lst[1] or "999999999")
        for changelist, builds in all_builds.items():
            found_build = None
            if changelist >= first_changelist and changelist <= last_changelist:
                for b in builds:
                    if b['configuration'].lower() == config.lower():
                        found_build = b
            if found_build:
                changelists.append(changelist)
    else:
        changelists = [int(changelists_string)]
    for cl in changelists:
        if cl not in all_builds:
            abort(f"Changelist {cl} not found")
    if not changelists:
        abort(f"Did not find valid changeslists in '{changelists_string}' for config '{config}'")
    return changelists


def collect_builds():
    global cached_builds
    if cached_builds:
        return cached_builds
    builds_path = Path("U:/SN2")
    builds_by_changelist = defaultdict(list)
    for f in builds_path.iterdir():
        if "_MAIN_" not in str(f):
            continue
        n = f.name
        lst = n.replace("CL-", "").split("_")
        build_number = int(lst[0])
        branch = lst[-2]
        configuration = "Test" if "test" in n.lower() else "Development"
        changelist = int(lst[-1])
        builds_by_changelist[changelist].append((f.name, branch, configuration))
    builds_by_changelist = dict(sorted(builds_by_changelist.items()))
    #pprint(builds_by_changelist)
    builds = get_builds()
    if not builds:
        secho("Running initial scan. This will take a while...", fg="yellow")
    n = 0
    for changelist, folders in builds_by_changelist.items():
        if changelist in builds:
            builds_by_changelist[changelist] = builds[changelist]
            continue
        if changelist not in builds:
            builds[changelist] = []

        for folder, branch, configuration in folders:
            path = builds_path / folder
            # U:\SN2\10147_TEST_MAIN_CL-53357\Publish\++project+sn2-main-ue\Subnautica2-CL-53353\XSX\Packages\Test
            package_path = path / "Publish" / "++project+sn2-main-ue"
            #print(package_path)
            # / f"Subnautica2-CL-{changelist}" / "XSX\Packages" / "Test"
            for f in package_path.glob("*/XSX/Packages/*/*.xvc"):
                if f.is_file():
                    print(f"Found XBox build for {folder}")
                    build = {
                        "filename": f.name,
                        "path": f.as_posix(),
                        "configuration": configuration,
                        "branch": branch,
                        "size_mb": f.stat().st_size // 1024 // 1024,
                        "timestamp": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
                    }
                    builds[changelist].append(build)
                    n += 1
            
        save_builds(builds)
    cached_builds = builds
    return builds

def get_loglines(num=None):
    ensure_xbapps()
    path = Path(f"//{console_ip}/SystemScratch/Logs/Subnautica2.log")
    if not path.is_file():
        abort(f"Path {path} not found")
    with path.open() as f:
        lines = f.readlines()
    ret = []
    if num:
        lines = lines[-num:]
    for l in lines:
        ret.append(l.strip())
    return ret

def ensure_xbapps():
    global console_ip
    if console_ip:
        return
    game_dk = os.environ.get("GAMEDK")
    if not game_dk:
        abort("XBox GDK Manager is not installed")
    game_bin_path = Path(game_dk) / "bin"
    xbapp = game_bin_path / "xbapp.exe"
    xbconnect = game_bin_path / "xbconnect.exe"
    if not xbapp.is_file() or not xbconnect.is_file():
        abort("XBox GDK Manager is not installed")
    p = Popen(f"{xbconnect} /q /b", stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if not not p.returncode:
        abort("No XBox console found (1)")

    console_ip = out.strip().decode()
    if not console_ip.startswith("192."):
        abort("No XBox console found (2)")

def xb(appname):
    ensure_xbapps()
    return Path(os.environ.get("GAMEDK")) / "bin" / appname

def get_builds():
    try:
        with open(builds_file) as f:
            return {int(k): v for k, v in json.load(f).items()}
    except Exception as e:
        return {}

def save_builds(data):
    with open(builds_file, "w") as f:
        json.dump(data, f, indent=4)

def mount():
    p = Path("U:")
    if p.is_dir():
        return
    mountbat_filename = my_path.parent / "BatchFiles" / "MountBuildsFolder.bat"
    cmd = ["net", "use", "U:", r"\\sn2-storage-int.metal.subnautica.net\storage /persistent:yes /user:install belabour-hull-calcutta"]
    p = Popen(cmd, shell=True)
    stdout, stderr = p.communicate()

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    """
    Manage xbox builds and run xbox phototours
    """
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug

@cli.command("list")
@click.option("-t", "--type", "config", default="None", help="Test or Development configuration (default is both)")
@click.option("-n", "--num", default=10, show_default=True, help="Maximum number of builds to show")
@click.option("-d", "--days", default=7, show_default=True, help="Show builds from the last few days")
@click.pass_context
def list_builds(ctx, config, num, days):
    """
    List out the builds in the build folder on teamcity.
    This might take a while to collect the builds
    """
    mount()
    builds = collect_builds()
    hdr = ["CL", "timestamp", "config", "GB"]
    lst = []
    for changelist, builds in builds.items():
        for build in builds:
            dt = parse(build["timestamp"])
            if dt < datetime.now() - timedelta(days=days):
                continue
            if config and build['configuration'].lower() != config.lower():
                continue
            lst.append([changelist, dt.strftime("%Y-%m-%d %H:%M"), build['configuration'], round(build['size_mb']/1024, 1)])
    lst.reverse()
    lst = lst[:num]
    echo(tabulate(lst, hdr))

@cli.command()
@click.option("-n", "--num")
@click.option("-f", "--filter")
@click.pass_context
def tail(ctx, num, filter):
    num = int(num) if num else 100
    lines = get_loglines(num)
    for l in lines:
        if not filter or filter.lower() in l.lower():
            print(l)

@cli.command()
@click.pass_context
def kill(ctx):
    """
    Terminate the currently running executable on your xbox
    """
    ensure_xbapps()
    xbapp = xb("xbapp.exe")
    cmd = [xbapp, "terminate"]
    call(cmd)

@cli.command()
@click.option("-m", "--mode", "kit_mode", help="Set mode to xss or xsx")
@click.pass_context
def mode(ctx, kit_mode):
    """
    Switch the xbox console between Lockhart (series S) and Anaconda (series X) modes.
    This will restart the console.
    """
    ensure_xbapps()
    app = xb("xbconfig.exe")
    cmd = [app, "/D"]
    p = Popen(cmd, stdout=PIPE)
    out, err = p.communicate()
    curr_settings = {}
    for l in out.splitlines():
        kv = [k.strip() for k in l.strip().decode().split(":")]
        try:
            curr_settings[kv[0]] = kv[1]
        except Exception as e:
            pass
    console_mode = curr_settings["consolemode"]
    extra_title_memory = curr_settings["extratitlememory"]
    profiling_mode = curr_settings["profilingmode"] == "on"
    secho(f"Console is in mode: {console_mode}", bold=True)
    modes = {
        "xss": {
            "ConsoleMode": "LockhartProfiling",
            "ProfilingMode": "On",
            "ExtraTitleMemory": "6048",
        },
        "xsx": {
            "ConsoleMode": "AnacondaProfiling",
            "ProfilingMode": "On"
        },
    }
    if kit_mode:
        settings = modes.get(kit_mode)
        if not settings:
            abort(f"Mode {kit_mode} not Found. Please select one of: {','.join(modes.keys())}")
        if settings["ConsoleMode"] == console_mode:
            echo(f"Console is already in mode {kit_mode}")
        else:
            echo(f"Setting console to mode {kit_mode} ({settings['ConsoleMode']})")
            cmd = [app]
            for k, v in settings.items():
                cmd.append(f"{k}={v}")
            p = Popen(cmd, stdout=PIPE)
            out, err = p.communicate()
            secho("Rebooting console. Please wait...")
            call(xb("xbreboot.exe"))

            while 1:
                sys.stdout.write(".")
                sys.stdout.flush()
                cmd = [xb("xbconnect.exe"), "/q"]
                p = Popen(cmd, stdout=PIPE, stderr=PIPE)
                p.communicate()
                if p.returncode:
                    time.sleep(1.0)
                else:
                    break
            secho(f"\nConsole mode has been set to {kit_mode}", fg="green")
            ctx.invoke(mode)
    else:
        echo("Use '-m xss' or '-m xsx' to switch modes")

def find_package(package):
    p = Path(package)
    if p.is_file():
        return p.as_posix()
    elif p.is_dir():
        files = []
        for f in p.glob("**/*.xvc"):
            if f.is_file():
                files.append(f.as_posix())
        if len(files) > 1:
            abort(f"Too many packages found: {files}")
        elif files:
            return files[0]
    abort(f"Package {package} not found")

def find_build(cl, config):
    all_builds = collect_builds()
    cl = int(cl)
    for b in all_builds[cl]:
        if b['configuration'].lower() == (config or "").lower() or len(all_builds[cl]) == 1:
            build = b
    if not build:
        abort(f"Multiple builds for {cl} found. Please specify --type=development|test")
    return build

@cli.command()
@click.option("-c", "--cl", "changelists_string", help="Comma separated list of changelists or a range [from]-[to]")
@click.option("-t", "--type", "config", default=None, help="Build configuration, select either Development or Test")
@click.pass_context
def fetch(ctx, changelists_string, config):
    """
    Fetch a build from teamcity storage to the local machine
    """
    all_builds = collect_builds()
    if not changelists_string:
        ctx.invoke(list_builds, config=config)
        changelists_string = input("Select a changelist to deploy: ")

    changelists = parse_changelists(changelists_string, config)
    secho(f"Downloading the following builds: {', '.join([str(c) for c in changelists])} in {config} configuration", bold=True)
    if (len(changelists) > 1):
        secho(f"This will require approximately {len(changelists)*20} GB space on your c:/ drive", fg="yellow")

    for i, cl in enumerate(changelists):
        build = find_build(cl, config)

        full_path = Path(build["path"])
        #echo(f"[{i+1}/{len(changelists)}] Downloading CL {cl} from {full_path}")

        target_file = temp_path / build['filename']
        if target_file.is_file():
            tz = datetime.fromtimestamp(target_file.stat().st_mtime).isoformat()
            if tz == build['timestamp']:
                secho(f"[{i+1}/{len(changelists)}] Build {target_file.name} is already in {temp_path}", fg="green")
                continue
            else:
                secho(f"[{i+1}/{len(changelists)}] Build {target_file.name} was found in {temp_path} but has the wrong timestamp. Will re-download", fg="yellow")
        secho(f"[{i+1}/{len(changelists)}] Copying file {full_path} to {temp_path}...", fg="green")
        path_to_copy = full_path.parent.as_posix()
        cmd = ["robocopy.exe", path_to_copy, temp_path, "*.xvc", "/mt:10"]
        p = call(cmd)

@cli.command()
@click.option("-c", "--cl", help="Changelist number to deploy")
@click.option("-p", "--package",  help=".xvc Package name or folder containing package, alternative to --cl")
@click.option("-t", "--type", "config", default=None, help="Build configuration, select wither Development or Test")
@click.pass_context
def deploy(ctx, cl, package, config):
    """
    Deploy a build that has already been downloaded to c:/temp/xboxbuilds
    to your xbox console
    """
    ensure_xbapps()
    xbapp = xb("xbapp.exe")
    xbconnect = xb("xbconnect.exe")

    if cl:
        echo(f"XBox found at IP {console_ip}. Deploying CL {cl}")
    else:
        echo(f"XBox found at IP {console_ip}. Deploying package {cl}")

    cmd = [xbapp, "list"]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if not not p.returncode:
        abort("No XBox console found")
    app_id = ""
    for l in out.split():
        l = l.decode()
        # try to find the build number
        if "UnknownWorldsEnter" in l and "!" not in l:
            installed_cl = l.strip().split(".")[-1].split("_")[0]
    if installed_cl:
        try:
            installed_cl = int(installed_cl)
        except Exception as e:
            installed_cl = 0
        if installed_cl == cl:
            secho(f"Changelist {cl} is already installed on xbox")
            return
    if package:
        file_path_string = find_package(package)
    else:
        file_path_string = temp_path / find_build(cl, config)['filename']
    secho(f"Installing build {file_path_string} on xbox", fg="green")
    cmd = [xbapp, "install", file_path_string]
    p = call(cmd)

@cli.command()
@click.option("-c", "--cl", "changelists_string", help="Comma separated or [from]-[to] list of changelists")
@click.option("-p", "--package",  help=".xvc Package name or folder containing package, alternative to --cl")
@click.option("-t", "--type", "config", default=None, help="Development or Test configuration (required)")
@click.option("-m", "--mode", "kit_mode", default="xss", show_default=True, help="Run as xss or xsx")
@click.option("--teamcity/--no-teamcity", default=False, help="Run as teamcity build (sets group)")
@click.option("--cameras", default="xss", help="Comma separated list of camera filters")
@click.pass_context
def phototour(ctx, changelists_string, package, config, kit_mode, teamcity, cameras):
    """
    Run a phototour from the selected changelists on the xbox console.
    Downloads the required builds to your local machine before running.
    Before running this use 'list' to see available builds
    """
    ensure_xbapps()
    ctx.invoke(mode, kit_mode=kit_mode)
    if not package:
        changelists = parse_changelists(changelists_string, config)
        secho(f"Running phototours on the following changelists: {','.join([str(c) for c in changelists])}")
        ctx.invoke(fetch, changelists_string=changelists_string, config=config)
        for cl in changelists:
            run_phototour(ctx, cl, None, config, teamcity, cameras, kit_mode)
    else:
        run_phototour(ctx, None, package, config, teamcity, cameras, kit_mode)

def run_phototour(ctx, cl, package, config, teamcity, cameras, kit_mode):
    if cl:
        secho(f"Deploying and running changelist {cl}", fg="green")
    else:
        secho(f"Deploying and running package {package}", fg="green")
    ctx.invoke(deploy, cl=cl, package=package, config=config)
    xbapp = xb("xbapp.exe")
    # get the build ID
    cmd = [xbapp, "list"]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if not not p.returncode:
        abort("No XBox console found")
    app_id = ""
    for l in out.split():
        l = l.decode()
        if "UnknownWorldsEnter" in l and "!" in l:
            app_id = l.strip()
    if not app_id:
        abort("App not found on console")
        
    computer_name = socket.gethostname()
    current_user = getpass.getuser()
    cmd = [xbapp, "launch", app_id, "-phototour", 
            f'-perftour_runner="{computer_name}/{current_user}"', 
            '-perftour_tags="personal"']
    if cameras:
        cmd.append(f'-perftour_cameras="{cameras}"')
    if teamcity:
        cmd.append(f'-perftour_group="{kit_mode.lower()}"')
    secho(f"Launching phototour with app {app_id}", fg="green")
    p = Popen(cmd, shell=True)
    out, err = p.communicate()
    done = False
    start_time = datetime.now()
    while 1:
        time.sleep(10)
        lines = get_loglines()
        lines.reverse()
        latest_timestamp = None
        for l in lines:
            if not latest_timestamp:
                latest_timestamp = get_timestamp_from_logline(l)
            if "phototour" in l.lower():
                echo(l)
                break
            if "RequestExit" in l:
                echo(l)
                done = True
        if latest_timestamp < datetime.now() - timedelta(minutes=2):
            secho(f"No loglines since {latest_timestamp.isoformat()}. Quitting", fg="yellow")
            done = True
        if done:
            break
    durr = (datetime.now() - start_time).total_seconds()
    secho(f"Phototour has finished running in {durr} sec", fg="green")

if __name__ == "__main__":
    cli()