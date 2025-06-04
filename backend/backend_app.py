from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


def invalid_post(post):
    """
    checking if required fields are present, if not, return error msg
    """
    if "title" not in post and "content" not in post:
        return jsonify({"error": "Missing post title and content"}), 400
    if "title" not in post:
        return jsonify({"error": "Missing post title"}), 400
    if "content" not in post:
        return jsonify({"error": "Missing post content"}), 400
    else:
        return None


@app.route('/api/posts', methods=['POST'])
def add_new_post():
    """
    add a new blog post
    """
    new_post = request.get_json()

    # validate the new post's info
    if invalid_post(new_post):
        return invalid_post(new_post)

    # generate a new post id and add the new post to our database
    if len(POSTS) == 0:
        post_id = 1
    else:
        # get the id of the latest post and increment it by 1
        post_id = max(post["id"] for post in POSTS) + 1
        new_post["id"] = post_id
        POSTS.append(new_post)

    return jsonify(POSTS), 201


def find_post_by_id(post_id):
    """ find the post with the id 'post_id'
    If there is no post with this id, return None
    """
    for post in POSTS:
        if post["id"] == post_id:
            return post
    return None


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """
    delete post with id 'id'
    return success msg or error msg
    """
    post = find_post_by_id(id)
    if post is None:
        return jsonify({"error": "Post not found"}), 404
    else:
        POSTS.remove(post)
        return jsonify({"message": "Post with id <id> has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """
    update post with id 'id'
    title and content updates are both optional
    """
    post_to_update = find_post_by_id(id)
    if post_to_update is None:
        return jsonify({"error": "Post not found"}), 404
    else:
        updating_post = request.get_json()
        for post in POSTS:
            if post["id"] == post_to_update["id"]:
                if "title" in updating_post:
                    post["title"] = updating_post["title"]
                if "content" in updating_post:
                    post["content"] = updating_post["content"]
                return jsonify(updating_post), 200
        return jsonify({"error": "Post not found"}), 404



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
