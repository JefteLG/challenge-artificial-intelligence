class FaqExamples:
    @property
    def is_faq(self) -> list[str]:
        # examples that are faq
        return [
            "Como posso centralizar um elemento na página usando apenas CSS?",
            "Qual é a diferença entre display: block, display: inline e display: inline-block?",
            "Como posso criar um layout responsivo para dispositivos móveis?",
            "Qual é a diferença entre null e undefined em JavaScript?",
            "Como faço para evitar callback hell em JavaScript?",
            "O que são closures e como elas funcionam em JavaScript?",
            "No Angular, como faço para criar um serviço que se comunique com um backend?",
            "Qual é a diferença entre state e props no React?",
            "Como posso adicionar roteamento em uma aplicação Vue.js?",
            "Qual é a diferença entre Node.js e Python para desenvolvimento backend?",
            "Como faço para implementar autenticação usando JWT (JSON Web Tokens) em uma aplicação Node.js?",
            "Qual é a diferença entre SQL e NoSQL?",
            "Como otimizar consultas em um banco de dados relacional?",
            "Quais são as vantagens e desvantagens de usar um banco de dados em memória como o Redis?",
            "Como o Django facilita o desenvolvimento web em Python?",
            "Quais são as principais diferenças entre o Express.js e o Koa.js no Node.js?",
            "Como usar o Git para colaborar em um projeto de desenvolvimento web?",
            "Qual é a diferença entre npm e yarn para gerenciamento de pacotes em JavaScript?",
            "O que é o padrão MVC (Model-View-Controller) e como ele é aplicado em desenvolvimento web?",
            "Qual é a diferença entre uma arquitetura monolítica e uma arquitetura de microsserviços?",
            "Como criar um menu de navegação com efeito de hover usando apenas CSS?",
            "Qual é a diferença entre margin e padding em CSS?",
            "Como posso incorporar fontes personalizadas em um site usando CSS?",
            "Como posso verificar se um objeto JavaScript está vazio?",
            "a diferença entre == e === em JavaScript?",
            "Como posso usar Promises para lidar com operações assíncronas em JavaScript?",
            "No Angular, como faço para criar um formulário reativo?",
            "Como posso implementar autenticação de usuário usando o React?",
            "Quais são as vantagens de usar o Vuex no Vue.js para gerenciamento de estado?",
            "Como configurar um servidor Node.js para lidar com solicitações HTTP?",
            "Qual é a diferença entre uma função síncrona e uma função assíncrona em JavaScript?",
            "Como faço para enviar e-mails programaticamente em uma aplicação Python usando o Flask?",
            "Como projetar um esquema de banco de dados relacional para uma aplicação de comércio eletrônico?",
            "Quais são as melhores práticas para lidar com a migração de dados em um banco de dados MongoDB?",
            "Como implementar cache de consultas em um aplicativo Laravel usando o Redis?",
            "Como criar um modelo de dados no Rails e associá-lo a outros modelos?",
            "os principais recursos do Spring Boot para o desenvolvimento de aplicativos Java?",
            "Qual é a diferença entre ESLint e Prettier para formatação de código JavaScript?",
            "Como usar o Docker para criar e implantar contêineres de aplicativos em um ambiente de produção?",
            "organizar arquivos e pastas em um projeto de frontend usando a estrutura MVC?",
            "Quais são as melhores práticas para documentar código em uma equipe de desenvolvimento colaborativo?",
            "Como criar um efeito de paralaxe em um site usando HTML e CSS?",
            "Qual é a diferença entre position: absolute, position: relative e position: fixed em CSS?",
            "Como criar uma animação de transição suave entre páginas usando apenas CSS?",
            "Como posso detectar o tipo de dispositivo (desktop, tablet, mobile) usando JavaScript?",
            "diferença entre forEach, map, filter e reduce em JavaScript?",
            "Como faço para implementar validação de formulário em tempo real usando JavaScript?",
            "Como posso implementar roteamento com navegação pre-renderizada em uma aplicação Ember.js?",
            "Quais são as diferenças fundamentais entre o AngularJS e o Angular?",
            "integrar uma biblioteca externa, como o D3.js, em um projeto React?",
            "Como configurar e utilizar um servidor Apache para hospedar uma aplicação PHP?",
            "Como implementar autenticação baseada em tokens usando o Django Rest Framework em Python?",
            "Quais são as principais diferenças entre o tratamento de erros síncronos e assíncronos em Node.js?",
            "Como projetar um sistema de mensagens em tempo real usando um banco de dados NoSQL como o MongoDB?",
            "Quais são as melhores práticas para otimizar consultas em um banco de dados MySQL?",
            "Como criar e manter backups automatizados de um banco de dados PostgreSQL?",
            "Como configurar rotas personalizadas em um aplicativo Rails?",
            "principais conceitos do Django ORM (Object-Relational Mapping)?",
            "Como configurar um ambiente de desenvolvimento local usando Vagrant e VirtualBox?",
            "Qual é a diferença entre um servidor web e um servidor de aplicação, e quando devo usar cada um?",
            "Quais são as melhores práticas para dividir um monólito em microserviços?",
            "Como usar o padrão de design Singleton em um projeto Java para garantir uma única instância de uma classe?",
            "O que é Firewall"
        ]
    
    @property
    def static_output_examples(self) -> str:
        return """
Entrada: "quero saber os princípios do SOLID e como aplicá-los no desenvolvimento de software"
Saída: ```json
{
    "faq":true
}
```
---
Entrada: "Açai é muito bom"
Saída: ```json
{
    "faq":false
}
```
---
Entrada: "diferença entre os métodos GET, POST, PUT e DELETE em solicitações HTTP"
Saída: ```json
{
    "faq":true
}
```
"""