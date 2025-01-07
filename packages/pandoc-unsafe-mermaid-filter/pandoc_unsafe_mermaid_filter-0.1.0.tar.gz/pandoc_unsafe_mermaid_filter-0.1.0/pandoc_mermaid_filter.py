#!/usr/bin/env python

import os
import sys
import subprocess
import json

from pandocfilters import toJSONFilter, Para, Image
from pandocfilters import get_filename4code, get_caption, get_extension

# Environment variables with fallback values
MERMAID_BIN = os.path.expanduser(os.environ.get('MERMAID_BIN', 'mermaid'))
PUPPETEER_CFG = os.environ.get('PUPPETEER_CFG', None)

# Default puppeteer configuration for sandbox disable
DEFAULT_PUPPETEER_CONFIG = {
    "args": ["--no-sandbox"]
}

def no_config() -> bool:
    not os.path.isfile('puppeteer-config.json') and not PUPPETEER_CFG and not os.path.isfile('.puppeteer.json')

def mermaid(key, value, format_, _):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value

        if "mermaid" in classes:
            caption, typef, keyvals = get_caption(keyvals)

            filename = get_filename4code("mermaid", code)
            filetype = get_extension(format_, "png", html="svg", latex="png")

            src = filename + '.mmd'
            dest = filename + '.' + filetype

            if not os.path.isfile(dest):
                txt = code.encode(sys.getfilesystemencoding())
                with open(src, "wb") as f:
                    f.write(txt)

                # Create default puppeteer config if none exists
                if no_config():
                    with open('puppeteer-config.json', 'w') as f:
                        json.dump(DEFAULT_PUPPETEER_CONFIG, f, indent=2)

                # Default command to execute
                cmd = [MERMAID_BIN, "-i", src, "-o", dest]

                if PUPPETEER_CFG is not None:
                    cmd.extend(["-p", PUPPETEER_CFG])
                elif os.path.isfile('.puppeteer.json'):
                    cmd.extend(["-p", ".puppeteer.json"])
                else:
                    cmd.extend(["-p", "puppeteer-config.json"])

                subprocess.check_call(cmd)
                sys.stderr.write('Created image ' + dest + '\n')

            return Para([Image([ident, [], keyvals], caption, [dest, typef])])

def main():
    toJSONFilter(mermaid)

if __name__ == "__main__":
    main()