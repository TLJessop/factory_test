# User Data Generator

A lightweight Python desktop tool that lets developers **instantly create realistic dummy user data** for debugging, testing, demos, and seed databases.  
Through an intuitive point-and-click GUI you can:

* define any number of custom fields (e.g. `first_name`, `email`, `uuid`)
* choose a faker-powered data type for each field
* set how many records to create
* export the result as JSON or CSV with a single click

No scripting required—yet 100 % extensible for power users.

---

## 1  Features & What It Does
| | |
|---|---|
| 🧩 **Custom schema** | Add, edit or delete fields, choose their data type |
| 📈 **Scalable output** | Generate 1 record or 100 000—your call |
| 🔄 **Multiple formats** | Save to **JSON** or **CSV** (extensible) |
| 🎛 **Interactive GUI** | Built with Tkinter, runs on any machine with Python |
| 🛠 **Powered by Faker** | Over 20 realistic data generators out of the box |
| 🔌 **Pluggable** | Add new formats, field types, or CLI in minutes |

---

## 2  Installation

```bash
# 1. Clone the repo
git clone https://github.com/your-org/user-data-generator.git
cd user-data-generator

# 2. Create an optional virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python main.py
```

> Tkinter ships with the standard Python installer on Windows/macOS.  
> On most Linux distros install `python3-tk` via your package manager if missing.

---

## 3  Quick Start / How to Use

1. **Launch** `python main.py`  
2. **Add fields**  
   * Type a name (`first_name`)  
   * Choose a type (`First Name`)  
   * Click **Add Field**  
3. **Set “Number of Records”** (e.g. 500)  
4. **Choose “Export Format”** (JSON or CSV)  
5. **Browse** for an output file path  
6. Click **Generate Data** — Done!  

A progress bar tracks long batches and a success dialog shows where your file is saved.

---

## 4  Example Use-Cases

| Scenario | Why It Helps |
|----------|--------------|
| Front-end prototyping | Feed repeatable dummy user lists to React/Angular/Vue apps |
| API load testing | Seed Postman / JMeter scripts with thousands of fake users |
| Database demos | Populate staging DBs with privacy-safe sample records |
| CI pipelines | Auto-generate fixtures during test runs |
| Classroom / workshops | Teach SQL or data science without exposing real PII |

---

## 5  Supported Field Types  (Out-of-the-box)

* Full Name
* First Name
* Last Name
* Email
* Phone Number
* Address
* City
* Country
* Postal Code
* Date of Birth
* Username
* Password
* Text (paragraph)
* Number (integer 1-1000)
* Boolean
* UUID
* Job Title
* Company
* Credit Card (number/expiry/provider bundle)
* URL

Add your own by editing `data_generator.py`—one line per new type.

---

## 6  Supported Export Formats

| Format | File Extension | Notes |
|--------|----------------|-------|
| JSON   | `.json`        | Pretty-printed, UTF-8 |
| CSV    | `.csv`         | Header row included |

(Architecture allows adding XML, SQL INSERT, Parquet, etc.—see Contributing.)

---

## 7  Requirements & Dependencies

* Python ≥ 3.8
* [Faker](https://faker.readthedocs.io/) ≥ 18.0  – core data provider  
* [ttkthemes](https://github.com/RedFantom/ttkthemes) ≥ 3.2.2  – optional; nicer theme
* Tkinter – ships with CPython; may require `python3-tk` package on Linux

All managed by `pip install -r requirements.txt`.

---

## 8  Troubleshooting

| Problem | Fix |
|---------|-----|
| **`ModuleNotFoundError: No module named 'faker'`** | `pip install faker` (or activate your venv) |
| GUI will not start on Linux | `sudo apt install python3-tk` (Debian/Ubuntu) |
| Output file contains strange characters | Open as UTF-8 or ensure your editor’s encoding matches |
| Progress bar freezes on huge datasets | Generation runs in a thread; UI may appear sluggish on 100k+ rows—just wait or break into smaller batches |

---

## 9  Contributing & Extending

We love PRs! Here’s how to add more power:

### Add a New Field Type
1. Open `data_generator.py`
2. In `generate_field_value`, append your mapping, e.g.  
   ` "IPv4": lambda: fake.ipv4(),`
3. Add the label to `field_types` list in `gui.py`
4. Run `python main.py` and test

### Add an Export Format
1. Implement `_export_<format>()` in `gui.py`  
2. Extend the dropdown list & file extension mapping  
3. Submit a pull-request

### General Guidelines
* Use descriptive commit messages
* Follow PEP-8
* Include docstrings & type hints
* Add/adjust unit tests where relevant

Please open issues for bugs or feature requests.  
Happy generating! 🎉
