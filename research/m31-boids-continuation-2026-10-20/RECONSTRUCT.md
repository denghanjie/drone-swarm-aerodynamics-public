# Reconstruct a complete journal

Each case in results/index.json has a journal.parts array. Concatenate those exact files in listed order, without separators, to recover the logical journal.file. Verify every part size/hash/offset, then the compressed aggregate size/hash. Decompress the concatenated gzip stream (members and JSON lines may cross part boundaries); verify rawBytes and rawSha256 before interpretation. All original JSON-line bytes are preserved. Never decompress individual parts separately. No scientific execution is needed to reconstruct bytes.

The independent audit reads parts as one ordered byte stream without creating a duplicate whole journal. Failed or incomplete allocations are retained as failures and cannot be reconstructed using a nonexistent success index.
