@echo off
setlocal ENABLEDELAYEDEXPANSION

REM MoMo Transactions API - curl test suite (Windows)
REM Prerequisites: Server running: uvicorn api.server:app --reload

set BASE_URL=http://127.0.0.1:8000
set USER=apiuser
set PASS=apipass

echo ==================================================
echo [A] GET /transactions - valid auth (expect 200)
echo ==================================================
curl -i -u %USER%:%PASS% %BASE_URL%/transactions

echo.
echo ==================================================
echo [B] GET /transactions - invalid auth (expect 401)
echo ==================================================
curl -i -u wrong:creds %BASE_URL%/transactions

echo.
echo ==================================================
echo [C] GET /transactions/1 - valid auth (expect 200 if seeded)
echo ==================================================
curl -i -u %USER%:%PASS% %BASE_URL%/transactions/1

echo.
echo ==================================================
echo [D] GET /transactions/9999 - valid auth (expect 404)
echo ==================================================
curl -i -u %USER%:%PASS% %BASE_URL%/transactions/9999

echo.
echo ==================================================
echo [E] POST /transactions - create id=2 (expect 201)
echo ==================================================
curl -i -u %USER%:%PASS% ^
  -H "Content-Type: application/json" ^
  -d "{\"transaction_id\": 2, \"sender_id\": 101, \"receiver_id\": 202, \"category_id\": 11, \"amount\": 250.75, \"transaction_date\": \"2024-06-01T10:00:00\", \"status\": \"PENDING\"}" ^
  %BASE_URL%/transactions

echo.
echo ==================================================
echo [F] PUT /transactions/2 - update (expect 200)
echo ==================================================
curl -i -u %USER%:%PASS% -X PUT ^
  -H "Content-Type: application/json" ^
  -d "{\"transaction_id\": 2, \"sender_id\": 101, \"receiver_id\": 202, \"category_id\": 11, \"amount\": 300.00, \"transaction_date\": \"2024-06-02T12:00:00\", \"status\": \"SUCCESS\"}" ^
  %BASE_URL%/transactions/2

echo.
echo ==================================================
echo [G] DELETE /transactions/2 - delete (expect 204)
echo ==================================================
curl -i -u %USER%:%PASS% -X DELETE %BASE_URL%/transactions/2

echo.
echo Done. Review outputs above. The server console also shows minimal access logs for /transactions*.
endlocal
