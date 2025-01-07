
# Indofaker

**Indofaker** is a Python library designed to generate fake data with an Indonesian touch, such as names, addresses, phone numbers, and more. This library is useful for testing or development purposes when you need random data in an Indonesian format.

## Installation

To install this library, use pip:

```bash
pip install indofaker

````
## Usage

### 1. Generate Fake Names

### **Generate a name with specific details:**

You can generate a name based on the specified gender, tribe, and religion.

```python
from indofaker import generate_name, Gender, Tribe, Religion

name = generate_name(gender=Gender.MALE, tribe=Tribe.JAVA, religion=Religion.ISLAM)
print(name)
```

**Output:**
```
Surya Siswanto
```

### **Generate a random name:**

If you want a random name without specific details, you can use the following function:

```python
from indofaker import generate_random_name, Gender, Tribe, Religion

name = generate_random_name()
print(name)
```

**Output:**
```
Budi Raharjo
```

### 2. Generate Fake Address

You can also generate a fake address in a typical Indonesian format.

```python
from indofaker import generate_address

address = generate_address()
print(address)
```

**Output:**
```
Jl. Sudirman No.4, RT 09 / RW 05, Desa Singkole, Kecamatan Sangatta Utara, Kabupaten Kutai Timur, Provinsi Kalimantan Timur, 95243
```

## Additional Features

- **Gender:** You can specify gender (Male or Female).
- **Tribe:** Choose the Indonesian tribe you prefer (e.g., Java, Sunda, Batak, etc.).
- **Religion:** Options are available for different religions (Islam, Christianity, Hinduism, etc.).

## Contributing

If you want to contribute to this project, feel free to open a pull request or report any issues or suggestions.

## License

This project is licensed under the [MIT License](LICENSE).
```
