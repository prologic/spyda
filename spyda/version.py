# Package:  version
# Date:     12th October 2013
# Author:   James Mills, j dot mills at griffith dot edu dot au

"""Version Module

So we only have to maintain version information in one place!
"""

version_info = (0, 0, 3, "dev")  # (major, minor, patch, dev?)
version = ".".join(map(str, version_info))
