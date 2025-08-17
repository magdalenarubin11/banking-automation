import random
from faker import Faker

from src.pages.home_page import HomePage
from src.pages.manager_page import ManagerPage
from src.pages.customer_login_page import CustomerLoginPage

fake = Faker("pl_PL")

def test_banking_e2e(driver, base_url):
    first = fake.first_name()
    last  = fake.last_name()
    post  = f"{random.randint(10,99)}-{random.randint(100,999)}"
    display_name = f"{first} {last}"

    deposit_amounts = [100, 50, 25]
    withdraw_amounts = [40, 30]
    currency = "Dollar"

    HomePage(driver).open(base_url).go_manager()

    manager = ManagerPage(driver)
    alert_text = manager.add_customer(first, last, post)
    assert alert_text and "Customer added successfully" in alert_text

    alert_text = manager.open_account(display_name, currency=currency)
    assert alert_text and "Account created successfully" in alert_text

    manager.go_home()

    HomePage(driver).go_customer()
    account = CustomerLoginPage(driver).login_as(display_name)

    for amt in deposit_amounts:
        msg = account.deposit(amt)
        assert "Deposit Successful" in msg

    for amt in withdraw_amounts:
        msg = account.withdraw(amt)
        assert "Transaction successful" in msg

    tx = account.go_transactions()
    data = tx.get_transactions()
    assert data is not None and len(data) > 0  # sanity check

    deposited = sum(d["amount"] for d in data if d["type"].lower().startswith("credit"))
    withdrawn = sum(d["amount"] for d in data if d["type"].lower().startswith("debit"))
    assert deposited >= sum(deposit_amounts)
    assert withdrawn >= sum(withdraw_amounts)

    print(f"Customer: {display_name} | Currency: {currency}")
    print(f"Deposits: {deposit_amounts} -> recorded >= {deposited}")
    print(f"Withdrawals: {withdraw_amounts} -> recorded >= {withdrawn}")
    print("Transactions page is visible. Browser remains open by default.")
