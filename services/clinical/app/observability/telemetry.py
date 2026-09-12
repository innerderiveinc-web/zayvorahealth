"""
ZAYVORA HEALTH™ — Enterprise APM, OpenTelemetry & Prometheus Observability
Provides W3C trace context propagation, distributed span tracking, and Prometheus metrics scraping.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class TraceSpan:
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    service_name: str
    operation_name: str
    start_time: float
    end_time: Optional[float] = None
    status_code: str = "OK"
    attributes: Dict[str, Any] = field(default_factory=dict)


class TelemetryRegistry:
    """In-memory Prometheus metrics collector and OpenTelemetry span tracker."""

    def __init__(self):
        # Metrics storage
        self.request_counts: Dict[str, int] = defaultdict(int)
        self.latency_buckets: Dict[str, Dict[float, int]] = defaultdict(lambda: defaultdict(int))
        self.safety_blocks: Dict[str, int] = defaultdict(int)
        self.predictive_alerts: Dict[str, int] = defaultdict(int)
        self.active_spans: List[TraceSpan] = []

    def record_request(self, method: str, path: str, status_code: int, duration_sec: float):
        key = f'{method}:{path}:{status_code}'
        self.request_counts[key] += 1

        # Buckets for latency histogram: 0.05, 0.1, 0.25, 0.5, 1.0, 2.5
        buckets = [0.05, 0.1, 0.25, 0.5, 1.0, 2.5]
        for b in buckets:
            if duration_sec <= b:
                self.latency_buckets[path][b] += 1
        self.latency_buckets[path][float("inf")] += 1

    def record_safety_block(self, reason: str):
        self.safety_blocks[reason] += 1

    def record_predictive_alert(self, triage_band: str):
        self.predictive_alerts[triage_band] += 1

    @staticmethod
    def generate_w3c_traceparent() -> str:
        """Generates W3C compliant traceparent header."""
        trace_id = uuid.uuid4().hex
        span_id = uuid.uuid4().hex[:16]
        return f"00-{trace_id}-{span_id}-01"

    def start_span(
        self,
        operation_name: str,
        service_name: str = "clinical_service",
        parent_span_id: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> TraceSpan:
        span = TraceSpan(
            trace_id=uuid.uuid4().hex,
            span_id=uuid.uuid4().hex[:16],
            parent_span_id=parent_span_id,
            service_name=service_name,
            operation_name=operation_name,
            start_time=time.time(),
            attributes=attributes or {},
        )
        self.active_spans.append(span)
        return span

    def finish_span(self, span: TraceSpan, status_code: str = "OK"):
        span.end_time = time.time()
        span.status_code = status_code

    def export_prometheus_metrics(self) -> str:
        lines = [
            "# HELP zayvora_http_requests_total Total number of HTTP requests processed.",
            "# TYPE zayvora_http_requests_total counter",
        ]
        for key, count in sorted(self.request_counts.items()):
            parts = key.split(":")
            method, path, status = parts[0], parts[1], parts[2]
            lines.append(f'zayvora_http_requests_total{{method="{method}",path="{path}",status="{status}"}} {count}')

        lines.extend([
            "",
            "# HELP zayvora_safety_firewall_blocks_total Total number of safety firewall blocks.",
            "# TYPE zayvora_safety_firewall_blocks_total counter",
        ])
        for reason, count in sorted(self.safety_blocks.items()):
            lines.append(f'zayvora_safety_firewall_blocks_total{{reason="{reason}"}} {count}')

        lines.extend([
            "",
            "# HELP zayvora_predictive_alerts_total Total proactive relapse alerts by triage band.",
            "# TYPE zayvora_predictive_alerts_total counter",
        ])
        for band, count in sorted(self.predictive_alerts.items()):
            lines.append(f'zayvora_predictive_alerts_total{{triage_band="{band}"}} {count}')

        lines.append("")
        return "\n".join(lines)


GLOBAL_TELEMETRY = TelemetryRegistry()
