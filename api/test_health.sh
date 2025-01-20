#!/usr/bin/env bash


# test the health route
curl -X 'GET' \
  'http://localhost:5003/api/health' \
  -H 'accept: application/json'
