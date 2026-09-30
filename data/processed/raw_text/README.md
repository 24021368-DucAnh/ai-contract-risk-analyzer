# Raw contract text for offsets

The six `.txt` files were extracted from the matching files in
`data/raw/contracts/` using `scripts/extract_raw_text.ps1` and Microsoft Word
in read-only mode. The script converts Word paragraph returns to `\n`, table
cell markers and vertical tabs to spaces, removes trailing line whitespace,
and writes UTF-8 without a BOM. Git enforces LF endings on these files.
No clause annotation was inserted into these files.

Offsets in `clauses_v04.csv` refer to these exact committed text files. They
are Python character indices and use half-open ranges `[start_offset, end_offset)`.
The raw contract files remain unchanged. The extraction inputs have these
SHA-256 digests:

| Source | SHA-256 |
| --- | --- |
| HDLD001.doc | `59688a671b0f954e890d2724b1b5f3ba7d611e6f3a3447efc6eedf8fc4af94c5` |
| HDLD002.doc | `c1a54e74c14b093376c120bf39100e1bbc3c10e2e233f6e9390fccba71dcb1d5` |
| HDLD003.doc | `8f4fcafaa3867d5dbab7b013c595dc13f086a4af9fb505cb3da820c125ac0f3d` |
| HDLD004.docx | `3bc72c33865a5bb206df0d2a6b8a881154cd70aee5c6c4d85f5462742c6a1537` |
| HDLD005.docx | `d3653d3cea277db3cc7c82fee0461a26569d1a3d0c3a135004b43c316dac0f36` |
| HDLD006.docx | `5d42319b1d4459936524dd9f4c615084377d0e2c728b81771aee8cad7dbeaa34` |
