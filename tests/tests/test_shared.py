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
# server = Card(AID_SERVER)
# client = Card(AID_CLIENT)
# else:
#     raise RuntimeError("Not supported")

def setUpModule():
    # sim.connect()
    pass

def tearDownModule():
    # sim.disconnect()
    pass

SELECT = b"\x00\xA4\x04\x00"
GET    = b"\xB0\xA1\x00\x00"
STORE  = b"\xB0\xA2\x00\x00"

def encode(data):
    return bytes([len(data)])+data

class TeapotTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_shared(self):
        card = Card(AID_SERVER)
        card.connect()
        # set secret
        res = card.request(b"\x00\x00\x00\x00\x05\x12\x34\x56\x78\x9a")
        print(res.hex())
        # switch to client
        card.aid = AID_CLIENT
        card.connect()
        res = card.request(b"\x00\x00\x00\x00\x05")
        self.assertEqual(res, b"\x12\x34\x56\x78\x9a")


if __name__ == '__main__':
    unittest.main()