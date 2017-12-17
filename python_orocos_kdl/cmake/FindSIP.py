# FindSIP.py
#
# Copyright (c) 2007, Simon Edwards <simon@simonzone.com>
# Redistribution and use is allowed according to the terms of the BSD license.
# For details see the accompanying COPYING-CMAKE-SCRIPTS file.
from __future__ import print_function

import os
import sys

use_sip = False
use_sipconfig = False
try:
    import sipconfig
except ImportError:
    print("could not import 'sipconfig' module, try to import 'sip' instead", file=sys.stderr)
    try:
        import sip
    except ImportError:
        print("could not import 'sip' module, exiting", file=sys.stderr)
        raise
    else:
        use_sip = True
else:
    use_sipconfig = True

if use_sipconfig:
    sipcfg = sipconfig.Configuration()
    print("sip_version:%06.0x" % sipcfg.sip_version, file=sys.stderr)
    print("sip_version_str:%s" % sipcfg.sip_version_str, file=sys.stderr)
    print("sip_bin:%s" % sipcfg.sip_bin, file=sys.stderr)
    print("default_sip_dir:%s" % sipcfg.default_sip_dir, file=sys.stderr)
    print("sip_inc_dir:%s" % sipcfg.sip_inc_dir, file=sys.stderr)
else:
    if sys.platform == "win32":
        sip_py_lib_dir = os.path.join(sys.prefix, "libs")
        sip_bin_dir = sys.exec_prefix
        sip_sip_dir = os.path.join(sys.prefix, "sip")
    else:
        import distutils.sysconfig
        lib_dir = distutils.sysconfig.get_python_lib(plat_specific=1, standard_lib=1)
        sip_py_lib_dir = os.path.join(lib_dir, "config")
        sip_bin_dir = os.path.join(sys.exec_prefix, "bin")
        sip_sip_dir = os.path.join(sys.prefix, "share/sip")
    sip_inc_dir = distutils.sysconfig.get_python_inc()
    sip_bin = os.path.join(sip_bin_dir, "sip")
    print("sip_version:%06.0x" % sip.SIP_VERSION)
    print("sip_version_str:%s" % sip.SIP_VERSION_STR)
    print("sip_bin:%s" % sip_bin)
    print("default_sip_dir:%s" % sip_sip_dir)
    print("sip_inc_dir:%s" % sip_inc_dir)
    print("sip_version:%06.0x" % sip.SIP_VERSION, file=sys.stderr)
    print("sip_version_str:%s" % sip.SIP_VERSION_STR, file=sys.stderr)
    print("sip_bin:%s" % sip_bin, file=sys.stderr)
    print("default_sip_dir:%s" % sip_sip_dir, file=sys.stderr)
    print("sip_inc_dir:%s" % sip_inc_dir, file=sys.stderr)
