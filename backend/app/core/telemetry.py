import logging
import sys
from fastapi import FastAPI
from pythonjsonlogger import jsonlogger
from app.core.config import settings
from app.core.logging_context import request_id_ctx_var

# Check for OpenTelemetry dependencies
try:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    HAS_OTEL = True
except ImportError:
    HAS_OTEL = False


class CorrelationIdFilter(logging.Filter):
    """Logging filter that injects the active async request correlation ID into log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        # Retrieve context-active request ID, fallback to empty string if not in request thread
        record.request_id = request_id_ctx_var.get() or ""
        return True


def setup_logging() -> None:
    """Configures structured JSON logging with request ID correlation support."""
    root_logger = logging.getLogger()

    # Reset existing log handlers
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)

    # Register request trace filter
    correlation_filter = CorrelationIdFilter()
    handler.addFilter(correlation_filter)

    # Standardize on Structured JSON logging across environments to facilitate cloud aggregations
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s",
        rename_fields={"levelname": "severity", "asctime": "timestamp"},
    )

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Resolve log level configuration
    log_level = logging.DEBUG if settings.debug else logging.INFO
    root_logger.setLevel(log_level)

    # Limit verbose libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    logging.info(
        f"Structured JSON logging active. Level: {logging.getLevelName(log_level)}"
    )


def setup_telemetry(app: FastAPI) -> None:
    """Initializes OpenTelemetry trace exporter configurations."""
    if not settings.telemetry.enabled:
        logging.info("OpenTelemetry tracing is disabled by configuration.")
        return

    if not HAS_OTEL:
        logging.warning("OpenTelemetry SDK packages not installed. Tracing skipped.")
        return

    try:
        resource = Resource.create(
            attributes={
                "service.name": settings.telemetry.service_name,
                "deployment.environment": settings.env,
            }
        )

        provider = TracerProvider(resource=resource)
        exporter = OTLPSpanExporter(
            endpoint=settings.telemetry.otlp_endpoint, insecure=True
        )
        processor = BatchSpanProcessor(exporter)
        provider.add_span_processor(processor)

        trace.set_tracer_provider(provider)
        FastAPIInstrumentor.instrument_app(app)

        logging.info(
            f"OpenTelemetry successfully instrumented for service: {settings.telemetry.service_name}"
        )
    except Exception as e:
        logging.error(f"Failed to initialize OpenTelemetry: {e}", exc_info=True)
