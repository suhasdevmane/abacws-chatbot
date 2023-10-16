@echo off
:loop
ping -n 1 timescaledb > nul
if %errorlevel% neq 0 (
  timeout /t 5 /nobreak
  goto loop
)

psql -h timescaledb -U postgres -d thingsboard -W -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"

echo TimescaleDB extension has been created.

/usr/share/thingsboard/bin/run.sh
