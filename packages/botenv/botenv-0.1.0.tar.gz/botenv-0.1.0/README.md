# BotEnv

BotEnv é uma ferramenta Python projetada para simplificar o gerenciamento de variáveis de ambiente em aplicações. Ideal para projetos que exigem configurações seguras e reutilizáveis, BotEnv facilita a definição e o carregamento dessas variáveis diretamente no sistema.

## Funcionalidades

- **Carregamento de Variáveis de Ambiente:** Carregue as variaveis diretamente do sistema.
- **Definição Simplificada:** Configure variáveis com facilidade durante a execução pelo console.

## Requisitos

- Python 3.10 ou superior.

## Instalação

1. Instale o pacote:
   ```bash
   pip install botenv
   ```

## Exemplo de Uso

```python
from botenv import BotEnv

if __name__ == "__main__":
    e = Env(
        prefix_env='KEY_TEST',
        credentials_keys='USER PASSWORD'.split()
    )
    print(e.credentials)
```

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [Licença MIT](LICENSE) para mais detalhes.

## Contribuições

Contribuições são bem-vindas! Caso tenha sugestões, melhorias ou correções, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Contato

Para dúvidas ou suporte, entre em contato com o mantenedor através do [GitHub](https://github.com/botlorien/botenv).
