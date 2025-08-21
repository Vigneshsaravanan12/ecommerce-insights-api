from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import os

app = FastAPI(title="Ecommerce Insights API")

# ----------------------------
# Safe CSV Loader
# ----------------------------
def load_csv_safe(file_name):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        return pd.DataFrame()

sales_insights = load_csv_safe("sales_insights.csv")
top_products = load_csv_safe("top_products.csv")
top_customers = load_csv_safe("top_customers.csv")
category_sales = load_csv_safe("category_sales.csv")
mba_apriori = load_csv_safe("mba_rules_apriori.csv")
mba_fpgrowth = load_csv_safe("mba_rules_fpgrowth.csv")
reviews_sentiment = load_csv_safe("reviews_with_sentiment_final.csv")
product_summaries = load_csv_safe("product_summaries.csv")

# ----------------------------
# Root
# ----------------------------
@app.get("/")
def read_root():
    return {"message": "🚀 Ecommerce Insights API is running! Visit /docs for JSON endpoints or /dashboard for HTML view."}

# ----------------------------
# JSON API Endpoints
# ----------------------------
@app.get("/sales_insights")
def get_sales_insights():
    return sales_insights.to_dict(orient="records")

@app.get("/top_products")
def get_top_products():
    return top_products.to_dict(orient="records")

@app.get("/top_customers")
def get_top_customers():
    return top_customers.to_dict(orient="records")

@app.get("/category_sales")
def get_category_sales():
    return category_sales.to_dict(orient="records")

@app.get("/mba_apriori")
def get_mba_apriori():
    return mba_apriori.to_dict(orient="records")

@app.get("/mba_fpgrowth")
def get_mba_fpgrowth():
    return mba_fpgrowth.to_dict(orient="records")

@app.get("/reviews_sentiment")
def get_reviews_sentiment():
    return reviews_sentiment.to_dict(orient="records")

@app.get("/product_summaries")
def get_product_summaries():
    return product_summaries.to_dict(orient="records")

# ----------------------------
# Dashboard (HTML View)
# ----------------------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    html = """
    <html>
    <head>
        <title>Ecommerce Insights API</title>
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
        <h1>📊 Ecommerce Insights API</h1>
    """

    def df_to_html(title, df):
        if df.empty:
            return f"<h2>{title}</h2><p>No data available</p>"
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
