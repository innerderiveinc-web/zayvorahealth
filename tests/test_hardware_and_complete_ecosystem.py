#!/usr/bin/env python3
"""
ZAYVORA Health OS™ v5.0 — Clinical Hardware, Mobile, & Complete Ecosystem Test Suite
Validates:
1. Nabz 10-Ajnas Pulse Sensor Driver (FFT, AIx, PWV, Mizaj inference, safe_to_lock invariant)
2. Multispectral Lisan Tongue Camera Driver (CIE-Lab, 3-zone somatotopy, Humoral dyscrasia)
3. Wearables BLE Gateway (GATT 0x180D/0x1809/0x1822, Quwwat Hayawaniyyah index)
4. Botanical QC NIR Spectrometer (Heavy metals <0.05 ppm, Withanolides/Gymnemic acids, Mudabbar gate)
5. Cold-Chain Dispensary Environmental IoT Sensor (15°C–25°C, <60% RH, dew point, thermal excursion)
6. Mobile Offline Storage Service & Vernacular Audio Posology
7. Web E-Commerce Cart, Checkout, and Order Receipt Engine
8. REST Gateway Hardware Endpoints & Preview HTML Hardware Lab
"""

import os
import sys
import unittest
import hashlib
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def switch_service(service_name: str):
    """Isolates service imports to avoid module conflicts."""
    abs_service = os.path.abspath(os.path.join(BASE_DIR, f"services/{service_name}"))
    for s in [
        "services/clinical",
        "services/therapeutic",
        "services/knowledge",
        "services/ai",
        "services/identity",
        "services/gateway",
    ]:
        p = os.path.abspath(os.path.join(BASE_DIR, s))
        while p in sys.path:
            sys.path.remove(p)
    sys.path.insert(0, abs_service)
    to_del = [k for k in list(sys.modules.keys()) if k == "app" or k.startswith("app.")]
    for k in to_del:
        del sys.modules[k]


