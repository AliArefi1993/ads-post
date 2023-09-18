from fastapi.testclient import TestClient
from app.db.database import SessionLocal
from app.db import models
from app.main import app
from passlib.context import CryptContext

client = TestClient(app)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def test_get_comments():
    response = client.get("/comment")
    assert response.status_code == 200


def test_get_comment_detail():
    db = SessionLocal()
    test_comment = models.Comment(text="Test Comment")
    db.add(test_comment)
    db.commit()

    response = client.get(f"/comment/{test_comment.id}")

    assert response.status_code == 200

    response_json = response.json()
    assert "id" in response_json
    assert "text" in response_json

    db.delete(test_comment)
    db.commit()
    db.close()


def test_get_ads():
    response = client.get("/ads")
    assert response.status_code == 200


def test_get_user():
    response = client.get("/user")
    assert response.status_code == 200


def test_login_user():
    password = "test"
    email = "test6@test.com"
    hashed_password = get_password_hash(password)
    data = {"email": email,
            "hashed_password": hashed_password}

    db = SessionLocal()
    test_user = models.User(**data)
    db.add(test_user)
    db.commit()
    user_info = {"username": email,
                 "password": password}
    response = client.post("/token", data=user_info)
    assert response.status_code == 200

    response_json = response.json()
    assert "access_token" in response_json

    user_info = {"username": "wrong@wrong.com",
                 "password": "wrong_pass"}
    response = client.post("/token", data=user_info)

    db.delete(test_user)
    db.commit()
    db.close()
    assert response.status_code == 401


def test_post_ads():
    password = "test"
    email = "test14@test.com"
    hashed_password = get_password_hash(password)
    data = {"email": email,
            "hashed_password": hashed_password}

    db = SessionLocal()
    test_user = models.User(**data)
    db.add(test_user)
    db.commit()
    user_info = {"username": email,
                 "password": password}
    ads_data = {
        "title": "new",
        "text": "the",
        "pic_path": "empthy",
    }
    response = client.post("/token", data=user_info)
    response_json = response.json()
    access_token = response_json.get("access_token")

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/ads", json=ads_data, headers=headers)
    # assert response.status_code == 200
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code}. Response JSON: {response.json()}"

    db.delete(test_user)
    db.commit()
    db.close()


def test_post_comment():
    password = "test"
    email = "test15@test.com"
    hashed_password = get_password_hash(password)
    data = {"email": email,
            "hashed_password": hashed_password}

    db = SessionLocal()
    test_user = models.User(**data)
    db.add(test_user)
    db.commit()
    user_info = {"username": email,
                 "password": password}
    response = client.post("/token", data=user_info)
    response_json = response.json()
    access_token = response_json.get("access_token")

    ads_data = {
        "title": "new shoe test",
        "text": "the best",
        "pic_path": "empthy",
    }

    db = SessionLocal()
    test_ads = models.Ads(**ads_data)
    db.add(test_ads)
    db.commit()

    comment_data = {
        "text": "test comment",
        "ads_id": test_ads.id
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/comment", json=comment_data, headers=headers)
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code}. Response JSON: {response.json()}"

    db.delete(test_user)
    db.commit()

    db.delete(test_ads)
    db.commit()
    db.close()


def test_post_user():

    user_data = {
        "email": "testnew2@test.com",
        "full_name": "test",
        "disabled": True,
        "password": "test_pass"
    }
    response = client.post("/user", json=user_data)
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code}. Response JSON: {response.json()}"
    db = SessionLocal()
    response_json = response.json()

    user = db.query(models.User).filter(
        models.User.id == response_json.get("id")).first()
    db.delete(user)
    db.commit()
    db.close()


def test_delete_user():
    password = "test"
    email = "test_delet10@test.com"
    hashed_password = get_password_hash(password)
    data = {"email": email,
            "hashed_password": hashed_password}

    db = SessionLocal()
    test_user = models.User(**data)
    db.add(test_user)
    db.commit()

    user_info = {"username": email,
                 "password": password}
    response = client.post("/token", data=user_info)
    response_json = response.json()
    access_token = response_json.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.delete(f"/user/{test_user.id}", headers=headers)
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code}. Response JSON: {response.json()}"

    response = client.delete(f"/user/{test_user.id}")
    assert response.status_code == 401, f"Expected status code 401 but received {response.status_code}. Response JSON: {response.json()}"


def test_delete_ads():
    password = "test"
    email = "test_delet7@test.com"
    hashed_password = get_password_hash(password)
    data = {"email": email,
            "hashed_password": hashed_password}

    db = SessionLocal()
    test_user = models.User(**data)
    db.add(test_user)
    db.commit()

    ads_data = {
        "title": "new shoe test",
        "text": "the best",
        "pic_path": "empthy",
        "owner_id": test_user.id
    }
    test_ads = models.Ads(**ads_data)
    db.add(test_ads)
    db.commit()

    user_info = {"username": email,
                 "password": password}
    response = client.post("/token", data=user_info)
    response_json = response.json()
    access_token = response_json.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.delete(f"/ads/{test_ads.id}", headers=headers)
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code}. Response JSON: {response.json()}"

    response = client.delete(f"/ads/{test_ads.id}")
    assert response.status_code == 401, f"Expected status code 200 but received {response.status_code}. Response JSON: {response.json()}"

    db.delete(test_user)
    db.commit()
    db.close()


