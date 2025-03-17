# Projeto de Automação Residencial

## 📌 Descrição

Este é um projeto de automação residencial completo, para monitoramento e controle remoto de diversos sistemas em uma casa. O objetivo é permitir a gestão de Uma aquaponia, um pomar, aquário e partes residenciais como iluminação, consumo elétrico, hidráulico e muito mais, através de um painel web acessível remotamente e posteriormente por Aplicativo.

## 🖥️ Hardware Utilizado

- **Mini-PC Lenovo M910q**
- **STM32 F411CEU6 (Black Pill)** para leitura de sensores e acionamento de atuadores
- **Sensores**:
  - DS18B20 (temperatura da água)
  - DHT22 (temperatura e umidade ambiente)
  - Sensor de nível d'água
  - Sensor de vazamento de gás
  - Medidor de consumo elétrico
  - Sensor de umidade do solo
  - Sensor na caixa de correio
- **Atuadores**:
  - Relés para controle de bombas, iluminação e dispensador de ração
  - Válvulas solenóides para irrigar o pomar
- **Conectividade**:
  - Par trançado de cabo de rede para sensores com STM32
  - USB de STM32 para Mini-PC
  - Mini-PC configurado para acesso remoto

## 🛠️ Tecnologias Utilizadas

- **Backend**: Laravel (PHP) para API e painel web com Vue (Posteriormente aplicativo como alternativa ao painel)
- **Banco de Dados**: PostgreSQL
- **Microservices**: Python para comunicação com sensores e controle de dispositivos
- **Comunicação**:
  - MQTT (para troca de mensagens entre STM32 e backend)
  - WebSockets (para atualização em tempo real do painel Laravel)
- **Servidor Web**: Nginx
- **Gerenciamento de processos**: systemd + Supervisor

## 📂 Estrutura de Diretórios no Linux

```plaintext
/opt/home-automation/  
├── backend/                    # Laravel (API e Painel Web)  
│   ├── app/  
│   ├── bootstrap/  
│   ├── config/  
│   ├── database/               # Modelos e migrações do PostgreSQL  
│   ├── public/                 # Pasta acessível via web  
│   ├── resources/  
│   ├── routes/  
│   ├── storage/  
│   ├── .env                     # Configuração de banco, MQTT, etc.  
│   ├── artisan  
│   ├── composer.json  
│   └── package.json  
│  
├── microservices/               # Scripts Python para sensores/atuadores  
│   ├── aquarium.py              # Controle do aquário  
│   ├── aquaponics.py            # Controle da aquaponia  
│   ├── irrigation.py            # Irrigação do pomar  
│   ├── home_automation.py       # Luzes, câmeras, correio, gás, etc.  
│   ├── database.py              # Biblioteca comum para interagir com PostgreSQL  
│   ├── mqtt_client.py           # Cliente MQTT para comunicação entre ESP32 e backend  
│   ├── websocket_server.py      # WebSocket para Laravel receber dados em tempo real  
│   ├── .env                     # Configuração de conexão com banco e MQTT  
│   └── logs/                    # Logs dos sensores  
│  
├── firmware/                    # Código para ESP32  
│   ├── main.ino                 # Código do ESP32 (C++/MicroPython)  
│   ├── sensors/                 # Drivers dos sensores  
│   ├── actuators/               # Controle dos atuadores  
│   ├── mqtt_config.h            # Configuração do MQTT  
│   ├── wifi_config.h            # Configuração da rede Wi-Fi  
│   └── logs/  
│  
├── database/                     # PostgreSQL  
│   ├── backups/                  # Backups automáticos  
│   ├── init.sql                   # Script de criação de tabelas  
│   └── postgresql.conf            # Configurações otimizadas  
│  
├── services/                      # Configuração dos serviços no Debian  
│   ├── nginx/                     # Configuração do Nginx para o painel Laravel  
│   ├── systemd/                   # Arquivos .service para rodar Python na inicialização  
│   ├── supervisor/                # Configuração do Supervisor para processos Python  
│   └── docker/                    # (Opcional) Se quiser rodar alguns serviços em containers  
│  
└── docs/                          # Documentação do projeto  
```

## 📋 Funcionalidades

- 📡 **Monitoramento remoto em tempo real** (MQTT + WebSockets)
- 🌡 **Sensores ambientais e de consumo** (temperatura, umidade, energia, água)
- 🚰 **Automatização de bombas e irrigação** (baseado em umidade do solo)
- 🐟 **Controle de aquário e aquaponia** (bomba, luz, temperatura, alimentação)
- 💡 **Controle de iluminação** (automático e manual)
- 📹 **Integração com câmeras de segurança** (futuramente)
- 📬 **Sensor na caixa de correio** (alerta de entrega)
- 🔥 **Detector de vazamento de gás** (alerta e acionamento de exaustor sem faísca)
- 💾 **Registro de logs de todas as ações**

## 🚀 Próximos Passos

1. Configurar ambiente Debian com PostgreSQL, Laravel, Python e Nginx
2. Criar API em Laravel e scripts Python para sensores
3. Desenvolver firmware do ESP32 para comunicação com MQTT
4. Testar integração entre sensores, backend e painel web
