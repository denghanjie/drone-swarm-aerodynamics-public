#!/usr/bin/env python3
"""Metadata/arithmetic only: no state generation, project imports, codecs or query calls.

All values below are byte counts or cardinalities. Even object/array helpers
operate on integer sizes only; they never build a scientific record.
"""
import hashlib
import json
from pathlib import Path

MIB = 1048576
N = 1000
TERMS = 2000000
RECORDS = 22
LEAVES = 128
NODES = 255

def string_bytes(length):
    return 5 + length

def obj(**sizes):
    return 5 + sum(string_bytes(len(key.encode("utf-8"))) + size for key, size in sizes.items())

def array(count, item_bytes):
    return 5 + count * item_bytes

def words(count):
    return 5 + 8 * count

def ints(count):
    return 5 + 4 * count

def calculate():
    # Scalar number and exact binary64 word both occupy nine bytes.
    scalar = 9
    raw_row = obj(id=scalar, state=words(17))
    raw = array(N, raw_row)
    input_record = obj(drones=raw)
    prepared_row = obj(id=scalar, center=words(3), axis=words(3),
        offsets=array(4, words(3)), points=array(4, words(3)), forces=words(4),
        nativeTotal=scalar, nativeBeta=scalar, nativeNu=words(4))
    prepared = array(N, prepared_row)
    coefficients = obj(offsets=ints(4*N+1), sourceIndices=ints(TERMS),
        K=words(TERMS), a=words(TERMS))
    rotor = obj(alpha=scalar, x=scalar, T=scalar)
    solution = array(N, obj(id=scalar, y=scalar, rotors=array(4, rotor)))
    loads = array(N, obj(id=scalar, rotor=words(4), collective=scalar,
        worldForce=words(3), worldMoment=words(3)))
    # Full per-native reserve covers all fields other than the five tensors
    # above and tree: ids, constants, diagnostics, timing, recordMeta, hashes,
    # status/model/method, consumption, auditTiming and framing.
    native_small = 256*1024
    native_f = raw + prepared + coefficients + solution + loads + native_small

    # Overcount every node as a leaf carrying eight members, and every
    # dictionary slot as a distinct full list of all 128 leaves.
    tree_node = obj(id=scalar, min=words(3), max=words(3), left=scalar,
        right=scalar, members=ints(8))
    tree_nodes = array(NODES, tree_node)
    dictionary = array(N, ints(LEAVES))
    culls = N*LEAVES
    # A possible null in partial leavesRefs would force generic numeric
    # array encoding; nine bytes/receiver also bounds that case.
    tree_columns = ints(N)+ints(N+1)+ints(culls)+words(culls)+array(N,scalar)
    gathered = array(N, 58+8*((N+63)//64))
    tree_small = 64*1024  # base keys, canonicalIds, scalar/counter metadata
    tree = tree_nodes+dictionary+tree_columns+gathered+tree_small
    native_h = native_f + tree

    control_row = obj(id=scalar, stateWords=words(17), neighborIds=ints(N),
        desiredVelocityWords=words(3), target=obj(vxWord=scalar,vyWord=scalar,zWord=scalar,yawWord=scalar),
        commandsWords=words(4), saturated=1, desiredQuaternionWords=words(4))
    controller = array(N,control_row)+16*1024
    consumed = obj(rotorWords=words(4),collectiveWord=scalar,
        worldForceWords=words(3),worldMomentWords=words(3))
    derivative_row = obj(id=scalar, rawStateWords=words(17), stateWords=words(17),
        normSquareWord=scalar,normWord=scalar,commandsWords=words(4),
        nominalMotorWords=words(4),consumed=consumed,bodyArmWords=words(3),
        totalBodyWords=words(3),nominalYawWord=scalar,gyroWords=words(3),derivativeWords=words(17))
    stage = array(N,derivative_row)+2*input_record+array(N,words(4))+64*1024
    initial = input_record+16*1024
    rows = {
        "source":64*1024,"factories":16*1024,"wiring_control_12":12*64*1024,
        "initial":initial,"controller":controller,"native_F":native_f,
        "native_H0":native_h,"native_H":native_h,"stage":stage,
        "case_summary":16*1024,"driver_summary":128*1024,
    }
    # At most32 top-level fields, each key <=64UTF8 bytes; field header
    # <=256B. A <=96MiB body gives <=96+32 chunk refs, <=320B/ref.
    descriptor_each = 256+32*256+(96+32)*320
    descriptors = RECORDS*descriptor_each
    binary = sum(rows.values())
    evidence = binary+descriptors
    combined = evidence+64*MIB+30*MIB+2*MIB
    return {"schema":"m31-state1000-storage-bound-v1",
        "scope":"cold-complete-success-evidence-no-sharing",
        "n":N,"nativeCalls":3,"positiveTermCapUnchanged":TERMS,"recordCount":RECORDS,
        "coefficientRawPayloadPerCallBytes":20*TERMS+4*(4*N+1),
        "coefficientFramedPerCallBytes":coefficients,"treePerCallBytes":tree,
        "rawRowBytes":raw_row,"preparedRowBytes":prepared_row,
        "controllerRowBytes":control_row,"derivativeRowBytes":derivative_row,
        "recordBodyBoundsBytes":rows,"bodyUpperBoundBytes":binary,
        "descriptorPerRecordUpperBoundBytes":descriptor_each,
        "descriptorTotalUpperBoundBytes":descriptors,"evidenceUpperBoundBytes":evidence,
        "evidenceLimitBytes":160*MIB,"evidenceHeadroomBytes":160*MIB-evidence,
        "privateAllowanceBytes":64*MIB,"downstreamAllowanceBytes":30*MIB,
        "closureAllowanceBytes":2*MIB,"combinedUpperBoundBytes":combined,
        "combinedLimitBytes":256*MIB,"combinedHeadroomBytes":256*MIB-combined,
        "admitted":evidence<=160*MIB and combined<=256*MIB,
        "failureCaptureGuaranteedComplete":False}

def source_pins():
    root=Path(__file__).resolve().parents[3]
    package="research/m31-native-tree-state1000-2026-10-17/"
    paths=[package+"source/"+name for name in ["browser.js","browser-driver.cjs",
        "browser-adapter.cjs","tree.cjs","layout.cjs","native-tree.cjs",
        "transport.cjs","transport-store.cjs","science-config.json","storage-bound.py"]]
    paths += ["research/m31-native-fresh-transfer-2026-10-17/source/"+name for name in [
        "native-load.cjs","vendor/kernel.cjs","vendor/lean-anchor.cjs","vendor/anchor-kernel.cjs",
        "vendor/generation/milestone-31-source/grid.cjs"]]
    pins=[]
    for rel in paths:
        content=(root/rel).read_bytes()
        pins.append({"path":rel,"bytes":len(content),"sha256":hashlib.sha256(content).hexdigest()})
    return pins

if __name__ == "__main__":
    answer=calculate()
    answer["sourcePins"]=source_pins()
    print(json.dumps(answer,indent=2,sort_keys=True))
