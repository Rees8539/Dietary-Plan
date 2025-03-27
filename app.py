from flask import Flask, render_template, request, session
from ctransformers import AutoModelForCausalLM

app = Flask(__name__)
app.secret_key = "supersecretkey"  


llama_model_name = "TheBloke/Llama-2-7B-Chat-GGML"
model = AutoModelForCausalLM.from_pretrained(llama_model_name, model_type="llama", gpu_layers=0)

# Function to check if food is healthy or not
def check_food_health(food):
    unhealthy_foods = ["pizza", "burger", "fries", "soda", "cake", "chips"]
    if food.lower() in unhealthy_foods:
        return f"{food} is unhealthy. Try to eat it in moderation!"
    return f"{food} is healthy! Keep it up!"

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    query_response = ""

    
    if "set_preferences" in request.form:
        session["goal"] = request.form["goal"]
        session["dietary_restrictions"] = request.form["dietary_restrictions"]
        session["preferences"] = request.form["preferences"]

    if "check_food" in request.form:
        food = request.form["food"]
        result = check_food_health(food)

    if "ask_ai" in request.form:
        query = request.form["query"]

        
        preferences = session.get("preferences", "None")
        dietary_restrictions = session.get("dietary_restrictions", "None")
        goal = session.get("goal", "None")

        prompt = f"""
        User Preferences: {preferences}
        Dietary Restrictions: {dietary_restrictions}
        Health Goal: {goal}

        User: {query}
        AI:"""

        query_response = model(prompt)

    return render_template("index.html", result=result, query_response=query_response)

if __name__ == "__main__":
    app.run(debug=True)