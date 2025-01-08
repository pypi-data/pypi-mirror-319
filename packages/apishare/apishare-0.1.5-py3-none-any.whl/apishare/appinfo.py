#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""--------------------------------------------------------------------------
@FileName:		appinfo.py
@Author:		Chen GangQiang
@Version:		v1.0.0
@CreationDate:	2024/12/20 09:10
@Update Date:	2024/12/20 09:10
@Description:	
@History:
 <author>        <time>         <version>   <desc>
 ChenGangQiang  2024/12/20 09:10 1.0.0       build this module
-----------------------------------------------------------------------------
* Copyright @ 陈钢强 2024. All rights reserved.
--------------------------------------------------------------------------"""

# standard library import
from collections import namedtuple

# application version;
# the release level can be...
# 'beta' : changes are being implemented or were
#       just implemented, but not enough tests
#       were performed yet;
# 'release_candidate' : can be released, should not
#       be used in production, though;
# 'stable' : can be used in production; bugs,
#       if existent, are considered tolerable;

AppVersion = namedtuple("AppVersion", "major minor micro release_level")

APP_VERSION = AppVersion(0, 1, 5, "release_candidate")

# titles for the application
TITLE = "apishare"

APP_NAME = "apishare"

# used to name directories related to the app, like the config and log folders;
# it is important in case the title ever uses a name with characters not supported by any major operating system;
APP_DIR_NAME = "apishare"
ORG_DIR_NAME = 'Niututu'


# custom title formats:
# Result: 'Nodezator 1.5.3 (release_candidate)'
FULL_TITLE = "{} {} ({})".format(
    TITLE, ".".join(str(i) for i in APP_VERSION[:3]), APP_VERSION[3]
)
# result: 'apishare 1.5.3'
NO_RELEASE_LEVEL_FULL_TITLE = "{} {}".format(
    TITLE,
    ".".join(str(i) for i in APP_VERSION[:3]),
)

# Website url
WEBSITE_URL = "https://wwww.apishare.cn"