import iris
print(iris.__file__)
print(iris.__version__)
from pp_utils import pd
pd(iris.FUTURE)
if hasattr(iris.FUTURE, "save_split_attrs"):
    iris.FUTURE.save_split_attrs = True

from iris.cube import Cube
c
cube = Cube(
  [1],
  attributes={
    'x': 
  }
)
iris.save(cube, "tmp.nc")
