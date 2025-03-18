# Registro Automático de Ponto

Este projeto automatiza o registro de ponto em um sistema web, utilizando Selenium para interagir com a interface do usuário. O script permite login, navegação até a página de espelho de ponto, inserção de batidas e atualização da página.

## Requisitos

Antes de executar o projeto, certifique-se de ter os seguintes requisitos instalados:

- Python 3.11+
- Google Chrome instalado
- ChromeDriver compatível com a versão do Chrome
- Bibliotecas Python necessárias:

```bash
pip install selenium webdriver-manager holidays tomli-w
```

## Configuração

Antes de executar o script, é necessário configurar o arquivo `settings.toml` com as credenciais e informações necessárias:

```toml
login = "seu_usuario"
senha = "sua_senha"
desc = "Justificativa do ponto"
minhour = "07:50"
maxhour = "08:00"
url = "URL do sistema de ponto"
```

Se o arquivo `settings.toml` não existir, ele será criado automaticamente na primeira execução.

## Uso

Para executar o script, basta rodar:

```bash
python script.py
```

O script irá:
1. Abrir o navegador e acessar a URL fornecida.
2. Realizar login com as credenciais do `settings.toml`.
3. Acessar a página de espelho de ponto.
4. Verificar os dias trabalhados e validar os horários.
5. Inserir os horários de entrada e saída, respeitando as regras de compensação.
6. Atualizar a página para salvar as informações.

## Estrutura do Código

O projeto está estruturado da seguinte forma:

- `do_login(driver, user, passwd)`: Realiza o login no sistema.
- `goto_hours_grid(driver)`: Navega até a página de espelho de ponto.
- `open_insert(driver, handler)`: Abre o modal para inserção de batidas.
- `insert_hours(driver, team, data_validation, compensacao, config_hours)`: Insere as batidas de ponto.
- `do_update(driver)`: Atualiza a página.
- `generate_time_range(start_time, end_time)`: Gera um intervalo de horários possíveis para a entrada.
- `generate_data_for_validation(driver, data_structure)`: Obtém os dados necessários para validação do ponto.
- `main()`: Controla o fluxo principal do script.

## Logs

Todas as operações do script são registradas no arquivo `ponto_log.log`, incluindo sucessos e erros encontrados durante a execução.

## Contribuição

Se desejar contribuir com melhorias para o projeto, siga os seguintes passos:
1. Faça um fork do repositório.
2. Crie um branch para sua funcionalidade (`git checkout -b minha-feature`).
3. Faça suas alterações e commit (`git commit -m "Minha melhoria"`).
4. Envie para seu fork (`git push origin minha-feature`).
5. Abra um Pull Request para este repositório.

## Licença

Este projeto está sob a licença MIT.

