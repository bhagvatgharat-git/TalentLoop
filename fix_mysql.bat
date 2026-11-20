@echo off
echo ==============================================
echo TalentLoop - Fixing MySQL Service Permissions
echo ==============================================
echo.

echo 1. Stopping any lingering MySQL processes...
taskkill /f /im mysqld.exe 2>nul

echo 2. Taking ownership of MySQL Data directory...
takeown /f "C:\ProgramData\MySQL\MySQL Server 8.0\Data" /r /d y

echo 3. Granting permissions to NETWORK SERVICE and Administrators...
icacls "C:\ProgramData\MySQL\MySQL Server 8.0\Data" /grant "NT AUTHORITY\NETWORK SERVICE":(OI)(CI)F /t
icacls "C:\ProgramData\MySQL\MySQL Server 8.0\Data" /grant "Administrators":(OI)(CI)F /t

echo 4. Removing corrupted binlog files...
del /f /q "C:\ProgramData\MySQL\MySQL Server 8.0\Data\ASUSS14-bin.*" 2>nul

echo 5. Starting MySQL80 service...
net start MySQL80

echo.
sc query MySQL80
echo.
echo ==============================================
echo If STATE is RUNNING above, MySQL is started!
echo ==============================================
pause

