# 🌱 Green Budget

### Give AI an environmental budget. Let it choose the model.

Green Budget is a lightweight AI model-selection tool that helps developers choose a model not only based on **accuracy**, but also on its **environmental impact**.

Instead of asking:

> *“Which model is the most accurate?”*

Green Budget asks:

> **“Which model is accurate enough while staying within my environmental budget?”**

---

## 💡 Why Green Budget?

AI systems consume resources at every stage — from training and inference to the infrastructure running them.

When choosing a model, accuracy is usually the first thing we look at. But a slightly more accurate model may also require significantly more energy and produce more carbon emissions.

Green Budget makes these trade-offs visible.

A user can set limits for:

* 🎯 Minimum accuracy
* 🌍 Maximum CO₂ emissions
* ⚡ Maximum energy consumption
* 💧 Maximum water usage

The system then checks the available model configurations and recommends the **lowest-impact option that still meets the required accuracy**.

---

## ⚙️ How it works

The process is simple:

```text
User sets environmental budget
            ↓
     Candidate models
            ↓
      Budget evaluation
            ↓
   Remove models that fail
            ↓
     Calculate Green Score
            ↓
   Recommend the best model
```

Accuracy is treated as a **hard requirement**, while CO₂, energy and water are used to compare the feasible models.

---

## 🧪 Example

Suppose a developer sets:

| Requirement      | Budget |
| ---------------- | -----: |
| Minimum Accuracy |    92% |
| Maximum CO₂      |   30 g |
| Maximum Energy   |  60 Wh |
| Maximum Water    |    5 L |

Green Budget evaluates different configurations:

| Configuration      | Accuracy |    CO₂ | Energy | Water |
| ------------------ | -------: | -----: | -----: | ----: |
| Baseline MLP       |    94.8% |   42 g |  82 Wh | 7.1 L |
| Quantized MLP      |    93.8% |   26 g |  54 Wh | 4.7 L |
| Feature-Pruned MLP |    93.2% | 24.5 g |  49 Wh | 4.3 L |
| Distilled MLP      |    91.7% |   19 g |  38 Wh | 3.4 L |

The baseline exceeds the environmental limits, while the distilled model does not meet the accuracy requirement.

So Green Budget recommends:

### 🏆 Feature-Pruned MLP

It meets the accuracy requirement while staying within all three environmental budgets.

---

## 🧠 Green Score

For the MVP, feasible configurations are ranked using a weighted environmental score:

```text
Green Score =
0.4 × normalized CO₂
+ 0.3 × normalized Energy
+ 0.3 × normalized Water
```

A **lower score means lower environmental impact** among the evaluated candidates.

The weights can be changed in future versions depending on the application's priorities.

---

## 🏗️ Project Structure

```text
GREEN-BUDGET-MVP/
│
├── app.py
│
├── backend/
│   ├── __init__.py
│   └── enginee.py
│
├── data/
│   └── model1.csv
│
├── requirements.txt
 
└── README.md
```

### What each part does

**`app.py`**
The Streamlit frontend and dashboard.

**`backend/enginee.py`**
Contains the model evaluation, budget filtering, Green Score calculation and recommendation logic.

**`data/model1.csv`**
Contains the candidate model configurations and their environmental metrics.

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** — interactive dashboard
* **Pandas** — data processing
* **Plotly** — visualizations
* **Git & GitHub** — version control

The MVP intentionally keeps the architecture lightweight so it can be demonstrated quickly and extended later.

---

## 🚀 Run it locally

### 1. Clone the repository

```bash
git clone https://github.com/shree895/GREEN-BUDGET-MVP.git
cd GREEN-BUDGET-MVP
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Install dependencies

On Windows:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Start the application

```powershell
.venv\Scripts\python.exe -m streamlit run app.py
```

The application will open locally in your browser.

---

## 🌍 Where this can go next

This MVP is only the starting point.

Future versions could include:

* Real-time energy measurements
* Hardware-level telemetry
* Regional carbon-intensity data
* Water-stress-aware calculations
* Cloud cost alongside environmental cost
* More ML optimization techniques
* Automatic model profiling
* API/CLI support
* CI/CD integration

For example:

```text
GREEN-BUDGET-MVP evaluate model1.py
```

could eventually evaluate a model automatically before deployment.

---

## ⚠️ About the environmental numbers

The environmental values used in this MVP are **benchmark/estimated inputs created for demonstration purposes**.

They should not be interpreted as universally measured emissions.

A production version would use measured workload data together with documented assumptions such as hardware, runtime, electricity mix, cooling and regional factors.

---

## 🎯 The idea in one line

> **Green Budget turns sustainability from a reporting metric into a model-selection decision.**

Instead of choosing the most accurate model and measuring its environmental impact afterwards, we want developers to consider environmental constraints **before making the decision**.

---

## 👥 Built for Rethink 26

**Green Budget** was developed as a hackathon MVP for **Rethink 26**.

The goal was to build a simple but extensible demonstration of how environmental constraints can become part of everyday AI engineering decisions.

---

### 🌱 Build smarter. Stay within the budget. Go greener.

**Built by Shree Sinha & Kunjan Sharma.**
