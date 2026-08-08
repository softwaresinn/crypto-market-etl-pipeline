# Crypto Market ELT Pipeline

An end-to-end cryptocurrency market data ELT pipeline built with Python and PostgreSQL, with FastAPI providing access to curated market data.

The project implements a layered **Bronze → Silver → Gold** architecture for ingesting, storing, transforming, validating, and serving cryptocurrency market data from external APIs.

---

## Overview

The **Crypto Market ELT Pipeline** is a data engineering project designed to demonstrate a production-oriented approach to cryptocurrency data processing.

The pipeline extracts cryptocurrency market and futures data from external APIs and first loads the original source payloads into a PostgreSQL **Bronze** layer. The raw data is then transformed and cleaned into structured **Silver** datasets. Finally, the Silver data is further transformed into curated **Gold** datasets optimized for downstream analytics and application consumption.

A **FastAPI** application provides a controlled REST interface over the Gold layer.

The project follows clear separation of concerns between:

- Data ingestion
- Database persistence
- Data transformation
- Database schema management
- API serving
- Configuration and logging

The architecture is designed to be extensible toward orchestration, distributed processing, cloud infrastructure, streaming, automated testing, and data quality tooling.

---

## Key Features

- Multi-source cryptocurrency data ingestion
- Bronze → Silver → Gold layered architecture
- Raw JSON/JSONB payload preservation
- PostgreSQL-based ELT processing
- SQL-based data transformations
- Cryptocurrency market metrics processing
- Binance Futures metadata processing
- Data normalization and validation
- Nullable field handling
- Duplicate prevention
- Transaction-safe database operations
- Repository-based database access
- FastAPI REST API
- Modular project structure
- Clear separation of ingestion, transformation, and serving layers

---

## Architecture

```text
                         External APIs
                    ┌────────────────────┐
                    │  CoinMarketCap     │
                    │  Binance Futures   │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │     Ingestion      │
                    │   Python Clients   │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │      BRONZE        │
                    │                    │
                    │   Raw API Payloads │
                    │      JSON/JSONB    │
                    └─────────┬──────────┘
                              │
                              │ Transform
                              ▼
                    ┌────────────────────┐
                    │      SILVER        │
                    │                    │
                    │ Cleaned & Structured│
                    │       Data         │
                    └─────────┬──────────┘
                              │
                              │ Transform
                              ▼
                    ┌────────────────────┐
                    │       GOLD         │
                    │                    │
                    │ Curated & Serving  │
                    │       Data         │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │      FastAPI       │
                    │     REST API       │
                    └────────────────────┘
