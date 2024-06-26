import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load the dataset
data = load_breast_cancer()
X = data.data[:, :2]  # Use only the first two features for visualization purposes
y = data.target

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

print("X_train.shape: ", X_train.shape)
print("X_test.shape: ", X_test.shape)
print("y_train.shape: ", y_train.shape)
print("y_test.shape: ", y_test.shape)

# Standardize the dataset
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Implement logistic regression from scratch
class LogisticRegression:
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.weights = None
        self.bias = None

        print(type(learning_rate))
        print(type(iterations))

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        n_samples, n_features = X.shape  # X'in satır ve sütun sayısını elde eder
        self.weights = np.zeros(n_features)  # Özellik sayısına göre sıfırlardan oluşan ağırlık vektörü oluşturur
        self.bias = 0  # Bias'ı sıfıra eşitler


        print("n_samples: ", n_samples)
        print("n_features: ", n_features)
        print("weights: ", self.weights)
        print("bias: ", self.bias)
        print("X.shape: ", X.shape)
        print("y.shape: ", y.shape)

        for _ in range(self.iterations):
            linear_model = np.dot(X, self.weights) + self.bias  #modelin tahminlerini yapabilmesi için gerekli olan doğrusal kombinasyon hesaplanması ve
            y_predicted = self.sigmoid(linear_model)            #tahmin edilen değerlerin sigmoid fonksiyonuna sokulması

            dw = (1 / n_samples) * np.dot(X.T, (y_predicted - y))  #?? ----- gradientdescent
            db = (1 / n_samples) * np.sum(y_predicted - y)         #her bir iterasyonda modelin tahminleri ile gerçek değerler arasındaki
                                                                   #hatayı minimize etmek için ağırlıklar ve kesişim terimi güncellenir

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X):
        linear_model = np.dot(X, self.weights) + self.bias
        y_predicted = self.sigmoid(linear_model)
        y_predicted_cls = [1 if i > 0.5 else 0 for i in y_predicted]
        return np.array(y_predicted_cls)

# Train the model
model = LogisticRegression(learning_rate=0.1, iterations=1000) #learning_rate, her iterasyonda ağırlıkların ne kadar güncelleneceğini belirler
model.fit(X_train, y_train)

# Predict on test set
predictions = model.predict(X_test)

# Calculate accuracy
accuracy = np.mean(predictions == y_test)
print(f"Accuracy: {accuracy:.4f}")

# Visualize the results with a single decision boundary line
def plot_decision_boundary(X, y, model):
    # Get the weights and bias
    w = model.weights
    b = model.bias

    # Plot the data points
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', marker='o', cmap=plt.cm.RdYlBu)

    # Plot the decision boundary line
    x_values = [X[:, 0].min(), X[:, 0].max()]   # x0 (ilk özellik) için minimum ve maksimum değerler
    y_values = -(w[0] * np.array(x_values) + b) / w[1]  # x1 (ikinci özellik) için karar sınırı değerleri
    plt.plot(x_values, y_values, label='Decision Boundary', color='black')

    print("x_values: ", x_values)
    print("y_values: ", y_values)
    print("weights: ", w)
    print(w.shape)
    print("bias: ", b)

    plt.xlabel(data.feature_names[0])
    plt.ylabel(data.feature_names[1])
    plt.title('Logistic Regression Decision Boundary')
    plt.legend()
    plt.show()

# Visualize the decision boundary for the breast cancer dataset
plot_decision_boundary(X_test, y_test, model)
