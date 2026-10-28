# 📊 Sales Analysis Dashboard

A clean, simple, and professional desktop **Sales Analysis Dashboard** created in Python for a college Data Analytics / Data Visualization project.

---

## 🌟 Project Overview

This project provides a simple, clean, and intuitive desktop dashboard to analyze and visualize sales performance. It was specifically designed to look like an authentic student project — clean, functional, easy to demonstrate in front of an examiner, and simple to explain line-by-line during a viva.

The application loads a realistic sales dataset from CSV, performs standard data cleaning with **Pandas**, calculates key summary metrics using **NumPy**, renders interactive charts with **Matplotlib**, and presents everything inside a straightforward **Tkinter** desktop interface.

---

## 🚀 Key Features

1. **Simple, Human-Designed GUI**:
   - Clean top header with project title & subtitle.
   - Horizontal filter bar with Category, Region, and Month dropdowns.
   - Summary cards displaying Total Revenue, Units Sold, Number of Products, Total Orders, and Average Order Value.
   - 3 clean tabs: **Visualizations**, **Area Chart & Statistics**, and **Data Records**.
   - A straightforward **Key Insights** section at the bottom.
2. **Visualizations (Matplotlib)**:
   - **Line Plot**: Shows monthly sales revenue trend over time.
   - **Area Chart**: Shows overall sales trend and cumulative volume over time using `np.cumsum()`.
   - **Bar Chart (Category)**: Compares sales revenue across product categories.
   - **Bar Chart (Regional)**: Compares sales performance across North, South, East, and West.
   - **Pie Chart**: Displays the percentage distribution of sales by category with clear percentages (`autopct='%1.1f%%'`).
3. **NumPy Implementation**:
   - `np.sum()`: Calculates total revenue and total quantity sold.
   - `np.mean()` & `np.median()`: Computes average order value and median transaction size.
   - `np.std()`: Calculates standard deviation of order values.
   - `np.min()` & `np.max()`: Identifies minimum and maximum single sales.
   - `np.cumsum()`: Computes cumulative sales array for the area chart.
   - `np.unique()`: Counts distinct products.
4. **Data Cleaning (Pandas)**:
   - Removes duplicate rows (`df.drop_duplicates()`).
   - Handles missing / NaN values (`df.dropna()`).
   - Trims whitespaces from text columns (`str.strip()`).
   - Standardizes date strings into datetime format (`pd.to_datetime()`).
   - Coerces Quantity and Revenue into numeric types (`pd.to_numeric()`).
5. **Interactive Controls**:
   - Category filter dropdown.
   - Region filter dropdown.
   - Month filter dropdown.
   - "Apply Filters", "Reset", and "Load CSV File" buttons.
   - Real-time status bar reporting data cleaning summary and row counts.

---

## 🛠️ Technologies Used

- **Python** (Programming language)
- **Tkinter** (Desktop GUI interface)
- **NumPy** (Numerical calculations and statistics)
- **Pandas** (Data loading, cleaning, and grouping)
- **Matplotlib** (Line, Area, Bar, and Pie charts)

---

## 📁 Project Structure

```text
sales_analysis_dashboard/
│
├── main.py                # Main application code (clean & readable)
├── generate_dataset.py    # Generates realistic sample sales dataset
├── sales_data.csv         # Sample sales dataset (850+ records)
├── requirements.txt       # Python dependencies
├── run_dashboard.bat      # One-click Windows runner
└── README.md              # Project guide & Viva questions
```

---

## ⚙️ How to Run in VS Code

1. Open **VS Code**.
2. Click **File** $\rightarrow$ **Open Folder...** and select `python project`.
3. Open `main.py` in the editor.
4. Click the **▶ (Play)** button at the top-right corner of VS Code (or open the terminal and type `python main.py`).

---

## 📘 Viva Questions & Answers (15-20 Questions)

### Q1: What is Sales Analysis?
**Answer:** It is the process of studying past sales records and revenues to assess business performance, discover seasonal trends, identify top products, and make informed business decisions.

