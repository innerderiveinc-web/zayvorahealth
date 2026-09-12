"""
Unit tests for ZAYVORA Health™ Prescription Delivery Logistics & Courier Tracking (Issue AUTO-15).
Tests multi-carrier AWB generation, botanical cold-chain enforcement, and real-time tracking webhooks.
"""
from __future__ import annotations

import unittest
import uuid
from datetime import datetime, timezone

from app.engines.courier_engine import CourierLogisticsEngine
from app.models.logistics import ShipmentRecord


class MockShipmentDb:
    def __init__(self):
        self.shipments = {}

    def add(self, shipment):
        self.shipments[shipment.awb_tracking_number] = shipment

    def commit(self):
        pass

    def refresh(self, shipment):
        pass

    def get_shipment_by_awb(self, awb):
        return self.shipments.get(awb)

    def close(self):
        pass


class TestCourierLogistics(unittest.TestCase):
    def setUp(self):
        self.db = MockShipmentDb()
        self.org_id = uuid.uuid4()
        self.patient_id = uuid.uuid4()
        self.prescription_id = uuid.uuid4()

    def tearDown(self):
        self.db.close()

    def test_shipment_creation_and_awb_generation(self):
        shipment = CourierLogisticsEngine.create_shipment(
            organization_id=self.org_id,
            prescription_id=self.prescription_id,
            patient_id=self.patient_id,
            carrier="SHIPROCKET",
            destination_pincode="110025",
            shipping_address="Jamia Nagar, Okhla, New Delhi 110025",
            temperature_controlled=True,
            temperature_range_celsius="15C - 20C (Protected Herb Extracts)",
            db=self.db,
        )

        self.assertIsNotNone(shipment.id)
        self.assertTrue(shipment.awb_tracking_number.startswith("AWB-SHIP-"))
        self.assertEqual(shipment.status, "MANIFESTED")
        self.assertTrue(shipment.temperature_controlled)
        self.assertEqual(len(shipment.tracking_history), 1)

    def test_invalid_carrier_rejection(self):
        with self.assertRaises(ValueError):
            CourierLogisticsEngine.create_shipment(
                organization_id=self.org_id,
                prescription_id=self.prescription_id,
                patient_id=self.patient_id,
                carrier="UNKNOWN_COURIER",
                destination_pincode="110025",
                shipping_address="Jamia Nagar, New Delhi",
                db=self.db,
            )

    def test_courier_tracking_webhook_processing(self):
        shipment = CourierLogisticsEngine.create_shipment(
            organization_id=self.org_id,
            prescription_id=self.prescription_id,
            patient_id=self.patient_id,
            carrier="DELHIVERY",
            destination_pincode="500001",
            shipping_address="Charminar Road, Hyderabad 500001",
            db=self.db,
        )
        awb = shipment.awb_tracking_number

        # Milestone 1: IN_TRANSIT
        res1 = CourierLogisticsEngine.process_tracking_webhook(
            carrier="DELHIVERY",
            awb_tracking_number=awb,
            event_status="IN_TRANSIT",
            location="Delhi National Sorting Hub",
            notes="Package departed hub towards Hyderabad.",
            db=self.db,
        )
        self.assertEqual(res1["current_status"], "IN_TRANSIT")
        self.assertEqual(res1["total_events"], 2)

        # Milestone 2: DELIVERED
        res2 = CourierLogisticsEngine.process_tracking_webhook(
            carrier="DELHIVERY",
            awb_tracking_number=awb,
            event_status="DELIVERED",
            location="Hyderabad Delivery Hub",
            notes="Delivered to consignee with signature.",
            db=self.db,
        )
        self.assertEqual(res2["current_status"], "DELIVERED")
        self.assertIsNotNone(res2["delivered_at"])
        self.assertEqual(res2["total_events"], 3)


if __name__ == "__main__":
    unittest.main()
