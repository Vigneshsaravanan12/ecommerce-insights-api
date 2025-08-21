from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd

app = FastAPI(title="Ecommerce Insights API")

# Load CSV outputs
sales_insights = pd.read_csv("sales_insights.csv")
top_products = pd.read_csv("top_products.csv")
top_customers = pd.read_csv("top_customers.csv")
category_sales = pd.read_csv("category_sales.csv")
mba_apriori = pd.read_csv("mba_rules_apriori.csv")
mba_fpgrowth = pd.read_csv("mba_rules_fpgrowth.csv")
reviews_sentiment = pd.read_csv("reviews_with_sentiment_final.csv")
product_summaries = pd.read_csv("product_summaries.csv")

@app.get("/")
def read_root():
    return {"message": "🚀 Ecommerce Insights API is running! Visit /docs for endpoints or /dashboard for full view."}

# ---------- Custom All-in-One Page ----------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    html = """
    <html>
    <head>
        <title>Ecommerce Insights Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h2 { color: #2E86C1; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 30px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>📊 Ecommerce Insights</h1>
    """
    datasets = [
        ("Sales Insights", sales_insights),
        ("Top Products", top_products),
        ("Top Customers", top_customers),
        ("Category Sales", category_sales),
        ("MBA - Apriori Rules", mba_apriori),
        ("MBA - FP-Growth Rules", mba_fpgrowth),
        ("Review Sentiments", reviews_sentiment),
        ("Product Summaries", product_summaries)
    ]

    for title, df in datasets:
        html += f"<h2>{title}</h2>"
        html += df.head(10).to_html(index=False)  # show first 10 rows for readability

    html += """
    </body>
    </html>
    """
    return html