### Q2: Why did we use NumPy?
**Answer:** NumPy provides fast, efficient numerical operations on arrays. We used:
- `np.sum()` for total revenue and quantity.
- `np.mean()` for average order value.
- `np.median()` for median sale amount.
- `np.std()` for standard deviation (sales dispersion).
- `np.min()` and `np.max()` for minimum and maximum transactions.
- `np.cumsum()` to calculate the cumulative revenue series for the Area Chart.

### Q3: Why did we use Pandas?
**Answer:** Pandas is used for handling tabular datasets:
- Reading CSV files with `pd.read_csv()`.
- Data cleaning: removing duplicates (`drop_duplicates()`), handling missing values (`dropna()`), and string trimming.
- Converting dates using `pd.to_datetime()`.
- Grouping data by Category, Region, and Month using `df.groupby()`.

### Q4: Why did we use Matplotlib?
**Answer:** Matplotlib creates standard, customizable charts (Line plot, Area chart, Bar charts, and Pie chart) and embeds easily into Tkinter using `FigureCanvasTkAgg`.

### Q5: Why did we use Tkinter?
**Answer:** Tkinter is Python's standard built-in GUI library. It requires no heavy external web servers, starts up fast, and provides native desktop widgets like buttons, comboboxes, and notebook tabs.

### Q6: What is data cleaning and what did we clean?
**Answer:** Data cleaning prepares raw data for analysis:
1. Removed duplicate records.
2. Dropped rows missing critical values (Revenue and Quantity).
3. Stripped extra whitespaces from text columns.
4. Converted dates to standard datetime objects.
5. Ensured Quantity and Revenue are proper numbers.

### Q7: What is a line plot?
**Answer:** A line plot connects data points chronologically to show trends over time. In our dashboard, it displays sales revenue across the 12 months.

### Q8: What is an area chart?
**Answer:** An area chart is a line chart where the area beneath the line is filled with color (`fill_between`). It emphasizes the total cumulative volume of sales over the year.

### Q9: What is a bar chart?
**Answer:** A bar chart represents categorical data with rectangular bars whose lengths/heights are proportional to values. We used it to compare revenue across Product Categories and Regions.

### Q10: What is a pie chart?
**Answer:** A pie chart shows percentage proportions of a whole (100%). It visualizes the share of total revenue contributed by each product category (`autopct='%1.1f%%'`).

### Q11: How is total revenue calculated?
**Answer:** By converting the Sales Revenue column into a NumPy array and applying `np.sum(rev_array)`. For each individual row, `Sales Revenue = Quantity * Unit Price`.

### Q12: How are charts embedded into Tkinter?
**Answer:** Using `FigureCanvasTkAgg`. We create a Matplotlib figure, pass it to `FigureCanvasTkAgg(fig, master=frame)`, call `canvas.draw()`, and place it using `pack()`.

### Q13: How does filtering work?
**Answer:** When the user selects a Category, Region, or Month and clicks "Apply Filters", the dataset is filtered in Pandas (`df = df[df['Region'] == selected_region]`), NumPy recalculates the metrics, and the charts redraw with the filtered data.

### Q14: How are the Key Insights generated?
**Answer:** They are computed dynamically from the active data using Pandas `idxmax()` and NumPy statistics to find the highest-earning category, leading region, most sold product, and order averages.

### Q15: What is the difference between Mean and Median?
**Answer:** Mean is the arithmetic average, which can be pulled up or down by extreme values. Median is the middle number when sorted, making it immune to extreme price outliers.

### Q16: What does Standard Deviation (`np.std`) tell us?
**Answer:** It measures how spread out the order amounts are around the average. A higher standard deviation means transactions range from very small to very large.

### Q17: What error handling did we include?
**Answer:** If the CSV file is missing, the script automatically recreates it. If an invalid file is loaded, it shows a friendly Tkinter popup message box instead of crashing.

### Q18: What is `ttk.Notebook`?
**Answer:** A Tkinter widget that provides clean tabs, allowing us to organize charts, statistics, and data tables neatly without overcrowding the screen.

### Q19: What is `ttk.Treeview`?
**Answer:** A table widget in Tkinter used to display rows and columns of data, like an Excel sheet.

### Q20: What are the main business findings from this project?
**Answer:** Electronics is the leading revenue category, the North region generated the highest sales, and sales show strong seasonal growth towards the end of the year (Q4).
