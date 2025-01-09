# Copyright (c) 2024, InfinityQ Technology, Inc.
from pathlib import Path

from titanq.tools._mps._model_from_mps import from_mps
from ..._model.model import Model


def configure_model_from_mps_file(model: Model, file_path: Path) -> None:
    """
    .. deprecated:: 0.26.0
        Use from_mps() instead.

    Configure a model with an MPS file. Set the variable vector, the
    objective matrices and the constraints.

    Parameters
    ----------
    model
        The instance of the model to configure.
    file_path
        The path to the MPS file.
    """
    from_mps(file_path, model)