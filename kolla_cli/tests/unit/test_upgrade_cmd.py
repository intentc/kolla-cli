# Copyright (c) 2018 OpenStack Foundation
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from kolla_cli.tests.unit.common import KollaCliUnitTest


class TestUnit(KollaCliUnitTest):
    @mock.patch('kolla_cli.api.control_plane.ControlPlaneApi.upgrade')
    @mock.patch('kolla_cli.common.ansible.job.AnsibleJob.get_status')
    @mock.patch('kolla_cli.shell.KollaCli._is_inventory_present',
                return_value=True)
    def test_upgrade(self, _, mock_get_status, mock_upgrade):
        mock_get_status.return_value = 0
        mock_upgrade.return_value = self.get_fake_job()
        ret = self.run_cli_command('action upgrade')
        self.assertEqual(ret, 0)
        mock_upgrade.assert_called_once_with(1, [], [])

    @mock.patch('kolla_cli.api.control_plane.ControlPlaneApi.upgrade')
    @mock.patch('kolla_cli.common.ansible.job.AnsibleJob.get_status')
    @mock.patch('kolla_cli.shell.KollaCli._is_inventory_present',
                return_value=True)
    def test_upgrade_with_hosts(self, _, mock_get_status, mock_upgrade):
        mock_get_status.return_value = 0
        mock_upgrade.return_value = self.get_fake_job()
        hostnames = ['host1', 'host2']
        ret = self.run_cli_command(
            'action upgrade --hosts {hosts}'.format(
                hosts=','.join(hostnames)))
        self.assertEqual(ret, 0)
        mock_upgrade.assert_called_once_with(1, hostnames, [])

    @mock.patch('kolla_cli.api.control_plane.ControlPlaneApi.upgrade')
    @mock.patch('kolla_cli.common.ansible.job.AnsibleJob.get_status')
    @mock.patch('kolla_cli.shell.KollaCli._is_inventory_present',
                return_value=True)
    def test_upgrade_with_services(self, _, mock_get_status, mock_upgrade):
        mock_get_status.return_value = 0
        mock_upgrade.return_value = self.get_fake_job()
        services = ['service1', 'service2']
        ret = self.run_cli_command(
            'action upgrade --service {services}'.format(
                services=','.join(services)))
        self.assertEqual(ret, 0)
        mock_upgrade.assert_called_once_with(1, [], services)

    @mock.patch('kolla_cli.api.control_plane.ControlPlaneApi.upgrade')
    @mock.patch('kolla_cli.common.ansible.job.AnsibleJob.get_status')
    @mock.patch('kolla_cli.shell.KollaCli._is_inventory_present',
                return_value=True)
    def test_upgrade_with_hosts_and_services(self, _, mock_get_status,
                                             mock_upgrade):
        mock_get_status.return_value = 0
        mock_upgrade.return_value = self.get_fake_job()
        hostnames = ['host1', 'host2']
        services = ['service1', 'service2']
        ret = self.run_cli_command(
            'action upgrade --hosts {hosts} --service {services}'.format(
                hosts=','.join(hostnames), services=','.join(services)))
        self.assertEqual(ret, 0)
        mock_upgrade.assert_called_once_with(1, hostnames, services)
