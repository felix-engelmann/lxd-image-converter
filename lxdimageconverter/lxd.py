import subprocess

def lxd_import_image(meta,root, alias):
    subprocess.run(["lxc", "image", "import", meta, root, "--public", "--alias", alias])