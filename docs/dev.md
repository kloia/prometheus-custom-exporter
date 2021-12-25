
## Development

Developers need to run this command on their host. 
* Pre-commit will run automatically on git commit!

```
pip3 install pre-commit
pre-commit install
```

## Test

```
python3 -m unittest discover -s $(pwd) -v -f -p "test_*.py"
```
