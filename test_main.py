from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

VALID_TRANSACTION = {
    "amt": 120.50,
    "category": "grocery_pos",
    "hour": 23,
    "age": 34,
    "city_pop": 50000,
}


def test_predict_returns_expected_fields():
    """A valid transaction should return exactly the two fields the frontend uses."""
    response = client.post("/predict", json=VALID_TRANSACTION)

    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {"is_fraud", "fraud_probability"}
    assert isinstance(body["is_fraud"], bool)
    assert isinstance(body["fraud_probability"], float)


def test_probability_is_between_zero_and_one():
    """A probability outside 0 to 1 would mean something is broken in the model pipeline."""
    response = client.post("/predict", json=VALID_TRANSACTION)

    probability = response.json()["fraud_probability"]
    assert 0.0 <= probability <= 1.0


def test_same_input_gives_same_output():
    """The model should be deterministic: identical input, identical answer."""
    first = client.post("/predict", json=VALID_TRANSACTION).json()
    second = client.post("/predict", json=VALID_TRANSACTION).json()

    assert first == second


def test_unknown_category_does_not_crash():
    """A category the model never saw in training should still get a prediction."""
    transaction = {**VALID_TRANSACTION, "category": "not_a_real_category"}
    response = client.post("/predict", json=transaction)

    assert response.status_code == 200


def test_missing_field_is_rejected():
    """Leaving out a required field should return a validation error, not a crash."""
    incomplete = {key: value for key, value in VALID_TRANSACTION.items() if key != "amt"}
    response = client.post("/predict", json=incomplete)

    assert response.status_code == 422


def test_wrong_type_is_rejected():
    """Text where a number belongs should return a validation error."""
    bad = {**VALID_TRANSACTION, "amt": "not a number"}
    response = client.post("/predict", json=bad)

    assert response.status_code == 422
