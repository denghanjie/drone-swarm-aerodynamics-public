"""Bounded metadata acquisition; no archive extraction or scientific execution."""
from pathlib import Path
import datetime, hashlib, json, signal, struct, urllib.request

ROOT = Path(__file__).resolve().parent
SIZE = 2512858162
URL = 'https://zenodo.org/api/records/17457069/files/experimental_data.zip/content'
CUTOFF = datetime.datetime(2026, 10, 15, 23, tzinfo=datetime.timezone.utc)
report = {'kind': 'bounded-public-zip-index', 'url': URL, 'requests': [],
          'wholeArchiveAcquired': False, 'providerMD5Verified': False,
          'membersExtracted': False, 'scientificQualified': False}

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

def deadline(*_):
    raise TimeoutError('45-second acquisition deadline')

def get_range(start, end, name):
    assert len(report['requests']) < 2
    assert datetime.datetime.now(datetime.timezone.utc) < CUTOFF, 'launch cutoff'
    assert 0 <= start <= end < SIZE and end-start+1 <= 1048576
    item = {'start': start, 'end': end, 'bodyBytesRead': 0}
    report['requests'].append(item)
    req = urllib.request.Request(URL, headers={'Range': f'bytes={start}-{end}',
                                              'Accept-Encoding': 'identity'})
    with urllib.request.build_opener(NoRedirect()).open(req, timeout=20) as response:
        item['status'] = response.status
        item['headers'] = {k: response.headers[k] for k in
            ['Content-Range', 'Content-Length', 'Content-Type', 'ETag', 'Last-Modified']
            if k in response.headers}
        assert response.status == 206, 'range unsupported: body not read'
        assert response.headers.get('Content-Range') == f'bytes {start}-{end}/{SIZE}', 'range mismatch'
        body = response.read(end-start+2)
        item['bodyBytesRead'] = len(body)
        assert len(body) == end-start+1, 'range body length mismatch'
    (ROOT/name).write_bytes(body)
    item.update(file=name, sha256=hashlib.sha256(body).hexdigest())
    return body

signal.signal(signal.SIGALRM, deadline)
signal.alarm(45)
try:
    tail_start = SIZE-65557
    tail = get_range(tail_start, SIZE-1, 'tail.bin')
    off = tail.rfind(b'PK\x05\x06')
    assert off >= 0 and off+22 <= len(tail), 'no end record'
    _, disk, cd_disk, n_disk, n, cd_size, cd_offset, comment = struct.unpack_from('<4s4H2LH', tail, off)
    assert off+22+comment == len(tail), 'end/comment length mismatch'
    assert disk == cd_disk == 0 and n_disk == n and n != 65535, 'multidisk/ZIP64 unsupported'
    assert cd_offset != 0xffffffff and cd_size != 0xffffffff, 'ZIP64 unsupported'
    assert 0 < cd_size <= 1048576 and cd_offset+cd_size <= tail_start+off, 'directory bounds'
    if cd_offset >= tail_start:
        directory = tail[cd_offset-tail_start:cd_offset-tail_start+cd_size]
    else:
        directory = get_range(cd_offset, cd_offset+cd_size-1, 'directory.bin')
    assert len(directory) == cd_size
    pos = 0
    entries = []
    for _ in range(n):
        assert directory[pos:pos+4] == b'PK\x01\x02' and pos+46 <= len(directory), 'central signature'
        fields = struct.unpack_from('<4s6H3L5H2L', directory, pos)
        flags, method = fields[3], fields[4]
        crc, compressed, uncompressed = fields[7:10]
        name_size, extra_size, comment_size = fields[10:13]
        length = 46+name_size+extra_size+comment_size
        assert pos+length <= len(directory), 'entry bounds'
        name = directory[pos+46:pos+46+name_size].decode('utf-8' if flags & 2048 else 'cp437')
        entries.append({'name':name, 'compressedBytes':compressed, 'uncompressedBytes':uncompressed,
                        'compressionMethod':method, 'flags':flags, 'crc32':f'{crc:08x}',
                        'localHeaderOffset':fields[-1]})
        pos += length
    assert pos == len(directory), 'directory trailing bytes'
    report.update(status='index-read', entryCount=n, directoryOffset=cd_offset,
                  directoryBytes=cd_size, entries=entries)
except Exception as exc:
    report.update(status='incomplete', errorType=type(exc).__name__, error=str(exc))
finally:
    signal.alarm(0)
    report['finishedUTC'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (ROOT/'acquisition.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ['status','scientificQualified','finishedUTC']}))
