# lxd-image-builder
A small toolchain to generate lxd compatible images from raw cloud disk images

To build a cloud like environment with lxd, it is helpful to have cloud-init support for your images.
Unfortunately https://images.linuxcontainers.org does not have cloud-init enabled. Therefore this hacky tool exists.

First it was intended to be done by a Makefile, but it turned out easier to write an imperative script.

## Install

The best way to use this, is to create a virtual environment

    virtualenv env
    source ./env/bin/activate

Then install the dependencies

    pip install -r requirements.txt

Then you are ready to go.

## Usage

There are config files in the `confs` subfolder. Each `yaml` file has to container the following parameters:

| parameter | description |
|------|----|
|url | source of the original filesystem image, is has to have cloud-init installed. |
|distribution| lxd variable distribution |
| release | lxd variable release |
| description | lxd variable description |
| arch | destination architecture |

After configuring it, the new image can be created by e.g.

    python build.py confs/centos7.yml

As the image has to be mounted, root privileges will be required via sudo.

There will be two `tar` archives in the images folder. You can import them in to lxd via:

    sudo lxc image import <...-metadata.tar.gz> <...-rootfs.tar.gz>

## Support

So far, `.raw.tar.gz` and `.raw` images are supportet

## Process

Here is a short description on how the lxd image is created.

- Download the image
- Unpack to get the raw image
- find the first partition inside the image
- mount the partition
- create a `tar.gz` from the rootfs
- template the `metadata.yaml` from the config file
- archive the metadata
