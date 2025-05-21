
import frappe
import unittest
from momo_zambia.momo_zambia.api.payment import initiate_payment

class TestMoMoCollection(unittest.TestCase):
    def test_mock_payment(self):
        res = initiate_payment(mobile="260970000000", amount="10", currency="ZMW", external_id="TEST123")
        self.assertIn("reference_id", res)
