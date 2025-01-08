**This work builds upon the original implementation of solTg by Konstantin Britikov.**

Follow instructions in README_original.md to install dependencies. 

## Modified tgnonlin and solc

Precompiled binaries for linux are present in the ./deps folder, replace them with binaries compiled from soltgbackend repo if necessary.

## forge-std

```
forge install foundry-rs/forge-std --no-commit
```

To install forge-std.

## python

Once all dependencies are installed, run:
```
pip install .
```

This should install any python dependencies.

When I tried to run the tool on my linux system I got a version error for numpy.

```
pip install "numpy<2"
```

Fixed this error for me.

## How to run

Run the tool using the following command

```
`python3 ./solTg/RunAll.py -i <input file/dir>` -t <timeout in seconds>
```

The contract to be analysed must not be an abstract contract and its code must contain an assert in order for SolCMC to generate its CHC encoding. SolTG will notify the user if the encoding fails to generate.




