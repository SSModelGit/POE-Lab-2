#!/bin/bash
platformio run --target upload
platformio device monitor > logFile.csv
