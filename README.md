# lxd-image-converter
A small toolchain to generate lxd compatible images from raw cloud disk images

To build a cloud like environment with lxd, it is helpful to have cloud-init support for your images.
Unfortunately https://images.linuxcontainers.org does not have cloud-init enabled. Therefore this hacky tool exists.

First it was intended to be done by a Makefile, but it turned out easier to write an imperative script.

## Pre-built Images

Generated images are provided at https://images.nlogn.org:8443/ and can be added to your lxd instance by

    lxc remote add <alias> images.nlogn.org --public

and launch an instance e.g. with

    lxc launch <alias>:debian/8 <conatiner-name>

## Install

The best way to use this, is to create a virtual environment

    virtualenv env
    source ./env/bin/activate

Then install the dependencies

    pip install -r requirements.txt

Then you are ready to go.

### qcow2

If you plan to convert images from `.qcow2`, please install `qemu-utils`

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

## All in one

To build and import all config files you can run

    python make.py confs/
    
## Running inside a LXD container

Unfortunately, extracting images requires the tool to mount them, which requires elevated permissions.
To run this tool inside an lxd container itself, the container requires the access to the loop devices.
According to with https://github.com/lxc/lxd/issues/2980 prepare your container with

    lxc config device add <name> loop0 unix-block path=/dev/loop0
    lxc config device add <name> loop1 unix-block path=/dev/loop1
    lxc config device add <name> loop2 unix-block path=/dev/loop2
    lxc config device add <name> loop3 unix-block path=/dev/loop3
    lxc config device add <name> loop4 unix-block path=/dev/loop4
    lxc config device add <name> loop5 unix-block path=/dev/loop5
    lxc config device add <name> loop6 unix-block path=/dev/loop6
    lxc config device add <name> loop7 unix-block path=/dev/loop7
    
    lxc config device add <name> loop-control unix-char path=/dev/loop-control
    
    lxc config set <name> raw.apparmor "mount,"
    lxc config set <name> security.privileged true
    
    lxc restart <name>

## Support

So far, `.raw.tar.gz`, `.raw.xz` and `.raw` images are supportet

## Process

Here is a short description on how the lxd image is created.

- Download the image
- Unpack to get the raw image
- find the first partition inside the image
- mount the partition
- create a `tar.gz` from the rootfs
- template the `metadata.yaml` from the config file
- archive the metadata
