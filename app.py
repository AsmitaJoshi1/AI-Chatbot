from flask import Flask, request, jsonify, render_template
import markdown
from graph import graph
from models import ChatRequest

app = Flask(__name__)


@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate the input using Pydantic
        chat_request = ChatRequest(**data)

        # Send validated message to LangGraph
        result = graph.invoke({
            "user_message": chat_request.user_message,
            "response": ""
        })

        # Convert Markdown response to HTML
        response_html = markdown.markdown(
            result["response"],
            extensions=["tables", "fenced_code"]
        )

        # Return AI response
        return jsonify({
            "response": response_html
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400
@app.route("/", methods=["GET"])
def home():
   return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)