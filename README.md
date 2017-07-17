# pre-commit-shfmt hook

Single [pre-commit](http://pre-commit.com/) hook which runs **[terraform_unused_vars](https://github.com/ContainerLabs/terraform-unused-vars)** on the terraform project.


An example `.pre-commit-config.yaml`:

```yaml
-   repo: git://github.com/pecigonzalo/pre-commit-terraform-vars
    sha: master
    hooks:
      -   id: terraform-vars
```

Enjoy the clean code!
