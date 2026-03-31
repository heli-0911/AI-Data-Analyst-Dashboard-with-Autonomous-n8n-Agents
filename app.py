from flask import Flask, request, jsonify, send_file
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Load dataset
df = pd.read_csv("data.csv")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        query = data.get("query", "").lower()

        # =========================
        # 1. Top rows
        # =========================
        if "top" in query or "first" in query:
            result = df.head(5).to_dict(orient="records")

            return jsonify({
                "type": "table",
                "result": result,
                "explanation": "Showing first 5 rows of dataset"
            })

        # =========================
        # 2. Churn rate
        # =========================
        elif "churn rate" in query:
            churn = (df["Churn"].value_counts(normalize=True) * 100).round(2).to_dict()

            explanation = f"""
            - {churn.get('Yes',0)}% customers have churned.
            - {churn.get('No',0)}% customers are retained.
            """

            return jsonify({
                "type": "text",
                "result": churn,
                "explanation": explanation
            })

        # =========================
        # 3. Average monthly charges
        # =========================
        elif "average" in query:
            avg = round(df["MonthlyCharges"].mean(), 2)

            return jsonify({
                "type": "text",
                "result": avg,
                "explanation": f"Average monthly charges are ₹{avg}"
            })

        # =========================
        # 4. Total customers
        # =========================
        elif "total customers" in query:
            total = len(df)

            return jsonify({
                "type": "text",
                "result": total,
                "explanation": f"Total number of customers is {total}"
            })

        # =========================
        # 5. Churn by contract
        # =========================
        elif "contract" in query:
            contract = df.groupby("Contract")["Churn"].value_counts().to_dict()

            return jsonify({
                "type": "text",
                "result": contract,
                "explanation": "Churn distribution across contract types"
            })

        # =========================
        # 6. Summary statistics
        # =========================
        elif "summary" in query or "describe" in query:
            summary = df.describe().to_dict()

            return jsonify({
                "type": "text",
                "result": summary,
                "explanation": "Statistical summary of dataset"
            })

        # =========================
        # 7. Chart: Churn distribution
        # =========================
        elif "chart" in query or "graph" in query:
            plt.figure()
            df["Churn"].value_counts().plot(kind="bar", color=["green", "red"])
            plt.title("Churn Distribution")
            plt.xlabel("Churn")
            plt.ylabel("Count")

            chart_path = "chart.png"
            plt.savefig(chart_path)
            plt.close()

            return jsonify({
                "type": "chart",
                "chart": chart_path,
                "explanation": "Bar chart showing churn distribution"
            })

        # =========================
        # 8. Smart recommendation
        # =========================
        elif "why churn" in query or "reason churn" in query:
            return jsonify({
                "type": "text",
                "result": "Customers with higher monthly charges and short-term contracts are more likely to churn.",
                "explanation": "High cost and lack of long-term commitment increases churn risk."
            })

        # =========================
        # Default fallback
        # =========================
        else:
            return jsonify({
                "type": "text",
                "result": "Query not supported yet",
                "explanation": "Try asking about churn rate, average charges, or charts"
            })

    except Exception as e:
        return jsonify({"error": str(e)})


# =========================
# Route to serve chart image
# =========================
@app.route("/chart", methods=["GET"])
def get_chart():
    if os.path.exists("chart.png"):
        return send_file("chart.png", mimetype="image/png")
    else:
        return jsonify({"error": "No chart available"})


# =========================
# Run app
# =========================
if __name__ == "__main__":
    app.run(port=5000, debug=True)