class TestClinicalHardwareAndEcosystem(unittest.TestCase):

    # -------------------------------------------------------------------------
    # PART 1: NABZ 10-AJNAS PULSE SENSOR DRIVER & DSP
    # -------------------------------------------------------------------------
    def test_01_nabz_pulse_sensor_driver_and_10_ajnas(self):
        """Tests the Nabz pulse sensor hardware driver and 10-Ajnas digital signal processor."""
        switch_service("clinical")
        from app.hardware.nabz_pulse_sensor import NabzPulseSensorDriver, PulseSignalSample, NabzAnalysisResult

        driver = NabzPulseSensorDriver(sensor_id="NABZ-TEST-01")
        self.assertTrue(driver.is_connected)
        self.assertEqual(driver.firmware_version, "v3.8.4-Clinical")

        # 1. Acquire waveform stream (100 Hz for 2.5 seconds = 250 samples) with Balghami bias
        samples = driver.acquire_waveform_stream(duration_seconds=2.5, patient_mizaj_bias="Balghami", baseline_hr=58)
        self.assertEqual(len(samples), 250)
        self.assertIsInstance(samples[0], PulseSignalSample)
        self.assertGreaterEqual(samples[0].raw_photoplethysmogram, 0.0)
        self.assertLessEqual(samples[0].raw_photoplethysmogram, 1.0)
        self.assertGreater(samples[0].acoustic_resonance_db, 30.0)
        self.assertGreater(samples[0].tonometric_force_kpa, 1.0)

        # 2. Analyze pulse signals across 10 Classical Dimensions (10-Ajnas)
        analysis: NabzAnalysisResult = driver.analyze_pulse(patient_id="PAT-99101", samples=samples)
        self.assertEqual(analysis.patient_id, "PAT-99101")
        self.assertEqual(analysis.sampling_rate_hz, 100)
        self.assertGreater(analysis.heart_rate_bpm, 40)
        self.assertLess(analysis.heart_rate_bpm, 180)
        self.assertGreater(analysis.augmentation_index_pct, 0.0)
        self.assertGreater(analysis.pulse_wave_velocity_m_s, 3.0)

        # Validate 10-Ajnas dimensions are populated
        self.assertTrue(len(analysis.miqdar) > 0, "Miqdar missing")
        self.assertTrue(len(analysis.kayfiyyat_qar) > 0, "Kayfiyyat-e-Qar missing")
        self.assertTrue(len(analysis.surat) > 0, "Sur'at missing")
        self.assertTrue(len(analysis.tawatur) > 0, "Tawatur missing")
        self.assertTrue(len(analysis.imtila) > 0, "Imtila missing")
        self.assertTrue(len(analysis.malmas) > 0, "Malmas missing")
        self.assertTrue(len(analysis.zaman_sukoon) > 0, "Zaman-e-Sukoon missing")
        self.assertTrue(len(analysis.wazan) > 0, "Wazan missing")
        self.assertTrue(len(analysis.istiwa) > 0, "Istiwa missing")
        self.assertTrue(len(analysis.hal_shiryan) > 0, "Hal-e-Shiryan missing")

        # Invariant check: AI diagnostics must NEVER automatically lock
        self.assertFalse(analysis.safe_to_lock, "CRITICAL INVARIANT VIOLATION: safe_to_lock must be False")
        self.assertIn("Balgham", analysis.inferred_su_e_mizaj)

    # -------------------------------------------------------------------------
    # PART 2: MULTISPECTRAL LISAN TONGUE CAMERA SENSOR
    # -------------------------------------------------------------------------
    def test_02_multispectral_lisan_camera_sensor(self):
        """Tests multispectral tongue inspection, CIE-Lab colorimetry, and 3-zone somatotopy."""
        switch_service("clinical")
        from app.hardware.tongue_multispectral_sensor import TongueMultispectralSensor, TongueScanResult

        sensor = TongueMultispectralSensor(device_id="LISAN-TEST-02")
        self.assertTrue(sensor.is_calibrated)
        self.assertGreater(sensor.led_illumination_cri, 95.0)

        # 1. Bilious / Safrawi scan simulation
        result_safrawi: TongueScanResult = sensor.scan_and_analyze(
            patient_id="PAT-SAFRAW-01",
            clinical_notes="Patient presents with bitter taste, yellow saburra on middle dorsum, dry mouth",
        )
        self.assertIn("Asfar", result_safrawi.coating_color)
        self.assertIn("Yabis", result_safrawi.moisture_status)
        self.assertIn("Safrawi", result_safrawi.inferred_humoral_dyscrasia)
        # 3-Zone Organ somatotopy
        self.assertIn("Kabid", result_safrawi.middle_zone_hepatogastric)
        self.assertFalse(result_safrawi.safe_to_lock, "safe_to_lock must be False")
        self.assertGreater(len(result_safrawi.suggested_tadbeer), 0)

        # 2. Phlegmatic / Balghami scan simulation
        result_balghami: TongueScanResult = sensor.scan_and_analyze(
            patient_id="PAT-BALGHAM-02",
            clinical_notes="Wet swollen tongue, thick white fur covering entire dorsal surface",
        )
        self.assertIn("Abyaz", result_balghami.coating_color)
        self.assertIn("Ratab", result_balghami.moisture_status)
        self.assertIn("Balghami", result_balghami.inferred_humoral_dyscrasia)
        self.assertFalse(result_balghami.safe_to_lock)

    # -------------------------------------------------------------------------
    # PART 3: WEARABLES BLE GATT GATEWAY
    # -------------------------------------------------------------------------
    def test_03_wearables_ble_gateway(self):
        """Tests BLE GATT ingestion, HRV metrics, and Quwwat-e-Hayawaniyyah vitality mapping."""
        switch_service("clinical")
        from app.hardware.wearables_ble_gateway import WearablesBleGateway, BleDeviceReading

        gateway = WearablesBleGateway(gateway_id="BLE-GW-TEST")
        # 1. Device pairing
        pair_res = gateway.pair_device(patient_id="PAT-WEAR-01", device_mac="EA:44:09:88:12:33")
        self.assertEqual(pair_res["status"], "PAIRED")
        self.assertEqual(pair_res["device_mac"], "EA:44:09:88:12:33")

        # 2. GATT packet ingestion
        reading: BleDeviceReading = gateway.ingest_gatt_packet(
            device_mac="EA:44:09:88:12:33",
            patient_id="PAT-WEAR-01",
            heart_rate=64,
            rr_interval=920,
            temp_c=36.7,
            spo2=98.5,
        )
        self.assertEqual(reading.heart_rate_bpm, 64)
        self.assertEqual(reading.rr_interval_ms, 920)
        self.assertGreater(reading.hrv_rmssd_ms, 20.0)
        self.assertGreater(reading.hrv_sdnn_ms, 30.0)
        self.assertEqual(reading.spo2_pct, 98.5)

        # 3. Quwwat-e-Hayawaniyyah vital force index computation
        vitality = gateway.compute_quwwat_hayawaniyyah_status(reading)
        self.assertIn("vital_force_score", vitality)
        self.assertGreaterEqual(vitality["vital_force_score"], 0)
        self.assertLessEqual(vitality["vital_force_score"], 100)
        self.assertIn("hararat_ghariziyyah_status", vitality)

    # -------------------------------------------------------------------------
    # PART 4: BOTANICAL QC NIR SPECTROMETER
    # -------------------------------------------------------------------------
    def test_04_botanical_qc_spectrometer_and_mudabbar(self):
        """Tests botanical spectrometry, heavy metals ICP-MS, and Schedule E(1) Mudabbar release."""
        switch_service("therapeutic")
        from app.hardware.botanical_qc_spectrometer import BotanicalQcSpectrometer, BotanicalSpectraReport

        spectrometer = BotanicalQcSpectrometer(spectrometer_id="NIR-TEST-99")

        # 1. Standard botanical: Asgandh (Withania somnifera)
        report_asgandh: BotanicalSpectraReport = spectrometer.scan_botanical_lot(
            botanical_name="Asgandh (Withania somnifera)",
            lot_number="LOT-ASG-2026-01",
        )
        self.assertTrue(report_asgandh.heavy_metals_passed)
        self.assertLess(report_asgandh.lead_pb_ppm, 0.05)
        self.assertLess(report_asgandh.arsenic_as_ppm, 0.05)
        self.assertTrue(report_asgandh.marker_spec_passed)
        self.assertGreaterEqual(report_asgandh.measured_concentration_pct, 2.50)
        self.assertEqual(report_asgandh.qc_disposition, "RELEASED_FOR_PRODUCTION")
        self.assertEqual(len(report_asgandh.certificate_of_analysis_hash), 64)

        # 2. Schedule E(1) Toxic Botanical: Azaraqi WITHOUT Mudabbar -> Must be QUARANTINED
        report_raw_azaraqi: BotanicalSpectraReport = spectrometer.scan_botanical_lot(
            botanical_name="Azaraqi (Strychnos nux-vomica)",
            lot_number="LOT-AZA-RAW-01",
            is_mudabbar_protocol_applied=False,
        )
        self.assertTrue(report_raw_azaraqi.is_schedule_e1)
        self.assertFalse(report_raw_azaraqi.mudabbar_detox_certified)
        self.assertFalse(report_raw_azaraqi.marker_spec_passed)
        self.assertIn("REJECTED", report_raw_azaraqi.qc_disposition)
        self.assertIn("Schedule E(1)", report_raw_azaraqi.qc_disposition)

        # 3. Schedule E(1) Botanical WITH Mudabbar Detoxification -> Must be RELEASED
        report_detox_azaraqi: BotanicalSpectraReport = spectrometer.scan_botanical_lot(
            botanical_name="Azaraqi Mudabbar (Purified Nux-vomica)",
            lot_number="LOT-AZA-MUD-02",
            is_mudabbar_protocol_applied=True,
        )
        self.assertTrue(report_detox_azaraqi.is_schedule_e1)
        self.assertTrue(report_detox_azaraqi.mudabbar_detox_certified)
        self.assertEqual(report_detox_azaraqi.qc_disposition, "RELEASED_FOR_PRODUCTION")

    # -------------------------------------------------------------------------
    # PART 5: COLD-CHAIN DISPENSARY ENVIRONMENTAL SENSOR
    # -------------------------------------------------------------------------
    def test_05_cold_chain_dispensary_sensor(self):
        """Tests pharmacy environmental temperature and humidity IoT telemetry."""
        switch_service("therapeutic")
        from app.hardware.cold_chain_dispensary_sensor import ColdChainDispensarySensor, EnvironmentalTelemetry

        sensor = ColdChainDispensarySensor(sensor_id="ENV-TEST-DISP")

        # 1. Optimal Storage Conditions (19.4°C, 48% RH)
        telemetry_opt: EnvironmentalTelemetry = sensor.read_environmental_telemetry(
            ambient_temp_override=19.4,
            ambient_rh_override=48.0,
        )
        self.assertTrue(telemetry_opt.is_temperature_compliant)
        self.assertTrue(telemetry_opt.is_humidity_compliant)
        self.assertEqual(telemetry_opt.fefo_storage_status, "OPTIMAL_PRESERVATION")
        self.assertEqual(len(telemetry_opt.active_alerts), 0)

        # 2. Thermal Excursion Warning (27.5°C, 65% RH)
        telemetry_warn: EnvironmentalTelemetry = sensor.read_environmental_telemetry(
            ambient_temp_override=27.5,
            ambient_rh_override=65.0,
        )
        self.assertFalse(telemetry_warn.is_temperature_compliant)
        self.assertFalse(telemetry_warn.is_humidity_compliant)
        self.assertEqual(telemetry_warn.fefo_storage_status, "THERMAL_EXCURSION_WARNING")
        self.assertGreater(len(telemetry_warn.active_alerts), 0)

        # 3. Critical Spoilage Risk (34.0°C)
        telemetry_crit: EnvironmentalTelemetry = sensor.read_environmental_telemetry(
            ambient_temp_override=34.0,
            ambient_rh_override=78.0,
        )
        self.assertEqual(telemetry_crit.fefo_storage_status, "CRITICAL_SPOILAGE_RISK")

    # -------------------------------------------------------------------------
    # PART 6: MOBILE OFFLINE STORAGE SERVICE & TELECONSULT
    # -------------------------------------------------------------------------
    def test_06_mobile_offline_service_and_components(self):
        """Validates mobile offline storage service, vernacular audio posology, and teleconsult room."""
        offline_service_path = os.path.join(BASE_DIR, "apps/mobile/src/services/OfflineStorageService.ts")
        self.assertTrue(os.path.exists(offline_service_path), "OfflineStorageService.ts missing")
        with open(offline_service_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("OfflineStorageService", content)
            self.assertIn("enqueueDirtyMutation", content)
            self.assertIn("syncCentralLedger", content)
            self.assertIn("isOnline", content)
            self.assertIn("clearQueue", content)

        # Audio posology player
        posology_path = os.path.join(BASE_DIR, "apps/mobile/src/components/AudioPosologyPlayer.tsx")
        self.assertTrue(os.path.exists(posology_path), "AudioPosologyPlayer.tsx missing")
        with open(posology_path, "r", encoding="utf-8") as f:
            pcontent = f.read()
            self.assertIn("AudioPosologyPlayer", pcontent)
            self.assertIn("Urdu", pcontent)
            self.assertIn("Hindi", pcontent)
            self.assertIn("English", pcontent)

        # TeleConsult Room
        teleconsult_path = os.path.join(BASE_DIR, "apps/mobile/src/screens/TeleConsultRoom.tsx")
        self.assertTrue(os.path.exists(teleconsult_path), "TeleConsultRoom.tsx missing")
        with open(teleconsult_path, "r", encoding="utf-8") as f:
            tcontent = f.read()
            self.assertIn("TeleConsultRoom", tcontent)
            self.assertIn("WebRTC", tcontent)
            self.assertIn("MIZAJ EVALUATION", tcontent)

        # Lifestyle Tracker with Meezan-e-Sehat 0-100
        lifestyle_path = os.path.join(BASE_DIR, "apps/mobile/src/screens/LifestyleTrackerScreen.tsx")
        self.assertTrue(os.path.exists(lifestyle_path), "LifestyleTrackerScreen.tsx missing")
        with open(lifestyle_path, "r", encoding="utf-8") as f:
            lcontent = f.read()
            self.assertIn("Meezan-e-Sehat", lcontent)
            self.assertIn("Asbab-e-Sittah", lcontent)

    # -------------------------------------------------------------------------
    # PART 7: WEB E-COMMERCE CART, CHECKOUT, AND RECEIPT
    # -------------------------------------------------------------------------
    def test_07_web_ecommerce_cart_and_checkout_engine(self):
        """Validates public website e-commerce cart, checkout with UPI/Card/COD, and product monographs."""
        cart_page_path = os.path.join(BASE_DIR, "apps/web/app/website/cart/page.tsx")
        self.assertTrue(os.path.exists(cart_page_path), "Cart page missing")
        with open(cart_page_path, "r", encoding="utf-8") as f:
            ccontent = f.read()
            self.assertIn("UNANI15", ccontent)
            self.assertIn("UPI", ccontent)
            self.assertIn("Card", ccontent)
            self.assertIn("COD", ccontent)
            self.assertIn("FEFO", ccontent)
            self.assertIn("Order Placed Successfully", ccontent)

        product_page_path = os.path.join(BASE_DIR, "apps/web/app/website/product/page.tsx")
        self.assertTrue(os.path.exists(product_page_path), "Product page missing")
        with open(product_page_path, "r", encoding="utf-8") as f:
            pcontent = f.read()
            # Monograph keys for all 10 products
            for prod_id in [
                "manivital-pro",
                "ovasync",
                "qurs-taqwiyat-mani",
                "metabocore-elite",
                "thyromet-axis",
                "liverprime-core",
                "neurocalmx",
                "nightone-x",
                "sleep-stress",
                "men-daily",
            ]:
                self.assertIn(prod_id, pcontent, f"Product monograph missing: {prod_id}")

    # -------------------------------------------------------------------------
    # PART 8: FASTAPI GATEWAY HARDWARE ENDPOINTS & PREVIEW HTML
    # -------------------------------------------------------------------------
    def test_08_hardware_gateway_and_preview_html_sync(self):
        """Validates that hardware REST endpoints are in launcher and preview HTML contains hardware lab."""
        launcher_path = os.path.join(BASE_DIR, "scripts/launch_zayvora_os.py")
        self.assertTrue(os.path.exists(launcher_path))
        with open(launcher_path, "r", encoding="utf-8") as f:
            lcontent = f.read()
            self.assertIn("/api/v1/hardware/nabz/stream", lcontent)
            self.assertIn("/api/v1/hardware/wearables/ble/sync", lcontent)
            self.assertIn("/api/v1/hardware/dispensary/cold-chain", lcontent)
            self.assertIn("/api/v1/hardware/tongue/analyze", lcontent)
            self.assertIn("/api/v1/hardware/botanical/qc-scan", lcontent)

        # Check PlatformHeader.tsx hardware status
        header_path = os.path.join(BASE_DIR, "apps/web/components/PlatformHeader.tsx")
        self.assertTrue(os.path.exists(header_path))
        with open(header_path, "r", encoding="utf-8") as f:
            hcontent = f.read()
            self.assertIn("Hardware Integration Architecture", hcontent)
            self.assertIn("Connected Devices: 0", hcontent)

        # Check docs/zayvora_health_os_preview.html Hardware Architecture
        preview_path = os.path.join(BASE_DIR, "docs/zayvora_health_os_preview.html")
        self.assertTrue(os.path.exists(preview_path))
        with open(preview_path, "r", encoding="utf-8") as f:
            pcontent = f.read()
            self.assertIn("Hardware Integration Architecture", pcontent)
            self.assertIn("Connected Devices: 0", pcontent)
            self.assertIn("renderHardwareApp", pcontent)
            self.assertIn("Arterial PPG", pcontent)
            self.assertIn("10-Ajnas Nabz", pcontent)
            self.assertIn("CIE-Lab", pcontent)
            self.assertIn("Dispensary Cold-Chain IoT", pcontent)

    # -------------------------------------------------------------------------
    # PART 9: RUNTIME DAEMON HARDWARE REST HANDLERS EXECUTION
    # -------------------------------------------------------------------------
    def test_09_runtime_daemon_hardware_endpoints_execution(self):
        """Validates in-memory execution of all 5 hardware REST endpoints in ZayvoraOSHandler."""
        import io
        from scripts.launch_zayvora_os import ZayvoraOSHandler, PlatformDatabase

        class MockServer:
            pass

        def make_handler(path: str, method: str = "GET", body: str = None) -> ZayvoraOSHandler:
            h = ZayvoraOSHandler.__new__(ZayvoraOSHandler)
            h.client_address = ("127.0.0.1", 12345)
            h.path = path
            h.command = method
            h.headers = {"Content-Length": str(len(body))} if body else {}
            h.rfile = io.BytesIO(body.encode() if body else b"")
            h.wfile = io.BytesIO()
            h.server = MockServer()
            h.server.db = PlatformDatabase()
            h.requestline = f"{method} {path} HTTP/1.1"
            h.request_version = "HTTP/1.1"
            return h

        # 1. Nabz Stream Endpoint
        h_nabz = make_handler("/api/v1/hardware/nabz/stream?duration=1.0")
        h_nabz.do_GET()
        res_nabz = h_nabz.wfile.getvalue().decode()
        self.assertIn("200 OK", res_nabz)
        self.assertIn("samples_count", res_nabz)
        self.assertIn("heart_rate_bpm", res_nabz)

        # 2. Wearables BLE Sync Endpoint
        h_ble = make_handler("/api/v1/hardware/wearables/ble/sync")
        h_ble.do_GET()
        res_ble = h_ble.wfile.getvalue().decode()
        self.assertIn("200 OK", res_ble)
        self.assertIn("quwwat_hayawaniyyah_index", res_ble)

        # 3. Dispensary Cold-Chain Endpoint
        h_cc = make_handler("/api/v1/hardware/dispensary/cold-chain")
        h_cc.do_GET()
        res_cc = h_cc.wfile.getvalue().decode()
        self.assertIn("200 OK", res_cc)
        self.assertIn("temperature_celsius", res_cc)
        self.assertIn("is_temperature_compliant", res_cc)

        # 4. Tongue Multispectral POST Endpoint
        h_tongue = make_handler(
            "/api/v1/hardware/tongue/analyze",
            method="POST",
            body=json.dumps({"patient_id": "PAT-774901", "clinical_notes": "yellow saburra, dry"})
        )
        h_tongue.do_POST()
        res_tongue = h_tongue.wfile.getvalue().decode()
        self.assertIn("200 OK", res_tongue)
        self.assertIn("coating_color", res_tongue)

        # 5. Botanical QC Spectrometer POST Endpoint
        h_botanical = make_handler(
            "/api/v1/hardware/botanical/qc-scan",
            method="POST",
            body=json.dumps({"botanical_name": "Withania somnifera", "lot_number": "BMR-2026-MVP-09"})
        )
        h_botanical.do_POST()
        res_botanical = h_botanical.wfile.getvalue().decode()
        self.assertIn("200 OK", res_botanical)
        self.assertIn("qc_disposition", res_botanical)
        self.assertIn("certificate_of_analysis_hash", res_botanical)


if __name__ == "__main__":
    unittest.main()
