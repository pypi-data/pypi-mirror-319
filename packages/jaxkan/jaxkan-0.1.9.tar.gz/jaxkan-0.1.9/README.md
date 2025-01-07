# jaxKAN

A JAX implementation of the original Kolmogorov-Arnold Networks (KANs), using the Flax and Optax frameworks for neural networks and optimization, respectively. Our adaptation is based on the original [pykan](https://github.com/KindXiaoming/pykan), however we also included a built-in grid extension routine, which does not simply perform an adaptation of the grid based on the inputs, but also extends its size.


## Installation

`jaxKAN` is available as a PyPI package. For installation, simply run

```
pip3 install jaxkan
```

The default installation requires `jax[cpu]`, but there is also a `gpu` version which will install `jax[cuda12]` as a dependency.


## Why not more efficient?

Despite their overall potential in the Deep Learning field, the authors of KANs emphasized their performance when it comes to scientific computing, in tasks such as Symbolic Regression or solving PDEs. This is why we put emphasis on preserving their original form, albeit less computationally efficient, as it allows the user to utilize the full regularization terms presented in the [arXiv pre-print](https://arxiv.org/abs/2404.19756) and not the "mock" regularization terms presented, for instance, in the [efficient-kan](https://github.com/Blealtan/efficient-kan/tree/master) implementation.


## Citation

If you utilized `jaxKAN` for your own academic work, please consider using the following citation, which is the paper introducing the framework:

```
@article{10763509,
      author = {Rigas, Spyros and Papachristou, Michalis and Papadopoulos, Theofilos and Anagnostopoulos, Fotios and Alexandridis, Georgios},
      journal = {IEEE Access}, 
      title = {Adaptive Training of Grid-Dependent Physics-Informed Kolmogorov-Arnold Networks}, 
      year = {2024},
      volume = {12},
      pages = {176982-176998},
      doi = {10.1109/ACCESS.2024.3504962}
}
```
