#
# Copyright 2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from typing import Any, cast, List, Optional

import numpy
import pandas as pd
import trafaret as t
from typing_extensions import Self

from datarobot.enums import DEFAULT_MAX_WAIT, ENTITY_TYPES, INSIGHTS_SOURCES
from datarobot.insights.base import CsvSupportedInsight
from datarobot.models import StatusCheckJob


class ShapMatrix(CsvSupportedInsight):
    """Class for SHAP Matrix calculations. Use the standard methods of BaseInsight to compute
    and retrieve: compute, create, list, get.
    """

    INSIGHT_NAME = "shapMatrix"
    INSIGHT_DATA = {
        t.Key("index"): t.List(t.Int()),
        t.Key("link_function"): t.String(),
        t.Key("base_value"): t.Float(),
        t.Key("colnames"): t.List(t.String()),
        t.Key("matrix"): t.List(t.List(t.Or(t.Int(), t.Float()))),
    }

    @property
    def matrix(self) -> Any:  # numpy.types.NDArray is not compatible with sphinx docs.
        """SHAP matrix values."""
        return numpy.array(self.data["matrix"])

    @property
    def base_value(self) -> float:
        """SHAP base value for the matrix values"""
        return cast(float, self.data["base_value"])

    @property
    def columns(self) -> List[str]:
        """List of columns associated with the SHAP matrix"""
        return cast(List[str], self.data["colnames"])

    @property
    def link_function(self) -> str:
        """Link function used to generate the SHAP matrix"""
        return cast(str, self.data["link_function"])

    @classmethod
    def compute(
        cls,
        entity_id: str,
        source: str = INSIGHTS_SOURCES.VALIDATION,
        data_slice_id: Optional[str] = None,
        external_dataset_id: Optional[str] = None,
        entity_type: Optional[ENTITY_TYPES] = ENTITY_TYPES.DATAROBOT_MODEL,
        quick_compute: Optional[bool] = None,
        **kwargs: Any,
    ) -> StatusCheckJob:
        __doc__ = super().compute.__doc__  # noqa pylint: disable=unused-variable
        return super().compute(
            entity_id=entity_id,
            source=source,
            data_slice_id=data_slice_id,
            external_dataset_id=external_dataset_id,
            entity_type=entity_type,
            quick_compute=quick_compute,
            **kwargs,
        )

    @classmethod
    def create(
        cls,
        entity_id: str,
        source: str = INSIGHTS_SOURCES.VALIDATION,
        data_slice_id: Optional[str] = None,
        external_dataset_id: Optional[str] = None,
        entity_type: Optional[ENTITY_TYPES] = ENTITY_TYPES.DATAROBOT_MODEL,
        quick_compute: Optional[bool] = None,
        max_wait: Optional[int] = DEFAULT_MAX_WAIT,
        **kwargs: Any,
    ) -> Self:
        __doc__ = super().create.__doc__  # noqa pylint: disable=unused-variable
        return super().create(
            entity_id=entity_id,
            source=source,
            data_slice_id=data_slice_id,
            external_dataset_id=external_dataset_id,
            entity_type=entity_type,
            quick_compute=quick_compute,
            max_wait=max_wait,
            **kwargs,
        )

    @classmethod
    def list(cls, entity_id: str) -> List[Self]:
        __doc__ = super().list.__doc__  # noqa pylint: disable=unused-variable
        return super().list(entity_id=entity_id)

    @classmethod
    def get(
        cls,
        entity_id: str,
        source: str = INSIGHTS_SOURCES.VALIDATION,
        quick_compute: Optional[bool] = None,
        **kwargs: Any,
    ) -> Self:
        __doc__ = super().get.__doc__  # noqa pylint: disable=unused-variable
        return super().get(
            entity_id=entity_id, source=source, quick_compute=quick_compute, **kwargs
        )

    @classmethod
    def get_as_csv(cls, entity_id: str, **kwargs: Any) -> str:
        __doc__ = super().get_as_csv.__doc__  # noqa pylint: disable=unused-variable
        return super().get_as_csv(entity_id=entity_id, **kwargs)

    @classmethod
    def get_as_dataframe(cls, entity_id: str, **kwargs: Any) -> pd.DataFrame:
        __doc__ = super().get_as_dataframe.__doc__  # noqa pylint: disable=unused-variable
        return super().get_as_dataframe(entity_id=entity_id, **kwargs)
