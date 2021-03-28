import os
from pathlib import Path
from platform import system
from os.path import realpath
import pytest
import numpy as np
from numpy.testing import assert_allclose
import porespy as ps
import openpnm as op
import openpnm.models.geometry as gmods


class NetworkExtractionTest():
    def setup_class(self):
        self.im = ps.generators.blobs(shape=[300, 300])
        self.snow = ps.filters.snow_partitioning(self.im, return_all=True)
        self.im3d = ps.generators.blobs(shape=[50, 50, 50])
        self.snow3d = ps.filters.snow_partitioning(self.im3d, return_all=True)
        self.net = op.network.Cubic(shape=[5, 5, 5])
        self.geom = op.geometry.StickAndBall(
            network=self.net, pores=self.net.Ps, throats=self.net.Ts)
        self.geom.add_model(propname="pore.volume", model=gmods.pore_volume.cube)
        self.geom.add_model(propname="throat.volume", model=gmods.throat_volume.cylinder)

    def test_regions_to_network(self):
        im = self.snow.regions*self.im
        net = ps.networks.regions_to_network(im)
        found_nans = False
        for key in net.keys():
            if np.any(np.isnan(net[key])):
                found_nans = True
        assert found_nans is False

    def test_snow_2d(self):
        a = np.unique(self.snow.peaks*self.im)
        b = np.unique(self.snow.regions*self.im)
        assert len(a) == len(b)

    def test_snow_3d(self):
        a = np.unique(self.snow3d.peaks*self.im3d)
        b = np.unique(self.snow3d.regions*self.im3d)
        assert len(a) == len(b)

    def test_extract_pore_network_3d(self):
        im = self.snow3d.regions*self.im3d
        net = ps.networks.regions_to_network(im)
        found_nans = False
        for key in net.keys():
            if np.any(np.isnan(net[key])):
                found_nans = True
        assert found_nans is False

    def test_snow(self):
        net = ps.networks.snow2(self.im3d)
        found_nans = False
        for key in net.keys():
            if np.any(np.isnan(net[key])):
                found_nans = True
        assert found_nans is False

    def test_map_to_regions(self):
        im = self.im
        regions = ps.filters.snow_partitioning(im)
        values = np.random.rand(regions.max() + 1)
        mapped = ps.networks.map_to_regions(regions, values)
        assert mapped.max() < 1
        # Some failures
        values = np.random.rand(regions.max())
        with pytest.raises(Exception):
            mapped = ps.networks.map_to_regions(regions, values)
        values = np.random.rand(regions.max()+2)
        with pytest.raises(Exception):
            mapped = ps.networks.map_to_regions(regions, values)

    def test_planar_2d_image(self):
        np.random.seed(1)
        im1 = ps.generators.blobs([100, 100, 1])
        np.random.seed(1)
        im2 = ps.generators.blobs([100, 1, 100])
        np.random.seed(1)
        im3 = ps.generators.blobs([1, 100, 100])
        np.random.seed(1)
        snow_out1 = ps.filters.snow_partitioning(im1, return_all=True)
        pore_map1 = snow_out1.im * snow_out1.regions
        net1 = ps.networks.regions_to_network(regions=pore_map1,
                                              voxel_size=1)
        np.random.seed(1)
        snow_out2 = ps.filters.snow_partitioning(im2, return_all=True)
        pore_map2 = snow_out2.im * snow_out2.regions
        net2 = ps.networks.regions_to_network(regions=pore_map2,
                                              voxel_size=1)
        np.random.seed(1)
        snow_out3 = ps.filters.snow_partitioning(im3, return_all=True)
        pore_map3 = snow_out3.im * snow_out3.regions
        net3 = ps.networks.regions_to_network(regions=pore_map3,
                                              voxel_size=1)
        assert np.allclose(net1['pore.coords'][:, 0], net2['pore.coords'][:, 0])
        assert np.allclose(net1['pore.coords'][:, 1], net2['pore.coords'][:, 2])
        assert np.allclose(net1['pore.coords'][:, 0], net3['pore.coords'][:, 1])

    def test_generate_voxel_image(self):
        im = ps.networks.generate_voxel_image(
            network=self.net,
            pore_shape="cube",
            throat_shape="cylinder",
            max_dim=400,
            rtol=0.01
        )
        porosity_actual = im.astype(bool).sum() / np.prod(im.shape)
        volume_void = self.net["pore.volume"].sum() + self.net["throat.volume"].sum()
        volume_total = np.prod(self.net.spacing * self.net.shape)
        porosity_desired = volume_void / volume_total
        assert_allclose(actual=porosity_actual, desired=porosity_desired, rtol=0.1)

    def test_max_ball(self):
        path = Path(realpath(__file__), '../../fixtures/pnextract.exe')
        if system() == 'Windows':
            ps.networks.maximal_ball(im=self.im3d, prefix='test_maxball',
                                     path_to_exe=path, voxel_size=1e-6)
            assert os.path.isfile("test_maxball_link1.dat")
            assert os.path.isfile("test_maxball_link2.dat")
            assert os.path.isfile("test_maxball_node1.dat")
            assert os.path.isfile("test_maxball_node2.dat")
            os.remove("test_maxball_link1.dat")
            os.remove("test_maxball_link2.dat")
            os.remove("test_maxball_node1.dat")
            os.remove("test_maxball_node2.dat")


if __name__ == '__main__':
    t = NetworkExtractionTest()
    self = t
    t.setup_class()
    for item in t.__dir__():
        if item.startswith('test'):
            print(f'Running test: {item}')
            t.__getattribute__(item)()
