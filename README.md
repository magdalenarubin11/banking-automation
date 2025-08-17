# Banking E2E Automation (XYZ Bank – GlobalSQA)

End‑to‑end UI automation in **Python + Selenium + pytest** that performs the exact recruitment task:

1) Wejście na stronę: https://www.globalsqa.com/angularJs-protractor/BankingProject/
2) a. Zaloguj się jako bank (Bank Manager Login)
   b. Dodaj klienta
   c. Przejdź do otwarcia konta
   d. Wybierz dodanego klienta i otwórz jego konto w dowolnej walucie
   e. Wróć na stronę główną
   f. Zaloguj się jako nowo dodany klient
   g. Dodaj kilka transakcji wpłat
   h. Dodaj kilka transakcji wypłat
   i. Przejdź na stronę spisu transakcji (przeglądarka może pozostać otwarta)

## Szybki start (PyCharm / lokalnie)

1. **Wymagania**
   - Python 3.10+
   - Google Chrome
   - Internet access
2. **Instalacja**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Uruchomienie testu**
   ```bash
   pytest -q tests/test_banking_e2e.py -s
   ```
   Flaga `-s` pokaże komunikaty/printy.

### Tryb headless (CI) i pozostawianie przeglądarki otwartej
- Uruchom w trybie **headless**:
  ```bash
  HEADLESS=true pytest -q tests/test_banking_e2e.py
  ```
- Pozostaw **otwartą przeglądarkę po teście** (np. do oceny przez rekrutera):
  ```bash
  KEEP_BROWSER_OPEN=true pytest -q tests/test_banking_e2e.py -s
  ```
  > Gdy `KEEP_BROWSER_OPEN=true`, driver **nie** zostanie zamknięty po teście.

## Struktura projektu
```text
banking-automation/
├─ README.md
├─ requirements.txt
├─ pytest.ini
├─ conftest.py
├─ src/
│  ├─ utils/
│  │  └─ helpers.py
│  └─ pages/
│     ├─ home_page.py
│     ├─ manager_page.py
│     ├─ open_account_page.py
│     ├─ customer_login_page.py
│     ├─ account_page.py
│     └─ transactions_page.py
└─ tests/
   └─ test_banking_e2e.py
```
