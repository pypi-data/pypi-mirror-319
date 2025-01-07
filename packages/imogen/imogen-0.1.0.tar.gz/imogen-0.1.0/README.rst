..
  Copyright 2024 - 2025 Avram Lubkin, All Rights Reserved

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.


Overview
========

Imogen is a system image generator, primarily intended for generating cloud imaged for Linux
operating systems which employ kickstart files for automated installs.

The tool takes advantage of hard drive emulation enabled on most distribution ISO images, booting
into Anaconda to perform an automated build with a kickstart file imbedded into the image.

For now it only supports AWS, but expect more providers in the future.

This tool is still in early development, but is being used. Please report issues. PRs welcome!


Usage
=====

See the examples directory for configuration and kickstart examples.

To build a basic AMI for Rocky 9, make sure you have AWS credentials configured and run:

.. code::

    imogen -c examples/rocky-9.yaml --aws


Troubleshooting tips
====================

Probing instance
----------------

If you need to probe the system during the build, you can use a %pre script and have it log
to the console

.. code:: console

    %pre --log=/dev/tty
    ls -l /sys/class/block
    %end

My root partition isn't automatically growing
---------------------------------------------

Check the cloud-init logs. The growpart module doesn't support LVM, so you'll need to create your
own logic and run it in bootcmd
