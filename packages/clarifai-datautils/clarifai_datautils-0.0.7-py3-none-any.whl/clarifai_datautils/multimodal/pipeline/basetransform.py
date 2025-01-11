from typing import List


class BaseTransform:
  """Base Transform Component"""

  def __init__(self) -> None:
    pass

  def __call__(self,) -> List:
    """Transform components."""
    raise NotImplementedError()
