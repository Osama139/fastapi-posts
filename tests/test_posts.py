import pytest

from app import models, schemas


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts")
    assert response.status_code == 200

def test_get_a_post(authorized_client, test_posts):
    response = authorized_client.get("/posts/1")
    assert response.status_code == 200

@pytest.mark.parametrize("title, content, published", [
    ("some title1", "some content1", True),
    ("some title2", "some content2", True),
    ("some title33", "some content3", False),
])
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post('/posts', json={
                                                      "title":title,
                                                      "content":content,
                                                      "published":published
                                                      }
                                      )
    new_post = schemas.PostOut(**response.json())
    assert new_post.user_id == test_user['id']
    assert response.status_code == 201


