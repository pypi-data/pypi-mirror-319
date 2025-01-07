python setup.py sdist bdist_wheel
pip install dist/pipcherry-0.1.0-py3-none-any.whl
python -m twine upload -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDZmNGE2YzU2LTU3YTEtNDk0Mi1hNWE0LTUyMzVjY2IxOWI0MAACKlszLCI1MzE3MmViNy05ZDdmLTRkMzUtOTNhZS03ZTdjYmQyYTBlNDkiXQAABiCdIpx_OL2XiMfhtEKbjYADZoTsUIp_LAzHu-Vm9LytQw dist/* --verbose

pip install dist/pipcherry-0.1.1-py3-none-any.whl
