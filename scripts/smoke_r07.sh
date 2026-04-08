#!/usr/bin/env bash
set -e
python -V
echo "[R-07] uruchamiam pytest (core + maszyny)"
pytest -q tests/test_machines_loader.py
echo "[R-07] OK"
