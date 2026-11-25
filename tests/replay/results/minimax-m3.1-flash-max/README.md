# MiniMax M3.1 Flash max-effort blind review results

- 6 cases × 2 review groups = 12 final valid outputs.
- Model: `minimax/MiniMax-M3.1-Flash`; effort: `max`; MCode CLI 0.7.2.
- `A/` contains standard design reviews; `B/` contains Goal Spec pre-execution gate reviews.
- `A/C03.md` is the successful retry. The first attempt failed only because `--max-steps 1` was insufficient; see `attempts/A/C03.initial-failure.log` and `attempts/A/C03.retry.log`.
- `run-manifest.json` records every initial attempt and the retry.
- `runner.py` and `retry_C03.py` preserve the prompts and execution parameters.
- Raw model outputs are unedited. The comparative assessment is in `../../mcode-blind-review-report.md`.

Each review was a separate `mcode exec` process with a separate empty working directory and only its case text supplied as input. The answer key and other review outputs were not supplied.
