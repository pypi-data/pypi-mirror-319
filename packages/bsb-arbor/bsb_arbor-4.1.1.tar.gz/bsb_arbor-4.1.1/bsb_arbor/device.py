import abc

import arbor
from bsb import DeviceModel, Targetting, config, types


@config.dynamic(attr_name="device", auto_classmap=True, classmap_entry=None)
class ArborDevice(DeviceModel):
    targetting = config.attr(type=Targetting, required=True)
    resolution = config.attr(type=float)
    sampling_policy = config.attr(type=types.in_(["exact"]))

    def __init__(self, **kwargs):
        self._probe_ids = []

    def __boot__(self):
        self.resolution = self.resolution or self.simulation.resolution

    def register_probe_id(self, gid, tag):
        self._probe_ids.append((gid, tag))

    def prepare_samples(self, simdata):
        self._handles = [
            self.sample(simdata.arbor_sim, probe_id) for probe_id in self._probe_ids
        ]

    def sample(self, sim, probe_id):
        schedule = arbor.regular_schedule(self.resolution)
        sampling_policy = getattr(arbor.sampling_policy, self.sampling_policy)
        return sim.sample(probe_id, schedule, sampling_policy)

    def get_samples(self, sim):
        return [sim.samples(handle) for handle in self._handles]

    def get_meta(self):
        attrs = ("name", "sampling_policy", "resolution")
        return dict(zip(attrs, (getattr(self, attr) for attr in attrs)))

    @abc.abstractmethod
    def implement_probes(self, simdata, target):
        pass

    @abc.abstractmethod
    def implement_generators(self, simdata, target):
        pass
