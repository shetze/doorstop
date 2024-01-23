# SPDX-License-Identifier: LGPL-3.0-only

"""Finding external references."""

import linecache
import os
import re

from doorstop import common, settings
from doorstop.common import DoorstopError, DoorstopWarning

log = common.logger(__name__)


class ReferenceFinder:
    """Finds files referenced from an Item."""

    @staticmethod
    def find_ref(ref, tree, item_path):
        """Get the external file reference and line number.

        :raises: :class:`~doorstop.common.DoorstopWarning` when no
            reference is found

        :return: relative path to file or None (when no reference
            set),
            line number (when found in file) or None (when found as
            filename) or None (when no reference set)

        """

        # Search for the external reference
        log.debug("searching for ref '{}'...".format(ref))
        pattern = r"(\b|\W){}(\b|\W)".format(re.escape(ref))
        log.trace("regex: {}".format(pattern))  # type: ignore
        regex = re.compile(pattern)
        for path, filename, relpath in tree.vcs.paths:
            # Skip the item's file while searching
            if path == item_path:
                continue
            # Check for a matching filename
            if filename == ref:
                return relpath, None
            # Skip extensions that should not be considered text
            if os.path.splitext(filename)[-1] in settings.SKIP_EXTS:
                continue
            # Search for the reference in the file
            try:
                lines = linecache.getlines(path)
            except (SyntaxError, UnicodeDecodeError):
                log.trace("unable to read lines from: {}".format(path))  # type: ignore
                continue
            for lineno, line in enumerate(lines, start=1):
                if regex.search(line):
                    log.debug("found ref: {}".format(relpath))
                    return relpath, lineno

        log.debug("external reference not found: {}".format(ref))
        return '', ''

    @staticmethod
    def find_file_reference(ref_path, root, tree, item_path, keyword=None):
        """Find the external file reference.

        :raises: :class:`~doorstop.common.DoorstopWarning` when no
            reference is found

        :return: Tuple (ref_path, line) when reference is found

        """

        log.debug("searching for ref '{}'...".format(ref_path))
        ref_full_path = os.path.normpath(os.path.join(root, ref_path))

        for path, _filename, relpath in tree.vcs.paths:
            # Skip the item's file while searching
            if path == item_path:
                continue
            if path == ref_full_path:
                if keyword is None:
                    return relpath, None

                # Search for the reference in the file
                try:
                    lines = linecache.getlines(path)
                except SyntaxError:
                    log.trace("unable to read lines from: {}".format(path))  # type: ignore
                    continue

                log.debug("searching for ref '{}'...".format(keyword))
                pattern = r"(\b|\W){}(\b|\W)".format(re.escape(keyword))
                log.trace("regex: {}".format(pattern))  # type: ignore
                regex = re.compile(pattern)
                for lineno, line in enumerate(lines, start=1):
                    if regex.search(line):
                        log.debug("found ref: {}".format(relpath))
                        return relpath, lineno

        log.debug("external reference not found: {}".format(ref_path))
        return '', ''

    @staticmethod
    def find_pattern_reference(pattern, root, tree, item_path, keyword):
        """Find an external reference based on a search regex pattern.

        :raises: :class:`~doorstop.common.DoorstopWarning` when no
            reference is found

        :return: List of tuples [(ref_path1, line), (ref_path2, line), ... ]
            when references are found

        """

        log.debug("searching for pattern '{}'...".format(pattern))

        if keyword == None :
            msg = "find_pattern_reference without keyword: {}".format(pattern)
            raise DoorstopError(msg)

        reflist = []

        rex = re.compile(pattern)
        for path, _filename, relpath in tree.vcs.paths:
            # Skip the item's file while searching
            if path == item_path:
                continue
            # if re.match(".*\.md", path):
            log.debug("check ref in '{}'...".format(path))
            if rex.match(path):
                log.debug("got ref in '{}'...".format(path))

                # Search for the reference in the file
                try:
                    lines = linecache.getlines(path)
                except SyntaxError:
                    log.trace("unable to read lines from: {}".format(path))  # type: ignore
                    continue

                log.debug("searching pattern for keyword '{}'...".format(re.escape(keyword)))
                pattern = r"(\b|\W){}(\b|\W)".format(re.escape(keyword))
                log.trace("regex: {}".format(pattern))  # type: ignore
                regex = re.compile(pattern)
                for lineno, line in enumerate(lines, start=1):
                    if regex.search(line):
                        log.debug("found ref: {}".format(relpath))
                        reflist.append( (relpath, lineno) )

        if reflist :
            return reflist

        log.debug("external pattern reference not found: {}".format(keyword))
        return '', ''
