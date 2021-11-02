import sys
import os
import subprocess
import platform

platform_dict = {}
platform_dict["Darwin"] = "OSX"

sys_n_arch = platform.platform()
sys_n_arch = sys_n_arch.split("-")
system, arch = sys_n_arch[0], sys_n_arch[2]
if system in platform_dict:
    system = platform_dict[system]

print("system: {}".format(system))

version_info = subprocess.check_output("freecadcmd --version", shell=True)
version_info = version_info.decode("utf-8").split(" ")
dev_version = version_info[1]
revision = version_info[3]
revision = revision.rstrip("\n")

if system == "OSX":
    import jinja2
    osx_directory = os.path.join(os.path.dirname(__file__), "..", "osx")
    print("osx directory: {}".format(osx_directory))
    with open(os.path.join(osx_directory, "Info.plist.template")) as template_file:
        template_str = template_file.read()
    template = jinja2.Template(template_str)
    rendered_str = template.render(FREECAD_VERSION="{}-{}".format(dev_version, revision), 
                                   APPLICATION_MENU_NAME="FreeCAD-{}-{}".format(dev_version, revision))
    with open(os.path.join(osx_directory, "APP", "FreeCAD.app", "Contents", "Info.plist"), "w") as rendered_file:
        rendered_file.write(rendered_str)


if os.environ["DEPLOY_RELEASE"] == "weekly-builds":
    dev_version = "weekly-builds"

if system == "OSX":
    print("FreeCAD_{}-{}-{}-{}-conda".format(dev_version, revision, system, arch))
elif system == "Linux":
    print("FreeCAD_{}-{}-{}-Conda_glibc2.12-x86_64".format(dev_version, revision, system))
