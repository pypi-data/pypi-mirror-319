# Copyright (c) OpenMMLab. All rights reserved.
import copy
import sys

from ..utils import Registry

RUNNERS = Registry("runner", sys.modules[__name__])
RUNNER_BUILDERS = Registry("runner builder", sys.modules[__name__])


def build_runner_constructor(cfg):
    return RUNNER_BUILDERS.build(cfg)


def build_runner(cfg, default_args=None):
    runner_cfg = copy.deepcopy(cfg)
    constructor_type = runner_cfg.pop("constructor", "DefaultRunnerConstructor")
    runner_constructor = build_runner_constructor(
        dict(type=constructor_type, runner_cfg=runner_cfg, default_args=default_args)
    )
    runner = runner_constructor()
    return runner
