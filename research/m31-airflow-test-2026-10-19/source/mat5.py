"""Restricted MATLAB v5 real-double reader. No MATLAB code executes."""
import math
import struct
import zlib

LIMIT = 4*1024*1024

def element(b, at):
    if at+8 > len(b): raise ValueError('truncated tag')
    tag, count = struct.unpack_from('<II', b, at)
    small = tag >> 16
    if small:
        if small > 4: raise ValueError('bad small element')
        return tag & 65535, b[at+4:at+4+small], at+8
    if count > LIMIT or at+8+count > len(b): raise ValueError('element size')
    end = at+8+count
    return tag, b[at+8:end], end if tag == 15 else at+8+((count+7)//8)*8

def read(data, values=True, allow_nonfinite=False):
    if len(data)>LIMIT or len(data)<136 or data[126:128]!=b'IM':
        raise ValueError('requires bounded little endian MAT5')
    if struct.unpack_from('<H',data,124)[0]!=256: raise ValueError('MAT version')
    typ,payload,end=element(data,128)
    if end!=len(data): raise ValueError('requires single variable')
    if typ==15:
        dec=zlib.decompressobj(); inner=dec.decompress(payload,LIMIT+1)
        if len(inner)>LIMIT or not dec.eof or dec.unused_data or dec.unconsumed_tail:
            raise ValueError('compressed stream invalid or oversized')
        typ,payload,end=element(inner,0)
        if end!=len(inner): raise ValueError('trailing compressed bytes')
    if typ!=14: raise ValueError('requires matrix')
    parts=[];at=0
    while at<len(payload):
        t,p,at=element(payload,at);parts.append((t,p))
    if at!=len(payload) or len(parts)!=4: raise ValueError('requires real dense matrix')
    if parts[0][0]!=6 or len(parts[0][1])!=8: raise ValueError('flags')
    flags,nz=struct.unpack('<II',parts[0][1])
    if flags!=6 or nz!=0: raise ValueError('requires plain double class')
    if parts[1][0]!=5 or len(parts[1][1])!=8: raise ValueError('requires two dimensions')
    dims=list(struct.unpack('<ii',parts[1][1]))
    if any(d<1 or d>10000 for d in dims): raise ValueError('dimensions')
    if parts[2][0]!=1: raise ValueError('name type')
    name=parts[2][1].decode('ascii')
    if not name.isidentifier(): raise ValueError('name')
    if parts[3][0]!=9 or len(parts[3][1])!=8*math.prod(dims): raise ValueError('payload shape')
    result={'name':name,'shape':dims,'order':'column-major'}
    if values:
        v=list(struct.unpack('<'+'d'*math.prod(dims),parts[3][1]))
        if not allow_nonfinite and not all(math.isfinite(x) for x in v): raise ValueError('nonfinite values')
        result['values']=v
    return result
