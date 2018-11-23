from glob import glob
import sys, os
import yaml
from lxdimageconverter.utils import download_file, extract_rootfs, make_meta
from lxdimageconverter.lxd import lxd_import_image
from lxdimageconverter.conf import IMAGE_DIR

if __name__ == '__main__':

    for file in glob(sys.argv[1]+"/*"):
        with open(file) as f:
            conf = yaml.safe_load(f)

        print(conf)

        packed = download_file(conf["url"])
        rootfs = extract_rootfs(packed, "%s-%s" % (conf["distribution"], conf["release"]))
        make_meta(conf)

        lxd_import_image(os.path.join(IMAGE_DIR,"%s-%s-metadata.tar.gz" % (conf["distribution"], conf["release"])),
                         os.path.join(IMAGE_DIR, "%s-%s-rootfs.tar.gz" % (conf["distribution"], conf["release"])),
                         "%s/%s" % (conf["distribution"], conf["release"]))

