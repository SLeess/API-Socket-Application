### Arquitetura e Ambiente de Desenvolvimento

O sistema foi desenvolvido em **Python** utilizando a arquitetura TCP/IP com Sockets e Threading para comunicação assíncrona. A estrutura do projeto foi planejada visando segurança, modularidade e facilidade de manutenção.

**Gerenciamento de Dependências e Expansibilidade:**
O projeto adota uma estratégia de isolamento de ambientes. Foram configuradas **Virtual Environments (`venvs`)** distintas para o Cliente e para o Servidor.
* **Isolamento:** Garante que as dependências de um lado não gerem conflitos de versão no outro.
* **Expansão Paralela:** Essa separação permite que o módulo do Cliente e o módulo do Servidor escalem independentemente. Futuras atualizações (como a migração da interface do cliente para um framework web ou mobile) podem ser realizadas sem impactar a estabilidade ou as bibliotecas do servidor.
* **Portabilidade:** As dependências exatas foram congeladas em arquivos `requirements.txt`, facilitando a replicação do ambiente em outras máquinas (`pip install -r requirements.txt`).

**Configuração e Segurança (.env):**
Para aderir às boas práticas de segurança (Twelve-Factor App), nenhuma configuração sensível foi hardcoded no código-fonte.
* Utilizou-se a biblioteca `python-dotenv` para carregar variáveis de ambiente a partir de arquivos **`.env`**.
* Dados críticos, como o endereço de **HOST**, a **PORTA** de comunicação e, principalmente, a **CHAVE PRIVADA (APP_KEY)** de criptografia Fernet, são lidos dinamicamente em tempo de execução. Isso protege as credenciais caso o código seja versionado em repositórios públicos.


### Instalação e Execução

Dado o isolamento dos ambientes, a configuração deve ser realizada individualmente para cada módulo. É necessário ter o Python instalado.

**1. Execução do Servidor**
No terminal, acesse o diretório do servidor, ative a virtual environment correspondente e instale as dependências listadas:

```bash
cd server

# Ativação do ambiente virtual (Windows)
.\Scripts\activate
# Em terminais Unix/Bash: source Scripts/activate

# Instalação das bibliotecas
pip install -r requirements.txt

# Inicialização
python server.py
```

*Após rodar o script, clique no botão "Iniciar Servidor" na interface gráfica para abrir a porta de conexão.*

**2. Execução do Cliente**
Abra um **novo terminal** para não interromper o servidor. Acesse o diretório do cliente e repita o processo de ativação e instalação:

```bash
cd client

# Ativação do ambiente virtual
.\Scripts\activate
# Em terminais Unix/Bash: source Scripts/activate

# Instalação das bibliotecas
pip install -r requirements.txt

# Inicialização
python client.py
```

*Para simular múltiplos usuários simultâneos, abra novos terminais e execute novamente apenas o comando `python client.py`.*