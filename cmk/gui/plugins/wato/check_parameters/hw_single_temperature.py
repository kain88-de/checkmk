#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Integer,
    Tuple,
)
from cmk.gui.plugins.wato import (
    RulespecGroupCheckParametersEnvironment,
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
)


def _parameter_valuespec_hw_single_temperature():
    return Tuple(help=_("Temperature levels for hardware devices with "
                        "a single temperature sensor."),
                 elements=[
                     Integer(title=_("warning at"), unit=u"°C", default_value=35),
                     Integer(title=_("critical at"), unit=u"°C", default_value=40),
                 ])


rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="hw_single_temperature",
        group=RulespecGroupCheckParametersEnvironment,
        is_deprecated=True,
        parameter_valuespec=_parameter_valuespec_hw_single_temperature,
        title=lambda: _("Host/Device temperature"),
    ))
