# Copyright (C) 2018  INRIA
# Copyright (C) 2018  University of Lille
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re
from enum import Enum

from powerapi.formula import FormulaState


class SmartWattsFormulaScope(Enum):
    """
    Enum used to set the scope of the SmartWatts formula.
    """
    CPU = "cpu"
    DRAM = "dram"


class SmartWattsFormulaConfig:
    """
    Global config of the SmartWatts formula.
    """

    def __init__(self, scope, reports_frequency, rapl_event, error_threshold, cpu_topology, min_samples_required, history_window_size):
        """
        Initialize a new formula config object.
        :param scope: Scope of the formula
        :param reports_frequency: Frequency at which the reports (in milliseconds)
        :param rapl_event: RAPL event to use as reference
        :param error_threshold: Error threshold (in Watt)
        :param cpu_topology: Topology of the CPU
        :param min_samples_required: Minimum amount of samples required before trying to learn a power model
        :param history_window_size: Size of the history window used to keep samples to learn from
        """
        self.scope = scope
        self.reports_frequency = reports_frequency
        self.rapl_event = rapl_event
        self.error_threshold = error_threshold
        self.cpu_topology = cpu_topology
        self.min_samples_required = min_samples_required
        self.history_window_size = history_window_size


class SmartWattsFormulaState(FormulaState):
    """
    State of the SmartWatts formula actor.
    """

    def __init__(self, actor, pushers, metadata, config):
        """
        Initialize a new formula state object.
        :param actor: Actor of the formula
        :param pushers: Dictionary of available pushers
        :param config: Configuration of the formula
        """
        FormulaState.__init__(self, actor, pushers, metadata)
        self.config = config

        m = re.search(r'^\(\'(.*)\', \'(.*)\', \'(.*)\'\)$', actor.name)  # TODO: Need a better way to get these information
        self.dispatcher = m.group(1)
        self.sensor = m.group(2)
        self.socket = int(m.group(3))
