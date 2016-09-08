import os
from twisted.trial import unittest
from twisted.internet import defer
from twisted.python import usage
from allmydata.util import configutil
from ..common_util import run_cli

class Config(unittest.TestCase):
    def read_config(self, basedir):
        tahoe_cfg = os.path.join(basedir, "tahoe.cfg")
        config = configutil.get_config(tahoe_cfg)
        return config

    @defer.inlineCallbacks
    def test_client(self):
        basedir = self.mktemp()
        rc, out, err = yield run_cli("create-client", basedir)
        cfg = self.read_config(basedir)
        self.assertEqual(cfg.getboolean("node", "reveal-IP-address"), True)
        self.assertEqual(cfg.get("node", "tub.port"), "disabled")
        self.assertEqual(cfg.get("node", "tub.location"), "disabled")

    @defer.inlineCallbacks
    def test_client_hostname(self):
        basedir = self.mktemp()
        try:
            rc, out, err = yield run_cli("create-client", "--hostname=computer", basedir)
        except usage.UsageError, e:
            self.failUnlessEqual(str(e), "option --hostname not recognized")
        else:
            self.fail("UsageError expected to be raised")

    @defer.inlineCallbacks
    def test_client_port_location(self):
        basedir = self.mktemp()
        try:
            rc, out, err = yield run_cli("create-client",
                                         "--port=unix:/var/tahoe/socket",
                                         "--location=tor:myservice.onion:12345",
                                         basedir)
        except usage.UsageError, e:
            self.failUnlessEqual(str(e), "option --port not recognized")
        else:
            self.fail("UsageError expected to be raised")

    @defer.inlineCallbacks
    def test_client_port_only(self):
        basedir = self.mktemp()
        try:
            rc, out, err = yield run_cli("create-client", "--port=unix:/var/tahoe/socket", basedir)
        except usage.UsageError, e:
            self.failUnlessEqual(str(e), "option --port not recognized")
        else:
            self.fail("UsageError expected to be raised")

    @defer.inlineCallbacks
    def test_client_location_only(self):
        basedir = self.mktemp()
        try:
            rc, out, err = yield run_cli("create-client", "--location=tor:myservice.onion:12345", basedir)
        except usage.UsageError, e:
            self.failUnlessEqual(str(e), "option --location not recognized")
        else:
            self.fail("UsageError expected to be raised")

    @defer.inlineCallbacks
    def test_client_listen_tcp(self):
        basedir = self.mktemp()
        try:
            rc, out, err = yield run_cli("create-client", "--listen=tcp", basedir)
        except usage.UsageError, e:
            self.failUnlessEqual(str(e), "option --listen not recognized")
        else:
            self.fail("UsageError expected to be raised)")

    @defer.inlineCallbacks
    def test_client_listen_tor(self):
        basedir = self.mktemp()
        try:
            rc, out, err = yield run_cli("create-client", "--listen=tor", basedir)
        except usage.UsageError, e:
            self.failUnlessEqual(str(e), "option --listen not recognized")
        else:
            self.fail("UsageError expected to be raised)")

    @defer.inlineCallbacks
    def test_client_listen_i2p(self):
        basedir = self.mktemp()
        try:
            rc, out, err = yield run_cli("create-client", "--listen=i2p", basedir)
        except usage.UsageError, e:
            self.failUnlessEqual(str(e), "option --listen not recognized")
        else:
            self.fail("UsageError expected to be raised")

    @defer.inlineCallbacks
    def test_client_hide_ip(self):
        basedir = self.mktemp()
        rc, out, err = yield run_cli("create-client", "--hide-ip", basedir)
        cfg = self.read_config(basedir)
        self.assertEqual(cfg.getboolean("node", "reveal-IP-address"), False)

    @defer.inlineCallbacks
    def test_node(self):
        basedir = self.mktemp()
        rc, out, err = yield run_cli("create-node", basedir)
        cfg = self.read_config(basedir)
        self.assertEqual(cfg.getboolean("node", "reveal-IP-address"), True)

    @defer.inlineCallbacks
    def test_node_hide_ip(self):
        basedir = self.mktemp()
        rc, out, err = yield run_cli("create-node", "--hide-ip", basedir)
        cfg = self.read_config(basedir)
        self.assertEqual(cfg.getboolean("node", "reveal-IP-address"), False)

    @defer.inlineCallbacks
    def test_node_hostname(self):
        basedir = self.mktemp()
        rc, out, err = yield run_cli("create-node", "--hostname=computer", basedir)
        cfg = self.read_config(basedir)
        self.assertTrue("computer" in cfg.get("node", "tub.location"))

    @defer.inlineCallbacks
    def test_node_port_location(self):
        basedir = self.mktemp()
        rc, out, err = yield run_cli("create-node",
                                     "--port=unix:/var/tahoe/socket",
                                     "--location=tor:myservice.onion:12345",
                                     basedir)
        cfg = self.read_config(basedir)
        self.assertEqual(cfg.get("node", "tub.location"), "tor:myservice.onion:12345")
        self.assertEqual(cfg.get("node", "tub.port"), "unix:/var/tahoe/socket")

    @defer.inlineCallbacks
    def test_node_listen_tcp(self):
        basedir = self.mktemp()
        rc, out, err = yield run_cli("create-node", "--listen=tcp", basedir)
        cfg = self.read_config(basedir)

    @defer.inlineCallbacks
    def test_node_listen_tor(self):
        basedir = self.mktemp()
        try:
            rc, out, err = yield run_cli("create-node", "--listen=tor", basedir)
        except NotImplementedError, e:
            self.failUnlessEqual(str(e), "This feature addition is being tracked by this ticket:" +
            "https://tahoe-lafs.org/trac/tahoe-lafs/ticket/2490")
        else:
            self.fail("NotImplementedError expected to be raised")

    @defer.inlineCallbacks
    def test_node_listen_i2p(self):
        basedir = self.mktemp()
        try:
            rc, out, err = yield run_cli("create-node", "--listen=i2p", basedir)
        except NotImplementedError, e:
            self.failUnlessEqual(str(e), "This feature addition is being tracked by this ticket:" +
            "https://tahoe-lafs.org/trac/tahoe-lafs/ticket/2490")
        else:
            self.fail("NotImplementedError expected to be raised")

    @defer.inlineCallbacks
    def test_node_port_only(self):
        basedir = self.mktemp()
        try:
            rc, out, err = yield run_cli("create-node", "--port=unix:/var/tahoe/socket", basedir)
        except usage.UsageError, e:
            self.failUnlessEqual(str(e), "The --port option must be used with the --location option.")
        else:
            self.fail("UsageError expected to be raised")

    @defer.inlineCallbacks
    def test_node_location_only(self):
        basedir = self.mktemp()
        try:
            rc, out, err = yield run_cli("create-node", "--location=tor:myservice.onion:12345", basedir)
        except usage.UsageError, e:
            self.failUnlessEqual(str(e), "The --location option must be used with the --port option.")
        else:
            self.fail("UsageError expected to be raised")

    @defer.inlineCallbacks
    def test_introducer(self):
        basedir = self.mktemp()
        rc, out, err = yield run_cli("create-introducer", basedir)
        cfg = self.read_config(basedir)
        self.assertEqual(cfg.getboolean("node", "reveal-IP-address"), True)

    @defer.inlineCallbacks
    def test_introducer_hide_ip(self):
        basedir = self.mktemp()
        rc, out, err = yield run_cli("create-introducer", "--hide-ip", basedir)
        cfg = self.read_config(basedir)
        self.assertEqual(cfg.getboolean("node", "reveal-IP-address"), False)

    @defer.inlineCallbacks
    def test_introducer_hostname(self):
        basedir = self.mktemp()
        rc, out, err = yield run_cli("create-introducer", "--hostname=computer", basedir)
        cfg = self.read_config(basedir)
        self.assertTrue("computer" in cfg.get("node", "tub.location"))
