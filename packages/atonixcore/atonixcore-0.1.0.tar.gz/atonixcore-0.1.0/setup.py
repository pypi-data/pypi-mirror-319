from setuptools import setup, find_packages

setup(
    name='atonixcore',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Django and Django REST Framework
        'django>=3.2,<4.0',
        'djangorestframework',
        'djangorestframework-simplejwt',
        'django-cors-headers',
        'django-allauth',
        'django-rest-auth',
        'django-environ',
        'django-debug-toolbar',
        'django-extensions',
        'psycopg2-binary',
        'gunicorn',
        'djangorestframework-jsonapi',
        'daphne',
        'channels',
        'django-redis',
        'celery',
        'redis',

        # Data Science and Computational Libraries
        'numpy',
        'pandas',
        'matplotlib',
        'scipy',
        'jupyter',
        'scikit-learn',
        'torch',

        # Security
        'cryptography',
        'pycryptodome',
        'paramiko',

        # Machine Learning and Quantum Computing
        'opencv-python',
        'channels-redis',
        'qiskit',
        'qiskit-nature',
        'qiskit-ibm-runtime',
        'qiskit-runtime',
        'qiskit-ibm-catalog',
        'qiskit-aer',
        'qutip',
        'pyscf',

        # Web Development
        'flask',
        'flask-jwt-extended',
        'flask-cors',
        'flask-restful',
        'openapi-spec-validator',
        'openapi-core',

        # Robotics and Hardware Integration
        'platformio',
        'rosdep',
        'rospkg',
        'roslibpy',

        # Data Analysis and Visualization
        'seaborn',
        'statsmodels',

        # Machine Learning
        'xgboost',
    ],
    author='Samuel Guxegdsa',
    author_email='ofidohub@gmail.com',
    description="At AtonixCorp, we're pioneering the future with cutting-edge technology solutions across agriculture, fintech, medical research, security, big data, and cloud computing. Our innovative approaches and dedicated expertise drive advancements and empower industries to reach new heights.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AtonixCorp/atonixcore',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
