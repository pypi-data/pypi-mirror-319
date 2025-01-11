ecommerce/
    __init__.py
    products/
        __init__.py
        product_manager.py
        inventory.py
    users/
        __init__.py
        user_manager.py
        authentication.py
    orders/
        __init__.py
        order_manager.py
        payment.py



# Creating a distribution file

* cd path/to/ecommerce
* python setup.py sdist

'''
This will create a dist/ folder containing a .tar.gz file:
    dist/
    ecommerce-1.0.0.tar.gz
'''

# Installing the Package Locally
* pip install dist/ecommerce-1.0.0.tar.gz

'''
from ecommerce.products.product_manager import add_product
from ecommerce.users.user_manager import add_user

# Add a product
add_product("Laptop", 1000, 10)

# Add a user
add_user("John Doe", "john@example.com")
'''

# Installing through github repo
    * create a github repo and push your project into it
    * pip install git+https://github.com/aicouncil/ecommerce.git

# PyPi => The python Package index
    * The primary repository for third-party python packages. It offers a vast collection of open-source tools and libraries.
* Discovery - Browse and serach PyPi to find packages that meet our needs, from web frameworks to scientific computing libraries.
* Centralised - PyPI is the go-to source for the majority of packages used in the Python ecosystem.
* pip - standard tool for installing, removing and managing python packages.
* key functions
 * Install
 * Uninstall
 * List - Show listed packages
 * Dependency Management - Automatically resolves and install package dependencies

 # Upload to Pypi
    * pip install twine
    * cd path/to/your/project
    * twine upload dist/*

# Install Your Package from PyPI
    * pip install ecommerce