def test_delete_comments():
    password = "test"
    email = "testdeletcomment@test.com"
    hashed_password = get_password_hash(password)
    data = {"email": email,
            "hashed_password": hashed_password}

    db = SessionLocal()
    test_user = models.User(**data)
    db.add(test_user)
    db.commit()

    ads_data = {
        "title": "new shoe test",
        "text": "the best",
        "pic_path": "empthy",
        "owner_id": test_user.id
    }
    test_ads = models.Ads(**ads_data)
    db.add(test_ads)
    db.commit()

    comment_data = {
        "text": "the best ever",
        "ads_id": test_ads.id,
        "owner_id": test_user.id
    }
    test_comment = models.Comment(**comment_data)
    db.add(test_comment)
    db.commit()

    user_info = {"username": email,
                 "password": password}
    response = client.post("/token", data=user_info)
    response_json = response.json()
    access_token = response_json.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.delete(f"/comment/{test_comment.id}", headers=headers)
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code}. Response JSON: {response.json()}"

    response = client.delete(f"/comment/{test_comment.id}")
    assert response.status_code == 401, f"Expected status code 401 but received {response.status_code}. Response JSON: {response.json()}"

    db.delete(test_user)
    db.commit()
    db.close()


def test_put_user():
    password = "test"
    email = "test_delet11@test.com"
    hashed_password = get_password_hash(password)
    data = {"email": email,
            "hashed_password": hashed_password}

    db = SessionLocal()
    test_user = models.User(**data)
    db.add(test_user)
    db.commit()

    user_info = {"username": email,
                 "password": password}
    response = client.post("/token", data=user_info)
    response_json = response.json()
    access_token = response_json.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    user_new_data = {"email@my_new_email2.com": email,
                     "password": "new_pass"}
    response = client.put(f"/user/{test_user.id}",
                          headers=headers, json=user_new_data)
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code}. Response JSON: {response.json()}"

    response = client.put(f"/user/{test_user.id}", json=user_new_data)
    assert response.status_code == 401, f"Expected status code 401 but received {response.status_code}. Response JSON: {response.json()}"

    db.delete(test_user)
    db.commit()
    db.close()


def test_put_ads():
    password = "test"
    email = "test_delet7@test.com"
    hashed_password = get_password_hash(password)
    data = {"email": email,
            "hashed_password": hashed_password}

    db = SessionLocal()
    test_user = models.User(**data)
    db.add(test_user)
    db.commit()

    ads_data = {
        "title": "new shoe test",
        "text": "the best",
        "pic_path": "empthy",
        "owner_id": test_user.id
    }
    test_ads = models.Ads(**ads_data)
    db.add(test_ads)
    db.commit()

    user_info = {"username": email,
                 "password": password}
    response = client.post("/token", data=user_info)
    response_json = response.json()
    access_token = response_json.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    ads_new_data = {
        "title": "new shoe test edited",
        "text": "the best edited",
        "pic_path": "empthy edited",
        "owner_id": test_user.id
    }
    response = client.put(f"/ads/{test_ads.id}",
                          headers=headers, json=ads_new_data)
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code}. Response JSON: {response.json()}"

    response = client.put(f"/ads/{test_ads.id}", json=ads_new_data)
    assert response.status_code == 401, f"Expected status code 200 but received {response.status_code}. Response JSON: {response.json()}"

    db.delete(test_user)
    db.commit()
    db.close()


def test_put_comments():
    password = "test"
    email = "testputcomment@testnew.com"
    hashed_password = get_password_hash(password)
    data = {"email": email,
            "hashed_password": hashed_password}

    db = SessionLocal()
    test_user = models.User(**data)
    db.add(test_user)
    db.commit()

    ads_data = {
        "title": "new shoe test",
        "text": "the best",
        "pic_path": "empthy",
        "owner_id": test_user.id
    }
    test_ads = models.Ads(**ads_data)
    db.add(test_ads)
    db.commit()

    comment_data = {
        "text": "the best ever",
        "ads_id": test_ads.id,
        "owner_id": test_user.id
    }
    test_comment = models.Comment(**comment_data)
    db.add(test_comment)
    db.commit()

    user_info = {"username": email,
                 "password": password}
    response = client.post("/token", data=user_info)
    response_json = response.json()
    access_token = response_json.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    comment_new_data = {
        "text": "the best ever new data",
        "ads_id": test_ads.id,
    }

    response = client.put(
        f"/comment/{test_comment.id}", headers=headers, json=comment_new_data)
    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code}. Response JSON: {response.json()}"

    response = client.put(f"/comment/{test_comment.id}", json=comment_new_data)
    assert response.status_code == 401, f"Expected status code 401 but received {response.status_code}. Response JSON: {response.json()}"

    db.delete(test_user)
    db.commit()
    db.close()
