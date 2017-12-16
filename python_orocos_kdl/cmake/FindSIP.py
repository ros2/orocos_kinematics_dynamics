# FindSIP.py
#
# Copyright (c) 2007, Simon Edwards <simon@simonzone.com>
# Redistribution and use is allowed according to the terms of the BSD license.
# For details see the accompanying COPYING-CMAKE-SCRIPTS file.
from __future__ import print_function

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
    print("sip_version:%06.0x" % sipcfg.sip_version)
    print("sip_version_str:%s" % sipcfg.sip_version_str)
    print("sip_bin:%s" % sipcfg.sip_bin)
    print("default_sip_dir:%s" % sipcfg.default_sip_dir)
    print("sip_inc_dir:%s" % sipcfg.sip_inc_dir)
else:
    print("sip_version:%06.0x" % sip.SIP_VERSION)
    print("sip_version_str:%s" % sip.SIP_VERSION_STR)
