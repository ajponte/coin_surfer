#!/usr/bin/env bash

uvicorn server.app:create_app --host localhost --port 5003 --reload --factory
