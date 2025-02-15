#!/usr/bin/env python3
# Copyright (C) 2021 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
# mypy: disallow_untyped_defs

import json
import typing

from cmk.base.plugins.agent_based.agent_based_api.v1 import HostLabel, register, Service
from cmk.base.plugins.agent_based.agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
    HostLabelGenerator,
    StringTable,
)
from cmk.base.plugins.agent_based.utils.kube import (
    check_with_time,
    CronJobInfo,
    kube_annotations_to_cmk_labels,
    kube_labels_to_cmk_labels,
)
from cmk.base.plugins.agent_based.utils.kube_info import check_info


def parse_kube_cronjob_info(string_table: StringTable) -> CronJobInfo:
    """Parses `string_table` into a CronJobInfo instance

    >>> parse_kube_cronjob_info([['{"architecture": "amd64",'
    ... '"name": "cronjob",'
    ... '"namespace": "checkmk-monitoring",'
    ... '"creation_timestamp": "1640000000.0",'
    ... '"cluster": "cluster",'
    ... '"labels": {},'
    ... '"annotations": {},'
    ... '"schedule": "0 * * * *",'
    ... '"concurrency_policy": "Allow",'
    ... '"failed_jobs_history_limit": "10",'
    ... '"successful_jobs_history_limit": "10",'
    ... '"suspend": "false"}'
    ... ]])
    CronJobInfo(name='cronjob', namespace='checkmk-monitoring', creation_timestamp=1640000000.0, labels={}, annotations={}, schedule='0 * * * *', concurrency_policy=<ConcurrencyPolicy.Allow: 'Allow'>, failed_jobs_history_limit=10, successful_jobs_history_limit=10, suspend=False, cluster='cluster')
    """
    return CronJobInfo(**json.loads(string_table[0][0]))


def host_labels(section: CronJobInfo) -> HostLabelGenerator:
    """Host label function

    Labels:
        cmk/kubernetes:
            This label is set to "yes" for all Kubernetes objects.

        cmk/kubernetes/object:
            This label is set to the Kubernetes object type.

        cmk/kubernetes/cluster:
            This label is set to the given Kubernetes cluster name.

        cmk/kubernetes/cronjob:
            This label contains the name of the Kubernetes CronJob this
            checkmk host is associated with.

        cmk/kubernetes/annotation/{key}:{value} :
            These labels are yielded for each Kubernetes annotation that is
            a valid Kubernetes label. This can be configured via the rule
            'Kubernetes'.
    """
    yield HostLabel("cmk/kubernetes", "yes")
    yield HostLabel("cmk/kubernetes/object", "cronjob")
    yield HostLabel("cmk/kubernetes/cluster", section.cluster)
    yield HostLabel("cmk/kubernetes/namespace", section.namespace)
    yield HostLabel("cmk/kubernetes/cronjob", section.name)
    yield from kube_labels_to_cmk_labels(section.labels)
    yield from kube_annotations_to_cmk_labels(section.annotations)


register.agent_section(
    name="kube_cron_job_info_v1",
    parsed_section_name="kube_cronjob_info",
    parse_function=parse_kube_cronjob_info,
    host_label_function=host_labels,
)


def discovery_kube_cronjob_info(section: CronJobInfo) -> DiscoveryResult:
    yield Service()


def check_kube_cronjob_info(now: float, section: CronJobInfo) -> CheckResult:
    yield from check_info(
        {
            "name": section.name,
            "age": now - typing.cast(float, section.creation_timestamp),
            "schedule": section.schedule,
            "concurrency_policy": section.concurrency_policy,
            "failed_jobs_history_limit": section.failed_jobs_history_limit,
            "successful_jobs_history_limit": section.successful_jobs_history_limit,
            "suspend": section.suspend,
        }
    )


register.check_plugin(
    name="kube_cronjob_info",
    service_name="Info",
    discovery_function=discovery_kube_cronjob_info,
    check_function=check_with_time(check_kube_cronjob_info),
)
