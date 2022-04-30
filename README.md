# topopt

*A topology optimization attempt for RF simulations*

---
[`create.py`](https://github.com/0xCoto/topopt/blob/main/create.py) takes a three-dimensional pattern input: in this case, a 5x5x5 binary matrix ([`space`](https://github.com/0xCoto/topopt/blob/main/create.py#L51-L58)), with a resolution of 1x1x1 mm, as defined in [`block_size`](https://github.com/0xCoto/topopt/blob/main/create.py#L60-L61).

#### Default input matrix
```python
space = [
[[0,1,0,0,1], [1,0,0,1,0], [0,1,0,1,1], [0,0,0,1,1], [0,1,1,0,1]],
[[1,1,1,0,1], [0,0,0,1,0], [0,0,1,1,1], [0,0,0,1,1], [0,1,0,0,0]],
[[0,1,0,1,0], [1,1,0,0,0], [1,0,0,1,0], [0,1,1,1,0], [0,1,1,1,1]],
[[0,1,0,1,0], [0,1,0,1,1], [1,1,0,1,0], [1,0,0,1,0], [0,0,0,0,0]],
[[1,0,0,1,1], [0,1,1,0,1], [0,1,0,1,1], [0,1,1,0,1], [1,0,1,0,0]],
]
```

A cell value of `False` indicates material absence at the associated matrix index, while `True` indicates material presence.

The output is a STEP file with all the created objects included.
![image](https://user-images.githubusercontent.com/25392776/166114233-2aac0f45-aada-4aba-ac45-9d8a5019a161.png)

# Open issues

## Multi-material definition
This could be achieved by either creating multiple `space` objects, each corresponding to a unique material (and STEP or STL file), or by assigning non-binary integer/real values to the matrix.

## Binary optimization
Many algorithms have to be tested to evaluate which optimization technique performs best for this problem. A variety of optimization methods can be adapted to alternate binary values in the matrix by setting appropriate constraints, i.e. stating the linear problem in the form of:

#### _Minimize/maximize:_
`|S_ij(frequency)|`
#### _Subject to:_
**Row constraints**
```py
x11+x12+x13+x14+x15 = 1
x21+x22+x23+x24+x25 = 1
x31+x32+x33+x34+x35 = 1
x41+x42+x43+x44+x45 = 1
x51+x52+x53+x54+x55 = 1
```
**Column constraints**
```py
x11+x21+x31+x41+x51 = 1
x12+x22+x32+x42+x52 = 1
x13+x23+x33+x43+x53 = 1
x14+x24+x34+x44+x54 = 1
x15+x25+x35+x45+x55 = 1
```

## Solver API
An E/M solver API shall be made use of/crafted to be called by the optimizer to evaluate the simulated scattering parameter magnitude at the frequency of interest (objective function).
