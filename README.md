# YSB_WikiPage (Assignment)

## Setup

---

1. Run MySQL DB Server via Docker or whatever
2. Conduct either action for **required settings** (Refer to app.configs.Settings for further information)
    - Put local.env file on the root path
    - Set environment variables
3. Execute below command lines
    - > $ pip install -r requirements.txt
    - > $ uvicorn app.main:app --reload

## Testing

---

- > $ pytest
