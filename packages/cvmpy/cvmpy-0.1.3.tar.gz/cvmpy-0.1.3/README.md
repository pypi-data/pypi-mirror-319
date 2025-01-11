# cvmpy

## Overview
The **cvmpy** is a tool designed to read and process datasets from the **Comissão de Valores Mobiliários (CVM)**. It simplifies access to financial information, making it easier for users to conduct research and financial analysis. The project supports the following data categories:

- **Companhias**: ITR (Quarterly Information), DFP (Financial Statements), and more.
- **Fundos de Investimento (FI)**: Informe Diário, Composição e Diversificação de Aplicações.
- **Fundos de Investimento (FII)**: Demonstrações Financeiras, Informe Mensal, and more.

---

## Installation

To install the package via `pip`, run the following command:

```bash
pip install cvmpy
```


## Usage

### **Example: Fetching FI Static and Historical Data**

To fetch data, you can use the following methods:

- For panel datasets:

`fetch_historical_data(dataset_name, start_date, end_date)`

- For static datasets:

`fetch_static_data(dataset_name)`

#### **Available Datasets**

- `cadastro` (registration)
- `extrato` (statement)
- `registro_fundo_classe` (fund class registration)
- `informe_diario` (daily report)
- `composicao_diversificacao` (composition and diversification)
- `balancete` (trial balance)
- `perfil_mensal` (monthly profile)

```python
import cvmpy

# Create an instance of FI datasets
fi = cvmpy.FI()

# Fetch static data (e.g., cadastro)
fi.fetch_static_data("cadastro")

# Fetch historical data (e.g., informe_diario)
fi.fetch_historical_data("informe_diario", "2024-11-05", "2024-12-23")
```

The fetched datasets become attributes of the `FI` instance. For example:

```python
# Display the first few rows of Informe Diário data
print(fi.informe_diario.inf_diario_fi.head())
```

#### **Handling Large Data with Parsers**

For long historical data, memory issues may arise. In such cases, you can apply a parser function to filter data as it is being read. Here’s an example of filtering by specific CNPJs:

```python
list_cnpjs = [
    "37.916.879/0001-26",  # DYNAMO COUGAR MASTER FIA
    "11.188.572/0001-62",  # ATMOS MASTER FIA
    "06.964.937/0001-63",  # OPPORTUNITY SELECTION MASTER FIA
]

# Fetch data with a parser function to filter by CNPJ
fi.fetch_historical_data(
    "composicao_diversificacao",
    "2024-01-31",
    "2024-03-31",
    parser=lambda df: (
        df[df["CNPJ_FUNDO_CLASSE"].isin(list_cnpjs)]
        if "CNPJ_FUNDO_CLASSE" in df.columns
        else df
    ),
)
```
In this example, only the specified CNPJs are retained in the dataset.

---

## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Commit changes: `git commit -m "Add your feature"`.
4. Push to your branch: `git push origin feature/your-feature-name`.
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact
If you encounter issues or have feedback, feel free to open an issue or reach out via the repository’s discussions tab.