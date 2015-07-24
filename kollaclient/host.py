# Copyright(c) 2015, Oracle and/or its affiliates.  All Rights Reserved.
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
import logging

from kollaclient.i18n import _
from kollaclient.sshutils import ssh_check_host
from kollaclient.sshutils import ssh_check_keys
from kollaclient.sshutils import ssh_install_host
from kollaclient.sshutils import ssh_keygen
from kollaclient.utils import load_etc_yaml
from kollaclient.utils import save_etc_yaml

from cliff.command import Command


class HostAdd(Command):
    "Host Add"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(HostAdd, self).get_parser(prog_name)
        parser.add_argument('hostname')
        parser.add_argument('networkaddress')
        # TODO(bmace) error if args missing
        return parser

    def take_action(self, parsed_args):
        hostname = parsed_args.hostname.rstrip()
        netAddr = parsed_args.networkaddress.rstrip()
        contents = load_etc_yaml('hosts.yml')
        for host, hostdata in contents.items():
            if host == hostname:
                # TODO(bmace) fix message
                self.log.info(_("host already exists"))
                return
        hostEntry = {hostname: {'Services': '', 'NetworkAddress':
                     netAddr, 'Zone': ''}}
        contents.update(hostEntry)
        save_etc_yaml('hosts.yml', contents)


class HostRemove(Command):
    "Host Remove"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(HostRemove, self).get_parser(prog_name)
        parser.add_argument('hostname')
        # TODO(bmace) error if arg missing
        return parser

    def take_action(self, parsed_args):
        hostname = parsed_args.hostname.rstrip()
        contents = load_etc_yaml('hosts.yml')
        foundHost = False
        for host, hostdata in contents.items():
            if host == hostname:
                foundHost = True
        if foundHost:
            del contents[hostname]
        else:
            # TODO(bmace) fix message
            self.log.info("no host by name (" + hostname + ") found")
        save_etc_yaml('hosts.yml', contents)


class HostList(Command):
    "Host List"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info(_("host list"))
        contents = load_etc_yaml('hosts.yml')
        # TODO(bmace) fix output format
        for host, hostdata in contents.items():
            self.log.info(host)
            self.log.info(hostdata)


class HostSetzone(Command):
    "Host Setzone"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info(_("host setzone"))
        self.app.stdout.write(parsed_args)


class HostAddservice(Command):
    "Host Addservice"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info(_("host addservice"))
        self.app.stdout.write(parsed_args)


class HostRemoveservice(Command):
    "Host Removeservice"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info(_("host removeservice"))
        self.app.stdout.write(parsed_args)


class HostCheck(Command):
    "Host Check"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(HostCheck, self).get_parser(prog_name)
        parser.add_argument('hostname')
        # TODO(bmace) error if arg missing
        return parser

    def take_action(self, parsed_args):
        self.log.info(_("host check"))
        sshKeysExist = ssh_check_keys()
        if not sshKeysExist:
            ssh_keygen()
        hostname = parsed_args.hostname.rstrip()
        netAddr = None
        contents = load_etc_yaml('hosts.yml')
        hostFound = False
        for host, hostdata in contents.items():
            if host == hostname:
                # TODO(bmace) fix message
                hostFound = True
                netAddr = hostdata['NetworkAddress']
                self.log.info(netAddr)

        if hostFound is False:
            self.log.info("no host by name (" + hostname + ") found")
            return False

        sshCheck = ssh_check_host(netAddr)
        if sshCheck is False:
            self.log.error("ssh access to host failed")
            return


class HostInstall(Command):
    "Host Install"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(HostInstall, self).get_parser(prog_name)
        parser.add_argument('hostname')
        parser.add_argument('password')
        # TODO(bmace) error if arg missing
        return parser

    def take_action(self, parsed_args):
        self.log.info(_("host install"))
        sshKeysExist = ssh_check_keys()
        if not sshKeysExist:
            ssh_keygen()
        hostname = parsed_args.hostname.rstrip()
        # TODO(bmace) get this password in another way?
        password = parsed_args.password.rstrip()
        netAddr = None
        contents = load_etc_yaml('hosts.yml')
        hostFound = False
        for host, hostdata in contents.items():
            if host == hostname:
                # TODO(bmace) fix message
                hostFound = True
                netAddr = hostdata['NetworkAddress']
                self.log.info(netAddr)

        if hostFound is False:
            self.log.info("no host by name (" + hostname + ") found")
            return False

        sshCheck = ssh_check_host(netAddr)
        # If sshCheck fails we need to set up the user / remote ssh keys
        # using root and the available password
        if sshCheck is False:
            self.log.info("configuring admin user and ssh keys")
            self.log.info("calling ssh_install_host with: " + netAddr +
                          " : " + password)
            installHost = ssh_install_host(netAddr, password)
            if installHost is False:
                # TODO(bmace) probably throw out of ssh_install_host and
                # log the error here, or maybe log it in ssh_install_host?
                self.log.info("host install failed for host: " + hostname)
            else:
                self.log.info("host install succeeded")
