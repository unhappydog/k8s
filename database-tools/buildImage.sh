#!/usr/bin/env bash

./gradlew install && docker build -t dbtool .
