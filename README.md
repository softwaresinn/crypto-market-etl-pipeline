# Crypto Market ELT Pipeline

An end-to-end cryptocurrency market data ELT pipeline built with Python, PostgreSQL, and FastAPI.

The project ingests raw cryptocurrency market data from external APIs, stores the original payloads in a Bronze layer, transforms and cleans the data into Silver tables, and produces business-ready Gold datasets that can be consumed through REST APIs.

---

## Architecture

```text
External APIs
     │
     ▼
┌─────────────────────┐
│     Ingestion       │
│  Binance / CMC API  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       Bronze        │
│    Raw JSON Data    │
│    PostgreSQL       │
└──────────┬──────────┘
           │
           │ Transform
           ▼
┌─────────────────────┐
│       Silver        │
│ Cleaned & Structured│
│        Data         │
└──────────┬──────────┘
           │
           │ Transform / Aggregate
           ▼
┌─────────────────────┐
│        Gold         │
│ Business-Ready Data │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      FastAPI        │
│     REST API        │
└─────────────────────┘
