#!/bin/bash

# SSH sunucusunu başlatıyoruz
service ssh start

# Flask uygulamasını başlatıyoruz
python app.py
