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

# NEW: Business Recommendations
recs_apriori = pd.read_csv("business_recommendations_apriori.csv")
recs_fpgrowth = pd.read_csv("business_recommendations_fpgrowth.csv")

# ----------------------------
# Helper: safe JSON conversion
# ----------------------------
def safe_json(df):
    """Convert DataFrame to JSON-safe dict (convert sets/lists to strings)."""
    df = df.copy()
    for col in df.columns:
        df[col] = df[col].apply(lambda x: str(x))
    return df.to_dict(orient="records")

# ----------------------------
# Root
# ----------------------------
@app.get("/")
def read_root():
    return {"message": "🚀 Ecommerce Insights API is running! Visit /docs for endpoints or /dashboard for full view."}

# ----------------------------
# JSON API Endpoints
# ----------------------------
@app.get("/sales_insights")
def get_sales_insights():
    return safe_json(sales_insights)

@app.get("/top_products")
def get_top_products():
    return safe_json(top_products)

@app.get("/top_customers")
def get_top_customers():
    return safe_json(top_customers)

@app.get("/category_sales")
def get_category_sales():
    return safe_json(category_sales)

@app.get("/mba_apriori")
def get_mba_apriori():
    return safe_json(mba_apriori)
    
# NEW: JSON Endpoints for Business Recommendations
@app.get("/business_recommendations_apriori")
def get_recs_apriori():
    return safe_json(recs_apriori)

@app.get("/mba_fpgrowth")
def get_mba_fpgrowth():
    return safe_json(mba_fpgrowth)

@app.get("/business_recommendations_fpgrowth")
def get_recs_fpgrowth():
    return safe_json(recs_fpgrowth)

@app.get("/reviews_sentiment")
def get_reviews_sentiment():
    return safe_json(reviews_sentiment)

@app.get("/product_summaries")
def get_product_summaries():
    return safe_json(product_summaries)

# ----------------------------
# Dashboard route (HTML)
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
        <h1>📊 Ecommerce Insights API Dashboard </h1>
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
    html += df_to_html("Business Recommendations (Apriori)", recs_apriori)
    html += df_to_html("Business Recommendations (FP-Growth)", recs_fpgrowth)

    html += "</body></html>"
    return html
