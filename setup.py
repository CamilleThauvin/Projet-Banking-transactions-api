"""Setup configuration for Banking Transactions API."""

from setuptools import find_packages, setup

setup(
    name="banking-transactions-api",
    version="1.0.0",
    description="API FastAPI pour exposer des transactions bancaires fictives",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "pandas>=2.1.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.21.0",
            "mypy>=1.7.0",
            "flake8>=6.1.0",
        ],
    },
)

