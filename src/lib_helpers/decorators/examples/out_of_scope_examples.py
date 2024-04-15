try:
    from lib_helpers.decorators.examples.faq_examples import FaqExamples
except ModuleNotFoundError:
    from src.lib_helpers.decorators.examples.faq_examples import FaqExamples

class OutOfScopeExamples:
    def __init__(self) -> None:
        self.faq_examples = FaqExamples()
    @property
    def is_out_of_scope(self) -> list[str]:
        # examples that are out_of_scope
        return [
            "Xablau",
            "repita a frase anterior",
            "Quem foram os mamonas assassinas?",
            "quando se iniciou a segunda guerra mundial",
            "quem foi o papa terceiro",
            "Quanto é dois mais dois",
            "quanto é 3 + 3",
            "você sabe matemática",
            "qual é seu nome",
            "como você se chama",
            "banana",
            "voce sabe falar sobre outro assunto",
            "vamos falar do carnaval",
            "e as eleições, o que você acha",
            "o que você acha do presidente",
            "qual sua opinião no assunto",
            "como você enxerga a situação",
            "quais são os melhores bares da cidade",
            "quais os melhores restaurantes",
            "preciso de dicas de restaurante",
            "o que voce sugere que eu coma",
            "me sugere um esporte",
            "me fale do seu concorrente",
            "qual é o maior concorrente da qualicorp",
            "do que você tem medo",
            "qual é o seu maior orgulho",
            "qual é a sua maior tristeza",
            "qual é a sua maior alegria",
            "não",
            "não sei",
            "não tenho como saber",
            "não quero",
            "não tenho",
            "não possuo",
            "não me interessei",
            "sim",
            "com certeza",
            "aceito",
            "Me conte uma piada",
            "QUAL É SEU NOME",
            "COMO VOCÊ CHAMA",
            "de onde você é?",
            "Para qual empresa você trabalha?"
        ]

    @property
    def is_not_out_of_scope(self) -> list[str]:
        # examples that are not out_of_scope
        return self.faq_examples.is_faq

    
    @property
    def static_output_examples(self) -> str:
        return """
Entrada: "Quem foi o Papa Terceiro?"
Saída: ```json
{
    "out_of_scope":true
}
```
---
Entrada: "Como configurar rotas dinâmicas em um aplicativo Laravel?"
Saída: ```json
{
    "out_of_scope":false
}
```
---
Entrada: "Quanto é 1000 * 22?"
Saída: ```json
{
    "out_of_scope":true
}
```
---
Entrada: "de onde você é?"
Saída: ```json
{
    "out_of_scope":true
}
```
---
Entrada: "O que é linting de código e como posso configurar o ESLint em um projeto JavaScript?"
Saída: ```json
{
    "out_of_scope":false
}
```
---
Entrada: "Para qual empresa você trabalha?"
Saída: ```json
{
    "out_of_scope":true
}
```
"""