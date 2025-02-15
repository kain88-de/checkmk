#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# fmt: off
# type: ignore
from cmk.base.plugins.agent_based.utils.df import FILESYSTEM_DEFAULT_LEVELS

checkname = 'storeonce_servicesets'

freeze_time = '2020-01-02 13:41:00'

info = [
    ['[1]'], ['ServiceSet ID', '1'], ['ServiceSet Name', '', 'Service Set 1'],
    ['ServiceSet Alias', 'SET1'], ['Serial Number', 'CZ25132LTD01'],
    ['Software Version', '3.15.1-1636.1'],
    ['Product Class', 'HPE StoreOnce 4700 Backup'],
    ['Capacity in bytes', '75952808613643'],
    ['Free Space in bytes', '53819324528395'],
    ['User Data Stored in bytes', '305835970141743'],
    ['Size On Disk in bytes', '19180587585836'],
    ['Deduplication Ratio', '15.945078260668'],
    ['ServiceSet Health Level', '1'], ['ServiceSet Health', 'OK'],
    ['ServiceSet Status', 'Running'], ['Replication Health Level', '1'],
    ['Replication Health', 'OK'], ['Replication Status', 'Running'],
    ['Overall Health Level', '1'], ['Overall Health', 'OK'],
    ['Overall Status', 'Running'], ['Housekeeping Health Level', '1'],
    ['Housekeeping Health', 'OK'], ['Housekeeping Status', 'Running'],
    ['Primary Node', 'hpcz25132ltd'], ['Secondary Node', 'None'],
    ['Active Node', 'hpcz25132ltd']
]

discovery = {'': [('1', {})], 'capacity': [('1', {})]}

checks = {
    '': [
        (
            '1', {}, [
                (0, 'Alias: SET1', []),
                (0, 'Overall Status: Running, Overall Health: OK', [])
            ]
        )
    ],
    'capacity': [
        (
            '1', FILESYSTEM_DEFAULT_LEVELS, [
                (
                    0, 'Used: 29.14% - 20.1 TiB of 69.1 TiB', [
                        (
                            'fs_used', 21108135.3046875, 57947394.26700058,
                            65190818.550375655, 0, None
                        ),
                        ('fs_free', 51326107.529063225, None, None, 0, None),
                        (
                            'fs_used_percent', 29.14110022953421, 80.0, 90.0, 0.0, 100.0
                        ), ('fs_size', 72434242.83375072, None, None, 0, None)
                    ]
                ),
                (
                    0, 'Dedup ratio: 15.95',
                    [('dedup_rate', 15.945078260668, None, None, None, None)]
                )
            ]
        )
    ]
}
