# A partition cover approach to tokenization
In this work, we formulate tokenization as an optimization objective, show that it is NP-hard via a simple reduction from vertex cover, and propose a polynomial-time greedy algorithm **GreedTok**.
Our formulation naturally relaxes to the well-studied weighted maximum coverage problem which has a simple $(1 - 1/e)$-approximation greedy algorithm.

### GreedTok 
1. If using python wrapper
   
    a. Using pip (use the lightweight source code w/o data/notebooks):
      ```
      wget "https://github.com/PreferredAI/pcatt/archive/refs/tags/v0.13.tar.gz"
      unzip pcatt-0.13.zip -d pcatt
      cd pcatt
      pip install -r requirements.txt
      pip install .
      ```
    b. Or compile manually e.g. (have to specify links)
      ```
      c++ -O3 -Wall -shared -std=c++20 \
      -fPIC $(python3 -m pybind11 --includes) \
      -I$CONDA_PREFIX/include/ \
      -I$CONDA_PREFIX/include/tbb \
      -I$CONDA_PREFIX/include/oneapi \
      -L$CONDA_PREFIX/lib/ \
      -l tbb \
      ./pcatt/greedy_builder.cpp \
      -o ./pcatt/greedy_builder$(python3-config --extension-suffix) 
      ```
    c. import and use! Examples in [eval_tokenizer_example.ipynb](https://github.com/PreferredAI/aoatt/blob/main/eval_tokenizer_example.ipynb)
2. If using C++ files directly

    a. Install dependencies for C++ code, we use oneTBB to parallelize the code, simplest way is to use Conda or pip:
      ```
      conda install tbb-devel
      ```

    b. Compile greedy_cache.py e.g.:
      ```
      c++ -O3 -std=c++20 \
      -I$CONDA_PREFIX/include/ \
      -I$CONDA_PREFIX/include/tbb \
      -I$CONDA_PREFIX/include/oneapi \
      -L$CONDA_PREFIX/lib/ \
      -l tbb \
      pcatt/greedy_cache.cpp \
      -o pcatt/greedy.exe 
      ```
    c. Prepare inputs (refer to [cpp_inputs](https://github.com/PreferredAI/aoatt/blob/main/cpp_inputs) for examples):
      * counts: a file with '\n' delimited integers
      * words: a file with ' ' (space) delimited words
        
    d. Run compiled program (currently looks for domain inputs in fixed path under cpp_inputs/*)
        ```
         ./greedy.exe <domain> <k>
        ```
    e. Now we obtained our ranked token sequence (refer to [cpp_outputs](https://github.com/PreferredAI/aoatt/blob/main/cpp_outputs/) for examples):
      * merges: the number of covers at each step, delimited by '\n'
      * tokens: byte sequences in hex-format, delimited by '\n'

Evaluations in [eval_notebook.ipynb](https://github.com/PreferredAI/aoatt/blob/main/eval_notebook.ipynb)

### Citation
TBD
