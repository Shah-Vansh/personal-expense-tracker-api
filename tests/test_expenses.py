import pytest

def test_get_expenses_empty(client):
    response = client.get("/expenses")

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["data"]["count"] == 0
    assert data["data"]["expenses"] == []


def test_create_expense(client):
    payload = {
        "amount": "250.00",
        "category": "Food",
        "date": "2026-10-24",
        "description": "Lunch"
    }

    response = client.post(
        "/expenses",
        json=payload
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["success"] is True
    assert data["data"]["category"] == "Food"
    assert data["data"]["amount"] == "250.00"
    assert data["data"]["description"] == "Lunch"
    assert "id" in data["data"]

def test_create_expense_invalid_amount(client):
    payload = {
        "amount": "-100.00",
        "category": "Food",
        "date": "2026-10-24",
        "description": "Invalid expense"
    }

    response = client.post(
        "/expenses",
        json=payload
    )

    assert response.status_code in (400, 422)

    data = response.get_json()

    assert data["success"] is False

def test_get_expense_by_id(client):
    payload = {
        "amount": "500.00",
        "category": "Travel",
        "date": "2026-10-25",
        "description": "Bus ticket"
    }

    create_response = client.post(
        "/expenses",
        json=payload
    )

    assert create_response.status_code == 201

    expense_id = create_response.get_json()["data"]["id"]

    response = client.get(f"/expenses/{expense_id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["data"]["id"] == expense_id
    assert data["data"]["category"] == "Travel"
    assert data["data"]["amount"] == "500.00"

def test_get_expense_not_found(client):
    response = client.get("/expenses/999999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["success"] is False
    assert data["error"] is not None

def test_update_expense(client):
    payload = {
        "amount": "500.00",
        "category": "Travel",
        "date": "2026-10-25",
        "description": "Bus ticket"
    }

    create_response = client.post(
        "/expenses",
        json=payload
    )

    assert create_response.status_code == 201

    expense_id = create_response.get_json()["data"]["id"]

    update_payload = {
        "amount": "750.00",
        "category": "Transport",
        "date": "2026-10-26",
        "description": "Train ticket"
    }

    response = client.put(
        f"/expenses/{expense_id}",
        json=update_payload
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["data"]["amount"] == "750.00"
    assert data["data"]["category"] == "Transport"
    assert data["data"]["description"] == "Train ticket"

    get_response = client.get(f"/expenses/{expense_id}")

    assert get_response.status_code == 200
    assert get_response.get_json()["data"]["amount"] == "750.00"

def test_delete_expense(client):
    payload = {
        "amount": "300.00",
        "category": "Food",
        "date": "2026-10-25",
        "description": "Dinner"
    }

    create_response = client.post(
        "/expenses",
        json=payload
    )

    assert create_response.status_code == 201

    expense_id = create_response.get_json()["data"]["id"]

    response = client.delete(f"/expenses/{expense_id}")

    assert response.status_code in (200, 204)

    get_response = client.get(f"/expenses/{expense_id}")

    assert get_response.status_code == 404

def test_filter_expenses_by_category(client):
    expenses = [
        {
            "amount": "250.00",
            "category": "Food",
            "date": "2026-10-24",
            "description": "Lunch"
        },
        {
            "amount": "350.00",
            "category": "Travel",
            "date": "2026-10-25",
            "description": "Bus"
        },
        {
            "amount": "150.00",
            "category": "Food",
            "date": "2026-10-26",
            "description": "Dinner"
        }
    ]

    for expense in expenses:
        response = client.post("/expenses", json=expense)
        assert response.status_code == 201

    response = client.get("/expenses?category=Food")

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["data"]["count"] == 2
    assert len(data["data"]["expenses"]) == 2

    for expense in data["data"]["expenses"]:
        assert expense["category"] == "Food"

def test_expense_pagination(client):
    for i in range(5):
        payload = {
            "amount": "100.00",
            "category": "Food",
            "date": "2026-10-25",
            "description": f"Expense {i + 1}"
        }

        response = client.post("/expenses", json=payload)
        assert response.status_code == 201

    response = client.get("/expenses?page=2&limit=2")

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["page"] == 2
    assert data["limit"] == 2
    assert data["total"] == 5
    assert data["total_pages"] == 3
    assert data["count"] == 2
    assert len(data["expenses"]) == 2

    assert data["expenses"][0]["description"] == "Expense 3"
    assert data["expenses"][1]["description"] == "Expense 4"

def test_monthly_expense_summary(client):
    expenses = [
        {
            "amount": "250.00",
            "category": "Food",
            "date": "2026-10-24",
            "description": "Lunch"
        },
        {
            "amount": "350.50",
            "category": "Travel",
            "date": "2026-10-25",
            "description": "Bus"
        },
        {
            "amount": "100.00",
            "category": "Food",
            "date": "2026-10-26",
            "description": "Dinner"
        },
        {
            "amount": "500.00",
            "category": "Shopping",
            "date": "2026-09-20",
            "description": "Clothes"
        }
    ]

    for expense in expenses:
        response = client.post("/expenses", json=expense)
        assert response.status_code == 201

    response = client.get(
        "/expenses/summary/monthly?year=2026&month=10"
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["year"] == 2026
    assert data["month"] == 10
    assert data["total"] == "700.50"
    assert data["transaction_count"] == 3

    categories = {
        item["category"]: item
        for item in data["categories"]
    }

    assert categories["Food"]["count"] == 2
    assert categories["Food"]["total"] == "350.00"

    assert categories["Travel"]["count"] == 1
    assert categories["Travel"]["total"] == "350.50"

    assert "Shopping" not in categories

@pytest.mark.parametrize(
    "query",
    [
        "page=0&limit=10",
        "page=-1&limit=10",
        "page=abc&limit=10",
        "page=1&limit=0",
        "page=1&limit=101",
    ]
)
def test_invalid_pagination(client, query):
    response = client.get(f"/expenses?{query}")

    assert response.status_code in (400, 422)

    data = response.get_json()

    assert data["success"] is False
    assert data["error"] is not None

@pytest.mark.parametrize(
    "query",
    [
        "start_date=invalid-date",
        "end_date=2026-15-10",
        "start_date=2026-10-30&end_date=2026-10-01",
    ]
)
def test_invalid_date_filters(client, query):
    response = client.get(f"/expenses?{query}")

    assert response.status_code in (400, 422)

    data = response.get_json()

    assert data["success"] is False
    assert data["error"] is not None

@pytest.mark.parametrize(
    "query",
    [
        "year=2026&month=0",
        "year=2026&month=13",
        "year=abc&month=10",
        "year=2026",
        "month=10",
    ]
)
def test_invalid_monthly_summary(client, query):
    response = client.get(
        f"/expenses/summary/monthly?{query}"
    )

    assert response.status_code in (400, 422)

    data = response.get_json()

    assert data["success"] is False
    assert data["error"] is not None

def test_filter_expenses_by_date_range(client):
    expenses = [
        {
            "amount": "100.00",
            "category": "Food",
            "date": "2026-10-10",
            "description": "Breakfast"
        },
        {
            "amount": "200.00",
            "category": "Travel",
            "date": "2026-10-20",
            "description": "Bus"
        },
        {
            "amount": "300.00",
            "category": "Shopping",
            "date": "2026-10-30",
            "description": "Clothes"
        }
    ]

    for expense in expenses:
        response = client.post("/expenses", json=expense)
        assert response.status_code == 201

    response = client.get(
        "/expenses?start_date=2026-10-15&end_date=2026-10-25"
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["count"] == 1
    assert data["expenses"][0]["category"] == "Travel"
    assert data["expenses"][0]["amount"] == "200.00"

def test_pagination_out_of_range(client):
    response = client.get("/expenses?page=100&limit=10")

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["count"] == 0
    assert data["total"] == 0
    assert data["expenses"] == []

def test_empty_monthly_summary(client):
    response = client.get(
        "/expenses/summary/monthly?year=2026&month=12"
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["year"] == 2026
    assert data["month"] == 12
    assert data["total"] == "0.00"
    assert data["transaction_count"] == 0
    assert data["categories"] == []
