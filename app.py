# app.py
from flask import Flask, request, jsonify, render_template
from executor import run_code_in_docker, ExecutionError, TIMEOUT_SECONDS

app = Flask(__name__)

MAX_CODE_LENGTH = 5000  # from the assignment


@app.route("/", methods=["GET"])
def index():
    # Simple HTML UI
    return render_template("index.html")


@app.route("/run", methods=["POST"])
def run_code():
    """
    JSON body: { "code": "print(2 + 2)" }
    Response:
      { "output": "4\n" }
    or on error:
      { "error": "Execution timed out after 10 seconds", "details": "..."}
    """
    data = request.get_json(silent=True)

    if not data or "code" not in data:
        return jsonify({"error": "Missing 'code' field in JSON body"}), 400

    code = data["code"]

    if not isinstance(code, str):
        return jsonify({"error": "'code' must be a string"}), 400

    if len(code) == 0:
        return jsonify({"error": "Code cannot be empty"}), 400

    if len(code) > MAX_CODE_LENGTH:
        return jsonify(
            {"error": f"Code is too long (max {MAX_CODE_LENGTH} characters)"}
        ), 400

    try:
        stdout, stderr = run_code_in_docker(code)
    except ExecutionError as e:
        # Polished, user-friendly error
        msg = str(e)
        status = 400

        if "timed out" in msg.lower():
            # Match the assignment text exactly:
            msg = f"Execution timed out after {TIMEOUT_SECONDS} seconds"

        return jsonify({"error": msg}), status

    # If stderr has content, treat it as an error from the user's code
    if stderr:
        return jsonify({"output": stdout, "error": stderr}), 200

    return jsonify({"output": stdout}), 200


if __name__ == "__main__":
    # Run dev server
    app.run(host="0.0.0.0", port=5000, debug=True)
