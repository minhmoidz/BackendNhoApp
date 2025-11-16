project/
│
├── main.py                          # Entry point
├── requirements.txt                 # Dependencies
├── .env                            # Environment variables
├── .env.example                    # Template
├── README.md                       # Documentation
│
├── app/
│   ├── __init__.py
│   ├── config.py                   # Cấu hình
│   ├── models.py                   # Data models
│   ├── database.py                 # Storage layer
│   ├── routes.py                   # API endpoints
│   ├── app.py                      # FastAPI setup
│   ├── server.py                   # Server startup
│   │
│   └── services/
│       ├── __init__.py
│       ├── ai_service.py           # AI Intelligence
│       └── ocr_service.py          # OCR
│
└── storage/                        # Data storage
    ├── diaries.json
    ├── notes.json
    ├── reminders.json
    ├── memories.json
    ├── user_profile.json
    ├── health_logs.json
    └── conversations.json
