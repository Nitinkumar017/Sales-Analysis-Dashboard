import os
import tempfile

# 1. Set matplotlib temporary cache directory before importing matplotlib
os.environ["MPLCONFIGDIR"] = os.path.join(tempfile.gettempdir(), "matplotlib_sales_cache")

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SalesDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Analysis Dashboard")
        self.root.geometry("1150x760")
        self.root.configure(bg="#f4f6f9")

        # Variables for dataset
        self.csv_file = "sales_data.csv"
        self.df = None
        self.filtered_df = None

        # Data cleaning counters
        self.duplicates_removed = 0
        self.missing_handled = 0

        # Load and clean initial data
        self.load_data(self.csv_file)

        # Build GUI Components
        self.create_header()
        self.create_controls()
        self.create_kpi_cards()
        self.create_tabs()
        self.create_insights_section()
        self.create_status_bar()

        # Initial dashboard display
        self.update_dashboard()

    # -------------------------------------------------------------
    # DATA LOADING AND CLEANING (Pandas)
    # -------------------------------------------------------------
    def load_data(self, file_path):
        """Loads and cleans the sales dataset using Pandas."""
        try:
            # Check if file exists, if not generate it
            if not os.path.exists(file_path):
                import generate_dataset
                generate_dataset.generate_sales_data(file_path)

            raw_df = pd.read_csv(file_path)
            initial_count = len(raw_df)

            # 1. Remove duplicate records
            cleaned = raw_df.drop_duplicates().copy()
            self.duplicates_removed = initial_count - len(cleaned)

            # 2. Count and handle missing values
            self.missing_handled = int(cleaned.isnull().sum().sum())
            cleaned = cleaned.dropna(subset=["Sales Revenue", "Quantity"]).copy()
            cleaned["Region"] = cleaned["Region"].fillna("North")

            # 3. Trim whitespace in text columns
            text_columns = ["Product", "Product Category", "Region", "Customer Segment"]
            for col in text_columns:
                if col in cleaned.columns:
                    cleaned[col] = cleaned[col].astype(str).str.strip()

            # 4. Convert Date to datetime format
            cleaned["Date"] = pd.to_datetime(cleaned["Date"], errors="coerce")
            cleaned = cleaned.dropna(subset=["Date"]).copy()

            # 5. Ensure numeric data types
            cleaned["Quantity"] = pd.to_numeric(cleaned["Quantity"], errors="coerce").astype(int)
            cleaned["Unit Price"] = pd.to_numeric(cleaned["Unit Price"], errors="coerce").astype(float)
            cleaned["Sales Revenue"] = pd.to_numeric(cleaned["Sales Revenue"], errors="coerce").astype(float)

            # Add Month column for aggregation
            cleaned["Month"] = cleaned["Date"].dt.strftime("%b")
            cleaned["Month_Num"] = cleaned["Date"].dt.month

            # Sort chronologically
            cleaned = cleaned.sort_values(by="Date").reset_index(drop=True)

            self.df = cleaned
            self.filtered_df = cleaned.copy()
            self.csv_file = file_path

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dataset: {str(e)}")

    # -------------------------------------------------------------
    # GUI SECTIONS (Tkinter)
    # -------------------------------------------------------------
    def create_header(self):
        """Creates simple top title header."""
        header_frame = tk.Frame(self.root, bg="#1e3a8a", height=60)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="Sales Analysis Dashboard",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#1e3a8a"
        )
        title_label.pack(side=tk.LEFT, padx=15, pady=(8, 0))

        subtitle_label = tk.Label(
            header_frame,
            text="Sales Performance & Business Insights",
            font=("Arial", 10),
            fg="#93c5fd",
            bg="#1e3a8a"
        )
        subtitle_label.pack(side=tk.LEFT, padx=15, pady=(28, 0))

    def create_controls(self):
        """Creates filter dropdowns and control buttons."""
        control_frame = tk.LabelFrame(
            self.root,
            text="Filters & Actions",
            font=("Arial", 10, "bold"),
            bg="white",
            padx=10,
            pady=6
        )
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=8)

        # Category Filter
        tk.Label(control_frame, text="Category:", font=("Arial", 9), bg="white").pack(side=tk.LEFT, padx=(5, 2))
        categories = ["All Categories"] + sorted(self.df["Product Category"].unique().tolist())
        self.cat_var = tk.StringVar(value="All Categories")
        self.cat_combo = ttk.Combobox(control_frame, textvariable=self.cat_var, values=categories, state="readonly", width=16)
        self.cat_combo.pack(side=tk.LEFT, padx=5)

        # Region Filter
        tk.Label(control_frame, text="Region:", font=("Arial", 9), bg="white").pack(side=tk.LEFT, padx=(10, 2))
        regions = ["All Regions"] + sorted(self.df["Region"].unique().tolist())
        self.reg_var = tk.StringVar(value="All Regions")
        self.reg_combo = ttk.Combobox(control_frame, textvariable=self.reg_var, values=regions, state="readonly", width=14)
        self.reg_combo.pack(side=tk.LEFT, padx=5)

        # Month Filter
        tk.Label(control_frame, text="Month:", font=("Arial", 9), bg="white").pack(side=tk.LEFT, padx=(10, 2))
        months = ["All Months"] + ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        self.month_var = tk.StringVar(value="All Months")
        self.month_combo = ttk.Combobox(control_frame, textvariable=self.month_var, values=months, state="readonly", width=12)
        self.month_combo.pack(side=tk.LEFT, padx=5)

        # Buttons
        btn_apply = tk.Button(
            control_frame,
            text="Apply Filters",
            font=("Arial", 9, "bold"),
            bg="#2563eb",
            fg="white",
            padx=8,
            pady=2,
            command=self.apply_filters
        )
        btn_apply.pack(side=tk.LEFT, padx=10)

        btn_reset = tk.Button(
            control_frame,
            text="Reset",
            font=("Arial", 9),
            bg="#e5e7eb",
            padx=8,
            pady=2,
            command=self.reset_filters
        )
        btn_reset.pack(side=tk.LEFT, padx=5)

        btn_load = tk.Button(
            control_frame,
            text="Load CSV File",
            font=("Arial", 9),
            bg="#f3f4f6",
            padx=8,
            pady=2,
            command=self.choose_file
        )
        btn_load.pack(side=tk.RIGHT, padx=5)

    def create_kpi_cards(self):
        """Creates clean summary cards showing NumPy calculated totals."""
        kpi_frame = tk.Frame(self.root, bg="#f4f6f9")
        kpi_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=2)

        self.cards = {}
        card_items = [
            ("revenue", "Total Revenue", "$0.00", "#1e40af"),
            ("quantity", "Total Units Sold", "0", "#047857"),
            ("products", "Number of Products", "0", "#b45309"),
            ("transactions", "Total Orders", "0", "#6d28d9"),
            ("avg_sale", "Average Order Value", "$0.00", "#be123c")
        ]

        for key, label_text, default_val, text_color in card_items:
            card = tk.Frame(kpi_frame, bg="white", relief="solid", bd=1, padx=10, pady=6)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

            lbl_title = tk.Label(card, text=label_text, font=("Arial", 8, "bold"), fg="#6b7280", bg="white")
            lbl_title.pack(anchor="w")

            lbl_value = tk.Label(card, text=default_val, font=("Arial", 13, "bold"), fg=text_color, bg="white")
            lbl_value.pack(anchor="w", pady=(2, 0))

            self.cards[key] = lbl_value

    def create_tabs(self):
        """Creates notebook tabs for charts and dataset table."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=6)

        # Tab 1: Main Charts (Line, Bar, Bar, Pie)
        self.tab_charts = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_charts, text="Visualizations")

        # Tab 2: Area Chart & Detailed Statistics
        self.tab_area = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_area, text="Area Chart & Statistics")

        # Tab 3: Dataset Records Table
        self.tab_data = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_data, text="Data Records")

        # Setup Tab 3 (Treeview table)
        self.setup_data_table()

    def create_insights_section(self):
        """Creates key insights section at the bottom."""
        insights_frame = tk.LabelFrame(
            self.root,
            text="Key Insights",
            font=("Arial", 9, "bold"),
            bg="white",
            padx=10,
            pady=4
        )
        insights_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 4))

        self.insight_labels = []
        for i in range(4):
            lbl = tk.Label(
                insights_frame,
                text="• Loading insight...",
                font=("Arial", 9),
                bg="white",
                fg="#1f2937",
                anchor="w"
            )
            lbl.pack(anchor="w", pady=1)
            self.insight_labels.append(lbl)

    def create_status_bar(self):
        """Creates simple bottom status bar."""
        self.status_bar = tk.Label(
            self.root,
            text="Ready | Dataset loaded successfully.",
            font=("Arial", 8),
            bg="#e5e7eb",
            fg="#4b5563",
            anchor="w",
            padx=10,
            pady=2
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_data_table(self):
        """Initializes simple Treeview table in Tab 3."""
        cols = ("Date", "Product", "Category", "Region", "Quantity", "Unit Price", "Sales Revenue", "Segment")
        self.tree = ttk.Treeview(self.tab_data, columns=cols, show="headings", height=14)

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.column("Product", width=180, anchor="w")

        scroll_y = ttk.Scrollbar(self.tab_data, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # -------------------------------------------------------------
    # CALCULATIONS USING NUMPY & PANDAS
    # -------------------------------------------------------------
    def calculate_kpis(self):
        """
        Uses NumPy arrays to calculate summary statistics:
        np.sum, np.mean, np.median, np.min, np.max, np.unique.
        """
        if self.filtered_df.empty:
            return 0.0, 0, 0, 0, 0.0

        # Convert Pandas columns to NumPy arrays
        rev_array = self.filtered_df["Sales Revenue"].to_numpy()
        qty_array = self.filtered_df["Quantity"].to_numpy()
        prod_array = self.filtered_df["Product"].to_numpy()

        # NumPy calculations:
        total_revenue = float(np.sum(rev_array))
        total_quantity = int(np.sum(qty_array))
        num_products = len(np.unique(prod_array))
        num_orders = len(rev_array)
        avg_order_value = float(np.mean(rev_array))

        return total_revenue, total_quantity, num_products, num_orders, avg_order_value

    def generate_insights(self):
        """Generates dynamic business statements from active data."""
        if self.filtered_df.empty:
            return ["No records found matching the selected filters."]

        statements = []

        # 1. Best performing category
        cat_sales = self.filtered_df.groupby("Product Category")["Sales Revenue"].sum()
        top_cat = cat_sales.idxmax()
        top_cat_val = cat_sales.max()
        statements.append(f"• Category '{top_cat}' generated the highest revenue (${top_cat_val:,.2f}).")

        # 2. Top region
        reg_sales = self.filtered_df.groupby("Region")["Sales Revenue"].sum()
        top_reg = reg_sales.idxmax()
        top_reg_val = reg_sales.max()
        statements.append(f"• Region '{top_reg}' recorded the highest sales performance (${top_reg_val:,.2f}).")

        # 3. Most sold product
        prod_qty = self.filtered_df.groupby("Product")["Quantity"].sum()
        top_prod = prod_qty.idxmax()
        top_qty = prod_qty.max()
        statements.append(f"• Most frequently sold product: '{top_prod}' with {top_qty:,} units sold.")

        # 4. NumPy order statistics
        rev_arr = self.filtered_df["Sales Revenue"].to_numpy()
        mean_val = np.mean(rev_arr)
        max_val = np.max(rev_arr)
        statements.append(f"• Average order value is ${mean_val:,.2f}, with maximum single sale of ${max_val:,.2f}.")

        return statements

    # -------------------------------------------------------------
    # MATPLOTLIB CHART GENERATION
    # -------------------------------------------------------------
    def draw_charts(self):
        """Draws the 4 main charts in Tab 1 (Line, Bar, Bar, Pie)."""
        # Clear previous canvas if any
        for widget in self.tab_charts.winfo_children():
            widget.destroy()

        fig, axes = plt.subplots(2, 2, figsize=(10, 5), dpi=90)
        fig.subplots_adjust(hspace=0.45, wspace=0.3, left=0.08, right=0.95, top=0.92, bottom=0.1)

        # 1. Line Chart: Sales Trend Over Months
        ax1 = axes[0, 0]
        monthly = self.filtered_df.groupby(["Month_Num", "Month"])["Sales Revenue"].sum().reset_index()
        monthly = monthly.sort_values("Month_Num")
        if not monthly.empty:
            ax1.plot(monthly["Month"], monthly["Sales Revenue"], marker="o", color="#2563eb", linewidth=2)
            ax1.set_title("Sales Trend (Line Chart)", fontsize=9, fontweight="bold")
            ax1.set_ylabel("Revenue ($)", fontsize=8)
            ax1.grid(True, linestyle="--", alpha=0.5)
            ax1.tick_params(labelsize=8)
        else:
            ax1.text(0.5, 0.5, "No Data", ha="center", va="center")

        # 2. Bar Chart: Category Analysis
        ax2 = axes[0, 1]
        cat_group = self.filtered_df.groupby("Product Category")["Sales Revenue"].sum().sort_values(ascending=False)
        if not cat_group.empty:
            ax2.bar(cat_group.index, cat_group.values, color="#3b82f6", width=0.5)
            ax2.set_title("Category Analysis (Bar Chart)", fontsize=9, fontweight="bold")
            ax2.set_ylabel("Revenue ($)", fontsize=8)
            ax2.grid(True, axis="y", linestyle="--", alpha=0.5)
            ax2.tick_params(axis="x", rotation=20, labelsize=8)
            ax2.tick_params(axis="y", labelsize=8)
        else:
            ax2.text(0.5, 0.5, "No Data", ha="center", va="center")

        # 3. Bar Chart: Regional Analysis
        ax3 = axes[1, 0]
        reg_group = self.filtered_df.groupby("Region")["Sales Revenue"].sum().sort_values(ascending=False)
        if not reg_group.empty:
            colors = ["#10b981", "#6366f1", "#f59e0b", "#ec4899"]
            ax3.bar(reg_group.index, reg_group.values, color=colors[:len(reg_group)], width=0.5)
            ax3.set_title("Regional Analysis (Bar Chart)", fontsize=9, fontweight="bold")
            ax3.set_ylabel("Revenue ($)", fontsize=8)
            ax3.grid(True, axis="y", linestyle="--", alpha=0.5)
            ax3.tick_params(labelsize=8)
        else:
            ax3.text(0.5, 0.5, "No Data", ha="center", va="center")

        # 4. Pie Chart: Sales Distribution by Category
        ax4 = axes[1, 1]
        if not cat_group.empty and cat_group.sum() > 0:
            pie_colors = ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899"]
            wedges, texts, autotexts = ax4.pie(
                cat_group.values,
                labels=cat_group.index,
                autopct="%1.1f%%",
                startangle=140,
                colors=pie_colors[:len(cat_group)]
            )
            ax4.set_title("Sales Distribution (Pie Chart)", fontsize=9, fontweight="bold")
            for t in texts:
                t.set_fontsize(8)
            for at in autotexts:
                at.set_fontsize(8)
        else:
            ax4.text(0.5, 0.5, "No Data", ha="center", va="center")

        canvas = FigureCanvasTkAgg(fig, master=self.tab_charts)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)

    def draw_area_chart(self):
        """Draws the Area Chart and NumPy statistics in Tab 2."""
        for widget in self.tab_area.winfo_children():
            widget.destroy()

        chart_frame = tk.Frame(self.tab_area, bg="white")
        chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        stats_frame = tk.LabelFrame(
            self.tab_area,
            text="NumPy Statistical Calculations",
            font=("Arial", 9, "bold"),
            bg="white",
            padx=12,
            pady=10,
            width=260
        )
        stats_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        stats_frame.pack_propagate(False)

        # Plot Area Chart
        fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=90)
        fig.subplots_adjust(left=0.12, right=0.94, top=0.90, bottom=0.12)

        monthly = self.filtered_df.groupby(["Month_Num", "Month"])["Sales Revenue"].sum().reset_index()
        monthly = monthly.sort_values("Month_Num")

        if not monthly.empty:
            months = monthly["Month"].tolist()
            rev_vals = monthly["Sales Revenue"].to_numpy()
            
            # Use NumPy cumulative sum for area chart
            cum_sales = np.cumsum(rev_vals)
            x = np.arange(len(months))

            ax.plot(x, cum_sales, color="#059669", linewidth=2, marker="o", label="Cumulative Sales")
            ax.fill_between(x, cum_sales, color="#10b981", alpha=0.3)
            ax.set_xticks(x)
            ax.set_xticklabels(months, fontsize=8)
            ax.set_title("Overall Sales Trend (Area Chart - np.cumsum)", fontsize=10, fontweight="bold")
            ax.set_ylabel("Cumulative Revenue ($)", fontsize=8)
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.legend(fontsize=8)
        else:
            ax.text(0.5, 0.5, "No Data", ha="center", va="center")

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)

        # Display NumPy Statistics in right panel
        if not self.filtered_df.empty:
            rev_arr = self.filtered_df["Sales Revenue"].to_numpy()
            stats_list = [
                ("Total (np.sum)", f"${np.sum(rev_arr):,.2f}"),
                ("Mean (np.mean)", f"${np.mean(rev_arr):,.2f}"),
                ("Median (np.median)", f"${np.median(rev_arr):,.2f}"),
                ("Std Dev (np.std)", f"${np.std(rev_arr):,.2f}"),
                ("Min Sale (np.min)", f"${np.min(rev_arr):,.2f}"),
                ("Max Sale (np.max)", f"${np.max(rev_arr):,.2f}")
            ]

            for label_title, stat_val in stats_list:
                item_box = tk.Frame(stats_frame, bg="#f9fafb", relief="solid", bd=1, padx=6, pady=4)
                item_box.pack(fill=tk.X, pady=4)

                tk.Label(item_box, text=label_title, font=("Arial", 8), fg="#4b5563", bg="#f9fafb").pack(anchor="w")
                tk.Label(item_box, text=stat_val, font=("Arial", 10, "bold"), fg="#111827", bg="#f9fafb").pack(anchor="w")

    def update_data_table(self):
        """Populates Treeview with records from active dataset."""
        self.tree.delete(*self.tree.get_children())
        # Display first 250 rows for smooth performance
        for _, row in self.filtered_df.head(250).iterrows():
            date_str = row["Date"].strftime("%Y-%m-%d") if pd.notnull(row["Date"]) else ""
            self.tree.insert("", tk.END, values=(
                date_str,
                row["Product"],
                row["Product Category"],
                row["Region"],
                row["Quantity"],
                f"${row['Unit Price']:.2f}",
                f"${row['Sales Revenue']:.2f}",
                row["Customer Segment"]
            ))

    # -------------------------------------------------------------
    # DASHBOARD REFRESH & USER ACTIONS
    # -------------------------------------------------------------
    def update_dashboard(self):
        """Updates all cards, charts, insights, and table."""
        # 1. Update KPI cards using NumPy
        total_rev, total_qty, num_prods, num_orders, avg_sale = self.calculate_kpis()
        self.cards["revenue"].config(text=f"${total_rev:,.2f}")
        self.cards["quantity"].config(text=f"{total_qty:,}")
        self.cards["products"].config(text=f"{num_prods}")
        self.cards["transactions"].config(text=f"{num_orders:,}")
        self.cards["avg_sale"].config(text=f"${avg_sale:,.2f}")

        # 2. Draw charts
        self.draw_charts()
        self.draw_area_chart()

        # 3. Update key insights
        insights = self.generate_insights()
        for idx, text in enumerate(insights):
            if idx < len(self.insight_labels):
                self.insight_labels[idx].config(text=text)

        # 4. Update table
        self.update_data_table()

        # 5. Status bar
        self.status_bar.config(
            text=f"Dataset: {os.path.basename(self.csv_file)} | Cleaned: {self.duplicates_removed} duplicates removed, {self.missing_handled} nulls handled | Showing {len(self.filtered_df)} records"
        )

    def apply_filters(self):
        """Filters dataset based on selected dropdown values."""
        df = self.df.copy()

        cat = self.cat_var.get()
        reg = self.reg_var.get()
        mon = self.month_var.get()

        if cat != "All Categories":
            df = df[df["Product Category"] == cat]
        if reg != "All Regions":
            df = df[df["Region"] == reg]
        if mon != "All Months":
            df = df[df["Month"] == mon]

        self.filtered_df = df
        self.update_dashboard()

    def reset_filters(self):
        """Resets dropdowns and restores complete dataset."""
        self.cat_var.set("All Categories")
        self.reg_var.set("All Regions")
        self.month_var.set("All Months")
        self.filtered_df = self.df.copy()
        self.update_dashboard()

    def choose_file(self):
        """Allows user to select custom CSV dataset."""
        path = filedialog.askopenfilename(
            title="Select Sales CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if path:
            self.load_data(path)
            self.reset_filters()
            messagebox.showinfo(
                "Success",
                f"Dataset loaded successfully!\n\n"
                f"• Clean records: {len(self.df)}\n"
                f"• Duplicates removed: {self.duplicates_removed}\n"
                f"• Missing values handled: {self.missing_handled}"
            )


# -------------------------------------------------------------
# APPLICATION LAUNCHER
# -------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SalesDashboardApp(root)
    root.mainloop()
