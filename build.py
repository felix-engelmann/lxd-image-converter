import yaml
import sys
from lxdimageconverter.utils import download_file, extract_rootfs, make_meta


if __name__ == '__main__':

    with open(sys.argv[1]) as f:
        conf = yaml.safe_load(f)

    print(conf)

    packed = download_file(conf["url"])
    rootfs = extract_rootfs(packed,"%s-%s"%(conf["distribution"],conf["release"]))
    make_meta(conf)


