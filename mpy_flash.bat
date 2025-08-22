.venv\Scripts\activate.bat
esptool erase_flash
esptool --baud 460800 write_flash 0 ESP32_GENERIC_S3-20250415-v1.25.0.bin