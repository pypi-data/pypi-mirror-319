# Code generated by TRAC

import typing as _tp  # noqa
import dataclasses as _dc  # noqa
import enum as _enum  # noqa

import tracdap.rt.metadata as metadata



@_dc.dataclass
class TagUpdateList:

    attrs: "_tp.List[metadata.TagUpdate]" = _dc.field(default_factory=list)


@_dc.dataclass
class JobResult:

    jobId: "metadata.TagHeader" = _dc.field(default_factory=lambda: metadata.TagHeader())

    statusCode: "metadata.JobStatusCode" = metadata.JobStatusCode.JOB_STATUS_CODE_NOT_SET

    statusMessage: "str" = ""

    results: "_tp.Dict[str, metadata.ObjectDefinition]" = _dc.field(default_factory=dict)
