from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd

app = FastAPI(title="Ecommerce Insights API")

# ----------------------------
# Load CSV outputs
# ----------------------------
sales_insights = pd.read_csv("sales_insights.csv")
top_products = pd.read_csv("top_products.csv")
top_customers = pd.read_csv("top_customers.csv")
category_sales = pd.read_csv("category_sales.csv")
mba_apriori = pd.read_csv("mba_rules_apriori.csv")
mba_fpgrowth = pd.read_csv("mba_rules_fpgrowth.csv")
reviews_sentiment = pd.read_csv("reviews_with_sentiment_final.csv")
product_summaries = pd.read_csv("product_summaries.csv")

# ----------------------------
# Root
# ----------------------------
@app.get("/")
def read_root():
    return {"message": "🚀 Ecommerce Insights API is running! Visit /docs for endpoints or /dashboard for full view."}

# ----------------------------
# Dashboard route
# ----------------------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    html = """
    <html>
    <head>
        <title>Ecommerce Insights Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h2 { color: #2c3e50; margin-top: 40px; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 40px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #2c3e50; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>📊 Ecommerce Insights Dashboard</h1>
    """

    def df_to_html(title, df):
        return f"<h2>{title}</h2>" + df.head(10).to_html(index=False, escape=False)

    html += df_to_html("Sales Insights", sales_insights)
    html += df_to_html("Top Products", top_products)
    html += df_to_html("Top Customers", top_customers)
    html += df_to_html("Category Sales", category_sales)
    html += df_to_html("Market Basket Analysis (Apriori)", mba_apriori)
    html += df_to_html("Market Basket Analysis (FP-Growth)", mba_fpgrowth)
    html += df_to_html("Review Sentiments", reviews_sentiment)
    html += df_to_html("Product Summaries", product_summaries)

    html += "</body></html>"
    return html
