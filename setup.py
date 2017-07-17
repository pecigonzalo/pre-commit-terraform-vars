from distutils.core import setup

setup(
    author_email='pecigonzalo@users.noreply.github.com',
    author='Gonzalo Peci',
    description='Find unused variables in Terraform.',
    include_package_data=True,
    long_description='Find unused variables in Terraform.',
    name='terraform-unused-vars',
    package_dir={},
    packages=['terraform_unused_vars'],
    entry_points={
        'console_scripts': [
            'terraform-unused-vars = terraform_unused_vars.__main__:main'
        ]
    },
    url='https://github.com/pecigonzalo/pre-commit-terraform-vars',
    version='0.1',
)
