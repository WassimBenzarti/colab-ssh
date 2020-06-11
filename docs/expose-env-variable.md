## Exposing an environment variable
Sometimes, you might need to expose an environement variable which is only available inside the Colab notebook runtime. 
This is useful if you are executing any Colab environment dependent application through terminal (instead of Google Colab).

### `expose_env_variable` function
The following function accepts: 
  - Environment variable name
  - File to add the export command in (for example: ~/.bashrc) [Optional: defaults to `/etc/environment`]
  
```python
from colab_ssh.utils.expose_env_variable import expose_env_variable
# Expose the COLAB_TPU_ADDR environment variable
expose_env_variable("COLAB_TPU_ADDR", "/etc/environment")
```
This function will add `export COLAB_TPU_ADDR=<the-env-variable-value>` line to the file `/etc/environment`
