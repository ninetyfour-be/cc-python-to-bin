"""Noxfile."""
from dataclasses import dataclass
from pathlib import Path
import platform
import shutil
from typing import List, Optional
from zipfile import ZipFile

import nox


ENTRYPOINT = Path("src/test_client.py")  # Change this depending on the project


class NoSpecifiedTarget(Exception):
    pass


@dataclass
class Target:

    name: str
    username: str
    password: str
    path: Path

    def __post_init__(self) -> None:
        self._session : Optional[nox.Session] = None
    
    @property
    def session(self) -> Optional[nox.Session]:
        return self._session
    
    @session.setter
    def session(self, v: nox.Session) -> None:
        self._session = v

    def _guest_cmd(self, *args) -> None:
        if self.session:
            self.session.run(
                "vboxmanage",
                "guestcontrol",
                self.name,
                "--username",
                self.username,
                "--password",
                self.password,
                *args,
            )

    def start(self) -> None:
        if self.session:
            self.session.run("vboxmanage", "startvm", self.name, "--type", "gui")
            input("Press enter when the VM is ready : ")


    def copy_to(self, src_path: Path, dest_path: Path) -> None:
        self._guest_cmd("copyto", str(src_path), str(dest_path))
    
    def mkdir(self, path: Path) -> None:
        self._guest_cmd("mkdir", "--parents", str(path))
    
    def rmdir(self, path: Path) -> None:
        self._guest_cmd("rmdir", "--recursive", str(path))

    def copy_from(self, src_path: Path, dest_path: Path) -> None:
        self._guest_cmd("copyfrom", str(src_path), str(dest_path))

    def execute(self, exe: Path, cmd: List[str]) -> None:
        self._guest_cmd("run", "--exe", str(exe), "--", *cmd)

    def stop(self):
        if self.session:
            self.session.run("vboxmanage", "controlvm", self.name, "poweroff")


TARGETS = {
    "windows": Target("windows", "Ninety Four", "1234", Path("C:/Users/Ninety Four/Documents")),
    "macos": Target("macos", "ninety", "1234", Path("/Users/ninety/Documents")),
    "linux": Target("linux", "ninetyfour", "1234", Path("/home/ninetyfour/Documents")),
}


@nox.session(python=False)
def release(session: nox.Session) -> None:
    """Build a release."""
    if not session.posargs:
        raise NoSpecifiedTarget("There is no specified target platform.")
    # Create release directory
    release_path = Path("./releases")
    if not release_path.is_dir():
        release_path.mkdir(parents=True)
    release_id = -1
    # Check for last release
    for file in release_path.iterdir():
        if file.suffix == ".zip":
            release_id = max(
                release_id,
                int(file.stem.split("_")[-1].replace("rev", ""))
            )
    release_id += 1
    # Freeze the application for each target platform
    for target_name in session.posargs:
        target = TARGETS[target_name]
        target.session = session
        target.start()
        work_path = target.path / Path.cwd().stem
        target.mkdir(work_path)
        for item in ["src", "icon", "requirements.txt", "noxfile.py"]:
            target.copy_to(Path(item), work_path)
        exe_path = Path("/home/ninetyfour/.local/bin/nox")
        if target.name == "windows":
            exe_path = Path("C:/Users/Ninety Four/.pyenv/pyenv-win/shims/nox.bat")
        elif target.name == "macos":
            exe_path = Path("/Users/ninety/.local/bin/nox")            
        target.execute(
            exe_path, 
            ["nox", "--noxfile", str(work_path / "noxfile.py"), "--session", f"freeze"]
        )
        release_target_path = release_path / "latest"
        release_target_path.mkdir(parents=True, exist_ok=True)
        target.copy_from(work_path / "dist", release_target_path)
        session.run("rm", "-rf", str(release_target_path / target.name))
        (release_target_path / "dist").rename(release_target_path / target.name)
        input("Press enter when the app is tested : ")
        target.stop()
    session.run("nox", "--session", "doc")
    # Produce a zip archive of the release
    archive = ZipFile(release_path / f"{Path.cwd().stem}_rev{release_id}.zip", "w")
    for file in release_target_path.glob("**/*"):
        print(file)
        archive.write(file, file.relative_to(release_target_path))
    archive.write(Path("build/doc/ninetyfour.pdf"))
    archive.close()


@nox.session()
def freeze(session: nox.Session) -> None:
    """Build an executable."""
    icon = "icon.png"
    if platform.system() == "Windows":
        icon = "icon.ico"
    elif platform.system() == "Darwin":
        icon = "icon.icns"
    session.install("-r", "requirements.txt")
    session.install("pyinstaller")
    session.run(
        "pyinstaller",
        str(ENTRYPOINT),
        "--clean",
        "--noconfirm",
        "--icon",
        f"icon/{icon}",
        "--onefile",
        "--windowed",  # Change this depending on the project
        #"--console",  # Change this depending on the project
    )


@nox.session
def doc(session: nox.Session) -> None:
    """Build the documentation."""
    session.install("sphinx", "sphinx_click", "myst-parser", "rinohtype")
    args = session.posargs or ["rinoh"]
    session.run("sphinx-build", "-b", args[0], "docs", "build/docs")
    # Clean build
    for path in Path("build").glob("**/*[!(.pdf)]"):
        if path.is_file():
            path.unlink()
    for path in [Path("build") / p for p in {"lib", "bdist.linux-x86_64", "docs/.doctrees"}]:
        try:
            shutil.rmtree(path)
        except Exception:
            pass
