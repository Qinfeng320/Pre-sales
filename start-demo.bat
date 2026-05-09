@echo off
cd /d "%~dp0demo"
start http://localhost:3000/policy_collector.html
npx serve . -p 3000
