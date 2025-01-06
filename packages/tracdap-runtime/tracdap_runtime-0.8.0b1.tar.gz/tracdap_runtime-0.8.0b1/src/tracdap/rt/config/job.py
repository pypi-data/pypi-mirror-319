# Code generated by TRAC

import typing as _tp  # noqa
import dataclasses as _dc  # noqa
import enum as _enum  # noqa

import tracdap.rt.metadata as metadata



@_dc.dataclass
class JobConfig:

    jobId: "metadata.TagHeader" = _dc.field(default_factory=lambda: metadata.TagHeader())

    job: "metadata.JobDefinition" = _dc.field(default_factory=lambda: metadata.JobDefinition())

    resources: "_tp.Dict[str, metadata.ObjectDefinition]" = _dc.field(default_factory=dict)

    resourceMapping: "_tp.Dict[str, metadata.TagHeader]" = _dc.field(default_factory=dict)

    resultMapping: "_tp.Dict[str, metadata.TagHeader]" = _dc.field(default_factory=dict)
