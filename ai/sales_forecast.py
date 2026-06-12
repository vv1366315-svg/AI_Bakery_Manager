from sklearn.linear_model import LinearRegression


def predict_sales(sales_quantities):

    # Need at least 2 data points
    if len(sales_quantities) < 2:
        return sales_quantities[0] if sales_quantities else 0

    X = []
    y = []

    for i, quantity in enumerate(sales_quantities):
        X.append([i + 1])
        y.append(quantity)

    model = LinearRegression()

    model.fit(X, y)

    next_day = [[len(X) + 1]]

    prediction = model.predict(next_day)

    return max(0, round(prediction[0]))