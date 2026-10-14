"""Exact-pair reservation, not a filesystem snapshot. See SOURCE-LEDGER.json.
PY-WALK/PY-SCANDIR: enumeration is not a snapshot; errors must propagate.
This implementation uses explicit listdir recursion and fresh lstat visits.
"""
import os
import stat
from pathlib import Path


class Rejected(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def require(ok, code):
    if not ok:
        raise Rejected(code)


class IO:
    """Narrow metadata seam. Driver may inject only declared negative faults."""
    def __init__(self, charge=lambda: None):
        self.charge = charge
        self.stats = []
        self.lists = []

    def lstat(self, path):
        self.charge()
        self.stats.append(str(path))
        return os.lstat(path)

    def listdir(self, path):
        self.charge()
        self.lists.append(str(path))
        return os.listdir(path)


def register(root, output, cap, io):
    root = Path(root)
    require(root.is_absolute() and root == Path(os.path.normpath(root)), 'REGISTRATION_PATH')
    require(type(cap) is int and cap > 0, 'REGISTRATION_CAP')
    require(isinstance(output, str) and output and all(p not in ('', '.', '..') for p in output.split('/'))
            and not output.startswith('/'), 'REGISTRATION_PATH')
    # Validate every ancestor with lstat, never resolve a symlink into acceptance.
    for path in reversed((root / output, *(root / output).parents)):
        s = io.lstat(path)
        require(stat.S_ISDIR(s.st_mode), 'REGISTRATION_ANCESTOR')
    return root, (root / output / 'current-context.json', root / output / 'current-context.next.json'), cap


def enumerate_names(reg, io):
    root, slots, _ = reg
    names = []
    def visit(directory):
        try:
            listed = sorted(io.listdir(directory))
        except OSError as exc:
            raise Rejected('CENSUS_ENUMERATION_ERROR') from exc
        for name in listed:
            p = directory / name
            if p in slots:
                # Trusted writer prerequisite: slots are ordinary bounded files.
                # No live lookup of either transient pathname, even for type.
                names.append(p)
                continue
            try:
                s = io.lstat(p)
            except FileNotFoundError as exc:
                raise Rejected('CENSUS_UNRELATED_MISSING') from exc
            except OSError as exc:
                raise Rejected('CENSUS_METADATA_ERROR') from exc
            if stat.S_ISDIR(s.st_mode):
                visit(p)
            else:
                require(stat.S_ISREG(s.st_mode), 'CENSUS_TYPE')
                require(s.st_nlink == 1, 'CENSUS_LINK_COUNT')
                names.append(p)
    visit(root)
    return sorted(names)


def ordinary_stat(p, io):
    try:
        s = io.lstat(p)
    except FileNotFoundError as exc:
        raise Rejected('CENSUS_UNRELATED_MISSING') from exc
    except OSError as exc:
        raise Rejected('CENSUS_METADATA_ERROR') from exc
    require(stat.S_ISREG(s.st_mode), 'CENSUS_TYPE')
    require(s.st_nlink == 1, 'CENSUS_LINK_COUNT')
    return s.st_size


def live(reg, io, hook=lambda stage, path: None, required=()):
    root, slots, cap = reg
    names = enumerate_names(reg, io)
    for name in required:
        require(root / name in names, 'CENSUS_REQUIRED_MISSING')
    hook('after_enumeration', None)
    ordinary = 0
    for p in names:
        hook('before_visit', p)
        if p not in slots:
            ordinary += ordinary_stat(p, io)
    return dict(ordinary_observed_bytes=ordinary, checkpoint_reserved_bytes=2 * cap,
                live_accounted_bytes=ordinary + 2 * cap, exact_snapshot=False)


def legacy(reg, io, hook):
    """Fair control: same enumeration, visits, ordinary checks; no slot exemption.
    Reproduces enumerate-then-lstat, not an imported predecessor executable.
    """
    names = enumerate_names(reg, io)
    hook('after_enumeration', None)
    total = 0
    for p in names:
        hook('before_visit', p)
        # Deliberately preserve the raw missing-name exception for the control.
        s = io.lstat(p)
        require(stat.S_ISREG(s.st_mode) and s.st_nlink == 1, 'LEGACY_TYPE')
        total += s.st_size
    return total


def quiescent(reg, io, *, writer_stopped, publication_occurred):
    root, slots, cap = reg
    require(writer_stopped is True, 'CHECKPOINT_WRITER_ACTIVE')
    actual, checks = 0, []
    # Validate both slots before ordinary traversal can exclude a directory.
    for index, p in enumerate(slots):
        try:
            s = io.lstat(p)
        except FileNotFoundError:
            require(index != 0 or not publication_occurred, 'CHECKPOINT_REQUIRED_MISSING')
            checks.append('absent')
            continue
        except OSError as exc:
            raise Rejected('CHECKPOINT_METADATA_ERROR') from exc
        require(stat.S_ISREG(s.st_mode), 'CHECKPOINT_TYPE')
        require(s.st_nlink == 1, 'CHECKPOINT_LINK_COUNT')
        require(0 <= s.st_size <= cap, 'CHECKPOINT_SIZE')
        actual += s.st_size
        checks.append('regular-single-link-within-cap')
    ordinary = sum(ordinary_stat(p, io) for p in enumerate_names(reg, io) if p not in slots)
    return dict(ordinary_observed_bytes=ordinary, checkpoint_actual_bytes=actual,
                actual_total_bytes=ordinary + actual, checkpoint_reserved_bytes=2 * cap,
                exact_snapshot=True, slot_checks=checks, writer_stopped=True,
                publication_occurred=publication_occurred)


def guarded_write(reg, slot, data, write):
    require(slot in reg[1], 'CHECKPOINT_WRITE_PATH')
    require(len(data) <= reg[2], 'CHECKPOINT_WRITE_SIZE')
    return write(slot, data)
