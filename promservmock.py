from prometheus_client import start_http_server, Counter, Gauge, Histogram, Summary
import random
import time

# Verschiedene Metriken anlegen
REQUEST_COUNTER = Counter(
    "demo_requests_total", 
    "Zählt die Anzahl Requests", 
    ["method", "endpoint"]
)

TEMPERATURE_GAUGE = Gauge(
    "demo_temperature_celsius", 
    "Aktuelle Temperatur in Celsius", 
    ["location"]
)

RESPONSE_TIME_HISTOGRAM = Histogram(
    "demo_response_seconds", 
    "Antwortzeiten in Sekunden",
    buckets=[0.1, 0.3, 1, 2, 5]
)

DB_QUERY_SUMMARY = Summary(
    "demo_db_query_seconds", 
    "Zusammenfassung der DB-Query Zeiten"
)

def generate_metrics():
    # Counter mit zufälligen Labels
    REQUEST_COUNTER.labels(
        method=random.choice(["GET", "POST", "PUT", "DELETE"]),
        endpoint=random.choice(["/api/v1/data", "/api/v1/login", "/api/v1/status"])
    ).inc()

    # Gauge mit Schwankungen
    TEMPERATURE_GAUGE.labels(location=random.choice(["zurich", "bern", "basel"])) \
        .set(random.uniform(15, 30))

    # Histogram und Summary füllen
    val = random.expovariate(1/0.5)  # Exponential verteilt um 0.5s
    RESPONSE_TIME_HISTOGRAM.observe(val)
    DB_QUERY_SUMMARY.observe(val * random.uniform(0.5, 1.5))


if __name__ == "__main__":
    # Startet Prometheus HTTP-Server auf Port 8000
    start_http_server(8000)
    print("Prometheus Demo läuft auf :8000/metrics")

    while True:
        generate_metrics()
        time.sleep(1)
