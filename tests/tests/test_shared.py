#!/usr/bin/env python3
import unittest, os

AID_SERVER = "112233445500"
AID_CLIENT = "112233446600"
# APPLET = "toys.TeapotApplet"
# CLASSDIR = "Teapot"

# mode = os.environ.get('TEST_MODE', "simulator")
# if mode=="simulator":
#     from util.simulator import Simulator, ISOException
#     sim = Simulator(AID, APPLET, CLASSDIR)
# elif mode=="card":
from util.card import Card, ISOException
sim = Card(AID_CLIENT)
# else:
#     raise RuntimeError("Not supported")

def setUpModule():
    sim.connect()

def tearDownModule():
    sim.disconnect()

def encode(data):
    return bytes([len(data)])+data

class TeapotTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_shared(self):
        # set secret
        res = sim.request(b"\x00\x01\x00\x00\x05\x12\x34\x56\x78\x9a")
        print(res.hex())
        # get secret
        res = sim.request(b"\x00\x00\x00\x00\x05")
        print(res.hex())
        self.assertEqual(res[:5], b"\x12\x34\x56\x78\x9a")


if __name__ == '__main__':
    unittest.main()