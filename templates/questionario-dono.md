# Questionário ao dono — <assunto>

Preenchido pelo `consultor-dominio` com o que já se sabe; o dono responde escrevendo
**resposta:** embaixo de cada pergunta. Pergunta sem resposta vale o padrão escrito nela. As
respostas vão literais ao escopo e, quando for o caso, ao cabeçalho do arquivo que implementa a
regra.

## O problema

1. **Qual problema, quem sente e quanto custa hoje?**
   Achado: <…> (fonte: <…>)
   Sem resposta, vale: o trabalho não começa.
   **resposta:**

2. **Que número vai mostrar que melhorou?**
   Achado: <…>
   Sem resposta, vale: o trabalho não começa.
   **resposta:**

## Requisitos em número

3. **Volume e pico, hoje e em doze meses?** Achado: <…> · Sem resposta, vale: "a medir".
   **resposta:**

4. **Tempo aceitável por item e disponibilidade exigida?** Achado: <…> · Sem resposta, vale: "a medir".
   **resposta:**

5. **Quanto dado se pode perder e quanto tempo se pode ficar fora (RPO e RTO)?**
   Sem resposta, vale: "a medir" — backup e redundância ficam como risco aberto.
   **resposta:**

## O domínio

6. **Qual fonte manda quando duas fontes divergem?** Achado: <…>
   Sem resposta, vale: <a mais conservadora>, com a divergência no log.
   **resposta:**

7. **O que parece igual e não é?** (os parecidos que não podem ser confundidos, e a palavra ou o
   atributo que os separa) Achado: <…>
   **resposta:**

8. **O que é eliminatório?** Achado: <…>
   **resposta:**

9. **Tolerâncias** (medida, prazo, valor) para cima e para baixo?
   Sem resposta, vale: tolerância zero.
   **resposta:**

10. **Na dúvida, o sistema segue e sinaliza, ou para e pergunta?** Consequência medida de cada
    lado: <…>
    **resposta:**

## Dados e risco

11. **Que dado pessoal entra, para quê e por quanto tempo?** Sem resposta, vale: nenhum dado
    pessoal é guardado.
    **resposta:**

12. **Pre-mortem: por que isto falharia em seis meses?**
    **resposta:**

## Prova

13. **Casos reais** (mascarados) do que deve passar e do que deve ser recusado, com a saída esperada:
    - <caso> → <esperado> (fonte: <…>)
    **resposta:** (confirme ou corrija)
