#!/bin/bash
uvicorn bot_webhook:fast_app --host 0.0.0.0 --port $PORT
