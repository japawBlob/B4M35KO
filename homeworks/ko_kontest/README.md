# KO kontest - Steiner tree

Největší prasárna, kterou jsem tenhle semestr napsal. Teorie výpočtu je správná, ale exekuce někde pokulhává. Cíleně si 
vybírám druhý terminál a nezačínám z prvního, protože mi to nevycházelo. Obdobně mi neprocházely první dva public vstupy, takže ty akorát printím. No prostě prasárna.

Ale idea implementace je správná. Jeden terminál je defacto 'zdroj' ze kterého vytéká tolik jednotek, kolik je ostatních
terminálů s tímže ostatní terminály konzumují jednu jednotku a zbytek flow odesálají dál. Jinak non-terminální nody posílají do sousedů, co do nich přijde.

Toto je jedno ze správných řešení a pokud se správně implementuje, tak dokonce funguje. 
