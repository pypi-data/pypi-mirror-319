import os
import shutil
import stat
import sysconfig
from pathlib import Path
from subprocess import check_call

from cffi import FFI
from git import Repo


def envlist(name: str) -> list[str]:
    value = os.environ.get(name, None)
    if value is None:
        return []
    return value.split(":")


def uname():
    if os.name == "nt":
        return "Windows"
    return os.uname().sysname


def rmtree(x: Path):
    # https://stackoverflow.com/a/12990113
    def redo_with_write(redo_func, path, err):
        os.chmod(path, stat.S_IWRITE)
        redo_func(path)

    if x.exists():
        shutil.rmtree(x, onerror=redo_with_write)


def build_and_install(root: Path, prefix: str, git_url: str, dst_dir: str):
    git_dir = root / ".gitdir"

    os.makedirs(git_dir, exist_ok=True)
    rmtree(git_dir / dst_dir)
    Repo.clone_from(git_url, git_dir / dst_dir, depth=1)

    rmtree(root / dst_dir)
    shutil.move(git_dir / dst_dir, root / dst_dir)

    env = os.environ.copy()
    env["C_INCLUDE_PATH"] = ":".join(envlist("C_INCLUDE_PATH") + [f"{prefix}/include"])
    env["LIBRARY_PATH"] = ":".join(envlist("LIBRARY_PATH") + [f"{prefix}/lib"])
    env["CFLAGS"] = "-std=c11 -O3 -fPIC"
    env["PREFIX"] = prefix

    if uname() == "Darwin" and "MACOSX_DEPLOYMENT_TARGET" not in env:
        target = sysconfig.get_config_var("MACOSX_DEPLOYMENT_TARGET")
        env["MACOSX_DEPLOYMENT_TARGET"] = target

    check_call(["make"], cwd=root / dst_dir, env=env)
    check_call(["make", "install"], cwd=root / dst_dir, env=env)


if __name__ == "__main__":
    CWD = Path(".").resolve()
    TMP = CWD / ".build_ext"
    PKG = CWD / "liknorm"

    url = "https://github.com/limix/liknorm.git"
    build_and_install(TMP, str(PKG), url, "liknorm")

    ffibuilder = FFI()

    interface_c = open(PKG / "interface.c", "r").read()
    ffibuilder.cdef(open(PKG / "interface.h", "r").read())
    ffibuilder.set_source(
        "liknorm._cffi",
        interface_c,
        language="c",
        libraries=["liknorm"],
        library_dirs=[str(PKG / "lib")],
        include_dirs=[str(PKG / "include")],
    )

    ffibuilder.compile(verbose=True)
