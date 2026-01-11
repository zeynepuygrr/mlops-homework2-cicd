@echo off
REM Build script for Docker image (Windows version)
REM This script packages the model and serving code into a deployable container

set IMAGE_NAME=avazu-ctr-api
set IMAGE_TAG=%IMAGE_TAG%
if "%IMAGE_TAG%"=="" set IMAGE_TAG=latest

echo Building Docker image: %IMAGE_NAME%:%IMAGE_TAG%

docker build -t %IMAGE_NAME%:%IMAGE_TAG% .

if %ERRORLEVEL% EQU 0 (
    echo Docker image built successfully: %IMAGE_NAME%:%IMAGE_TAG%
    echo Built image details:
    docker images %IMAGE_NAME%:%IMAGE_TAG%
) else (
    echo Docker build failed!
    exit /b 1
)

