#!/bin/bash

# URL de destino
URL="ec2-3-83-246-89.compute-1.amazonaws.com:1234"  # Cambia esto por la URL de tu API

# JSON_DATA01 (Tipo 1)
JSON_DATA01=$(cat <<EOF
{
  "type": 1,
  "video_name": "parking_lot_video_1",
  "environment_type": "parking_lot",
  "object_name": null,
  "color": null,
  "proximity": null
}
EOF
)

# Enviar JSON_DATA01 a la URL
response01=$(curl -X POST "$URL/receive_characteristics" -H "Content-Type: application/json" -d "$JSON_DATA01")
echo "Respuesta para JSON_DATA01: $response01"

# JSON_DATA02 (Tipo 2)
JSON_DATA02=$(cat <<EOF
{
  "type": 2,
  "video_name": "parking_lot_video_2",
  "environment_type": "parking_lot",
  "object_name": "car",
  "color": "red",
  "proximity": "close"
}
EOF
)

# Enviar JSON_DATA02 a la URL
response02=$(curl -X POST "$URL/receive_characteristics" -H "Content-Type: application/json" -d "$JSON_DATA02")
echo "Respuesta para JSON_DATA02: $response02"

# JSON_DATA03 (Tipo 3)
JSON_DATA03=$(cat <<EOF
{
  "type": 3,
  "video_name": "parking_lot_video_3",
  "environment_type": "parking_lot",
  "object_name": "bike",
  "color": null,
  "proximity": null
}
EOF
)

# Enviar JSON_DATA03 a la URL
response03=$(curl -X POST "$URL/receive_characteristics" -H "Content-Type: application/json" -d "$JSON_DATA03")
echo "Respuesta para JSON_DATA03: $response03"

# JSON_DATA04 (Tipo 2)
JSON_DATA04=$(cat <<EOF
{
  "type": 2,
  "video_name": "umbrella_video_1",
  "environment_type": "outdoor",
  "object_name": "umbrella",
  "color": "gray",
  "proximity": "near"
}
EOF
)

# Enviar JSON_DATA04 a la URL
response04=$(curl -X POST "$URL/receive_characteristics" -H "Content-Type: application/json" -d "$JSON_DATA04")
echo "Respuesta para JSON_DATA04: $response04"

# JSON_DATA05 (Tipo 2)
JSON_DATA05=$(cat <<EOF
{
  "type": 2,
  "video_name": "umbrella_video_2",
  "environment_type": "beach",
  "object_name": "umbrella",
  "color": "gray",
  "proximity": "near"
}
EOF
)

# Enviar JSON_DATA05 a la URL
response05=$(curl -X POST "$URL/receive_characteristics" -H "Content-Type: application/json" -d "$JSON_DATA05")
echo "Respuesta para JSON_DATA05: $response05"

# JSON_DATA06 (Tipo 2)
JSON_DATA06=$(cat <<EOF
{
  "type": 2,
  "video_name": "umbrella_video_3",
  "environment_type": "park",
  "object_name": "umbrella",
  "color": "gray",
  "proximity": "near"
}
EOF
)

# Enviar JSON_DATA06 a la URL
response06=$(curl -X POST "$URL/receive_characteristics" -H "Content-Type: application/json" -d "$JSON_DATA06")
echo "Respuesta para JSON_DATA06: $response06"

# JSON_DATA07 (Tipo 2) - Con "object_count"
JSON_DATA07=$(cat <<EOF
{
  "type": 2,
  "video_name": "umbrella_video_1",
  "environment_type": "outdoor",
  "object_name": "umbrella",
  "color": "gray",
  "proximity": "near",
  "object_count": 5
}
EOF
)

# Enviar JSON_DATA07 a la URL
response07=$(curl -X POST "$URL/receive_characteristics" -H "Content-Type: application/json" -d "$JSON_DATA07")
echo "Respuesta para JSON_DATA07: $response07"

# JSON_DATA08 (Tipo 2) - Con "object_count"
JSON_DATA08=$(cat <<EOF
{
  "type": 2,
  "video_name": "umbrella_video_2",
  "environment_type": "beach",
  "object_name": "umbrella",
  "color": "gray",
  "proximity": "near",
  "object_count": 3
}
EOF
)

# Enviar JSON_DATA08 a la URL
response08=$(curl -X POST "$URL/receive_characteristics" -H "Content-Type: application/json" -d "$JSON_DATA08")
echo "Respuesta para JSON_DATA08: $response08"

# JSON_DATA09 (Tipo 2) - Con "object_count"
JSON_DATA09=$(cat <<EOF
{
  "type": 2,
  "video_name": "umbrella_video_3",
  "environment_type": "city",
  "object_name": "umbrella",
  "color": "gray",
  "proximity": "near",
  "object_count": 10
}
EOF
)

# Enviar JSON_DATA09 a la URL
response09=$(curl -X POST "$URL/receive_characteristics" -H "Content-Type: application/json" -d "$JSON_DATA09")
echo "Respuesta para JSON_DATA09: $response09"
