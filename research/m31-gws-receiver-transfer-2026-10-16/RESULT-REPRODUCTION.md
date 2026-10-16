# Result reproduction notes

Follow the immutable [source instructions](REPRODUCE.md) to acquire the official input bytes into a private directory and reproduce the scientific aggregates in new destinations. Do not overwrite the completed campaign. The original science and saved-review invocations are terminal. Reproduction by another researcher is distinct from repeating this campaign.

The independent reviewer is `review/numerical/review_gws.py`. Its argument schema is readable in source. From repository root, a separate reproducibility environment can supply:

```sh
python3 research/m31-gws-receiver-transfer-2026-10-16/review/numerical/review_gws.py \
  --repo REPOSITORY_ROOT \
  --static PRIVATE_STATIC_TXT --axial PRIVATE_AXIAL_TXT \
  --private-result PRIVATE_ROWS_JSON \
  --public-result research/m31-gws-receiver-transfer-2026-10-16/results/aggregate.json \
  --source-commit ffec6dccee9def5acc473cd907417d09533bc636 \
  --expected-manifest-sha256 f2e644114d1911c0c93c389c5a9e97dc899cce41a9831486f2a790815e6cd3a2 \
  --expected-private-sha256 cbf5d0ca5d31760335774a557dee8634900121dabb2406bc2b5cf4a9d607e42d
```

Run a copied reviewer directory in a separate work area because it writes REVIEW-CHECKS.json beside its script. The exact private evidence pin refers to the retained original run. New independent outputs may have different provenance bytes; do not pretend they match that identity. The source analyzer checks its own committed bytes; checkout the source commit for exact original provenance, with packaging artifacts available separately.

No stochastic seed or timing comparison exists. Python standard-library bisection and independent hyperbolic roots are documented in their respective source files. The static viewer uses the existing vendored Three.js and OrbitControls, with dependency hashes in viewer/DEPENDENCIES.json. Display QA used installed Playwright 1.62.1 and Chrome 155.0.8059.80. The QA executable and artifact directories are supplied as arguments/environment values, with no personal runtime paths published.

Serve the repository root over local HTTP to view `research/m31-gws-receiver-transfer-2026-10-16/viewer/`. The viewer checks exact aggregate SHA-256 before plotting. It never reads the private input tables or full derived rows. The existing local server on port 8876 was retained.
